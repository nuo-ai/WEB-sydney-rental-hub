from fastapi import FastAPI, Request, Depends, HTTPException, Query, status, Security
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi_cache.coder import JsonCoder
from redis import asyncio as aioredis
from pydantic import BaseModel, Field, validator
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from jose import JWTError, jwt
from datetime import datetime, timedelta, date
# import os # os and load_dotenv are now handled in server.db
import logging
from typing import Any, Dict, List, Optional, TypeVar, Generic, Tuple
import json
import asyncio
import os
from contextlib import asynccontextmanager
import math
import base64
import httpx
from enum import Enum

# 从我们的模块导入
from api.graphql_schema import schema as gql_schema # Renamed to avoid conflict with strawberry.Schema
from api.auth_routes import router as auth_router # Import auth routes
import db as db_module # Import the module itself
from db import init_db_pool, close_db_pool, get_db_conn_dependency # Import specific functions

# Standardized API Response Models
T = TypeVar('T')

class PaginationInfo(BaseModel):
    total: int
    page: int = 1
    page_size: int = 20
    pages: int
    has_next: bool
    has_prev: bool
    next_cursor: Optional[str] = None

class ErrorInfo(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None

class APIResponse(BaseModel, Generic[T]):
    status: str = "success"
    data: Optional[T] = None
    pagination: Optional[PaginationInfo] = None
    error: Optional[ErrorInfo] = None

# Response Factory Functions
def success_response(data: Any = None, pagination: Optional[PaginationInfo] = None) -> Dict[str, Any]:
    return APIResponse(status="success", data=data, pagination=pagination).dict()

def error_response(code: str, message: str, status_code: int, details: Optional[Dict[str, Any]] = None) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=APIResponse(status="error", error=ErrorInfo(code=code, message=message, details=details)).dict(exclude_none=True)
    )

# Error Codes
class ErrorCodes:
    VALIDATION_ERROR = "VALIDATION_ERROR"
    AUTHENTICATION_ERROR = "AUTHENTICATION_ERROR"
    AUTHORIZATION_ERROR = "AUTHORIZATION_ERROR"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    BAD_REQUEST = "BAD_REQUEST"

# --- Security Configurations ---

# API Key Authentication
API_KEY = os.getenv("API_KEY", "your_default_dev_api_key") # Get API Key from environment
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="API key is missing")
    if api_key_header != API_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API Key")
    return api_key_header

# Rate Limiting
limiter = Limiter(key_func=get_remote_address)

# JWT Authentication
SECRET_KEY = os.getenv("SECRET_KEY", "a_very_secret_key_for_development")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token") # Placeholder token URL

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Placeholder for user model and DB interaction
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

async def get_user(username: str):
    # This is a placeholder. In a real app, you'd query the database.
    if username == "johndoe":
        return User(username="johndoe", email="johndoe@example.com", full_name="John Doe")
    return None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user(username=username)
    if user is None:
        raise credentials_exception
    return user

# Input Validation Model
class PropertyCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10)
    price: float = Field(..., gt=0)
    bedrooms: int = Field(..., ge=0)
    available_from: date
    
    @validator('title')
    def title_must_be_valid(cls, v):
        if '<script>' in v.lower():
            raise ValueError('Title cannot contain script tags')
        return v
    
    @validator('price')
    def price_must_be_reasonable(cls, v):
        if v > 10000000: # Set a reasonable max price
            raise ValueError('Price is out of reasonable range')
        return v

# --- End Security Configurations ---


# Pydantic Models for Pagination
class PaginationParams:
    def __init__(
        self,
        page: int = Query(1, ge=1, description="页码，从1开始"),
        page_size: int = Query(20, ge=1, le=100, description="每页项目数"),
        cursor: Optional[str] = Query(None, description="游标值（用于游标分页）")
    ):
        self.page = page
        self.page_size = page_size
        self.cursor = cursor


# Cursor helper functions
def encode_cursor(value: Any) -> str:
    return base64.urlsafe_b64encode(str(value).encode('utf-8')).decode('utf-8')

def decode_cursor(cursor: str) -> str:
    return base64.urlsafe_b64decode(cursor.encode('utf-8')).decode('utf-8')

# Asynchronous pagination logic adapted for psycopg2
async def paginate_query(db_conn: Any, query: str, count_query: str, params: tuple, pagination: PaginationParams) -> Tuple[List[Dict], PaginationInfo]:
    def _db_calls():
        with db_conn.cursor() as cursor:
            cursor.execute(count_query, params)
            total = cursor.fetchone()[0]
            
            offset = (pagination.page - 1) * pagination.page_size
            paginated_query = f"{query} LIMIT %s OFFSET %s"
            cursor.execute(paginated_query, params + (pagination.page_size, offset))
            
            items = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return items, columns, total

    items, columns, total = await asyncio.to_thread(_db_calls)
    
    pages = math.ceil(total / pagination.page_size) if total > 0 else 0
    
    pagination_info = PaginationInfo(
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
        pages=pages,
        has_next=pagination.page < pages,
        has_prev=pagination.page > 1,
    )
    # Transform property_description to description for consistency
    result = []
    for row in items:
        item_dict = dict(zip(columns, row))
        # Rename property_description to description if it exists
        if 'property_description' in item_dict:
            item_dict['description'] = item_dict.pop('property_description')
        result.append(item_dict)
    return result, pagination_info


# 配置日志 - (保持您现有的详细配置)
# Ensure this basicConfig is called only once, typically at the application entry point.
# If other modules also call basicConfig, it might lead to unexpected behavior.
# For a library/module like server.db, it's better to use logging.getLogger(__name__)
# and let the main application configure the root logger.
# However, since this is main.py, calling it here is usually fine.
if not logging.getLogger().handlers: # Configure only if no handlers are set
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(name)s - %(module)s - %(funcName)s - line %(lineno)d - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
    logging.getLogger().setLevel(logging.DEBUG)

logger = logging.getLogger(__name__) # Module-specific logger for main.py

logger.info("FastAPI应用启动中... 日志配置已设置为DEBUG级别 (如果之前未配置)。")

async def check_and_optimize_indexes():
    """
    检查并创建数据库性能优化索引
    只创建最关键的索引，避免启动时间过长
    """
    try:
        # 使用asyncpg直接连接数据库
        import asyncpg
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            logger.warning("DATABASE_URL未设置，跳过索引优化")
            return
            
        conn = await asyncpg.connect(database_url)
        try:
            # 检查最关键的复合索引是否存在
            check_sql = """
                SELECT COUNT(*) FROM pg_indexes 
                WHERE tablename = 'properties' 
                AND indexname = 'idx_properties_main_filter'
            """
            result = await conn.fetchval(check_sql)
            
            if result == 0:
                logger.info("检测到缺少关键索引，开始创建...")
                
                # 创建最重要的复合索引（覆盖90%的查询场景）
                # CONCURRENTLY 确保不锁表
                critical_indexes = [
                    {
                        'name': 'idx_properties_main_filter',
                        'sql': """
                            CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_properties_main_filter 
                            ON properties (suburb, rent_pw, bedrooms, available_date)
                            INCLUDE (address, property_type, bathrooms, parking_spaces, images)
                        """,
                        'description': '主筛选复合索引'
                    },
                    {
                        'name': 'idx_properties_available_now',
                        'sql': """
                            CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_properties_available_now 
                            ON properties (listing_id)
                            WHERE available_date IS NULL
                        """,
                        'description': 'Available Now快速查询'
                    },
                    {
                        'name': 'idx_properties_suburb_lower',
                        'sql': """
                            CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_properties_suburb_lower 
                            ON properties (lower(suburb))
                        """,
                        'description': '区域不分大小写搜索'
                    }
                ]
                
                for index in critical_indexes:
                    try:
                        await conn.execute(index['sql'])
                        logger.info(f"✅ 创建索引成功: {index['name']} - {index['description']}")
                    except Exception as e:
                        # 索引可能已存在或创建失败，不影响启动
                        logger.debug(f"索引 {index['name']} 创建跳过: {e}")
                
                # 更新统计信息
                await conn.execute("ANALYZE properties")
                logger.info("✅ 数据库索引优化完成，查询性能预计提升3-5倍")
            else:
                logger.info("关键索引已存在，跳过优化步骤")
        finally:
            await conn.close()
                
    except Exception as e:
        # 索引优化失败不应该阻止应用启动
        logger.warning(f"索引优化过程出现错误，但不影响服务启动: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("FastAPI application startup event triggered...")
    await init_db_pool()
    app.state.db_pool_initialized = True
    logger.info("Database pool initialization completed.")
    
    # 检查并优化数据库索引（增加可跳过与超时保护，避免启动卡死）
    # 仅在生产环境执行，或当未显式跳过时执行
    try:
        skip_opt = os.getenv("SKIP_INDEX_OPTIMIZATION", "").lower() in ("1", "true", "yes")
        optimize_timeout = float(os.getenv("INDEX_OPTIMIZE_TIMEOUT", "8"))
        if skip_opt or env != "production":
            logger.info(f"跳过索引优化：SKIP_INDEX_OPTIMIZATION={skip_opt}，env={env}")
        else:
            logger.info(f"开始索引优化（超时 {optimize_timeout}s）...")
            await asyncio.wait_for(check_and_optimize_indexes(), timeout=optimize_timeout)
    except asyncio.TimeoutError:
        logger.warning("索引优化超时，跳过并继续启动。")
    except Exception as e:
        logger.warning(f"索引优化检查失败: {e}. 继续启动...")
    
    # Initialize Redis Cache with fallback to in-memory cache（增加可配置与超时）
    try:
        redis_url = os.getenv("REDIS_URL", "").strip()
        if not redis_url:
            raise RuntimeError("REDIS_URL 未配置，使用内存缓存")
        connect_timeout = float(os.getenv("REDIS_CONNECT_TIMEOUT", "0.5"))
        socket_timeout = float(os.getenv("REDIS_SOCKET_TIMEOUT", "0.5"))
        ping_timeout = float(os.getenv("REDIS_PING_TIMEOUT", "1.0"))
        redis = aioredis.from_url(
            redis_url,
            encoding="utf8",
            decode_responses=True,
            socket_connect_timeout=connect_timeout,
            socket_timeout=socket_timeout
        )
        # Test Redis connection with timeout
        await asyncio.wait_for(redis.ping(), timeout=ping_timeout)
        app.state.redis = redis  # Store redis client in app state for cache invalidation
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
        logger.info(f"FastAPI Cache initialized with Redis backend ({redis_url}).")
    except Exception as e:
        logger.warning(f"Redis 不可用或未配置: {e}。使用内存缓存作为降级。")
        # 使用内存缓存作为降级方案
        from fastapi_cache.backends.inmemory import InMemoryBackend
        FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
        app.state.redis = None
        logger.info("FastAPI Cache initialized with InMemory backend (fallback).")

    yield
    # Shutdown
    logger.info("FastAPI application shutdown event triggered...")
    await close_db_pool()

# FastAPI 应用实例
app = FastAPI(title="Rental MCP Server", version="1.0.0", lifespan=lifespan)
app.state.limiter = limiter

# 自定义缓存键：使用完整URL（含查询参数）作为缓存键，确保分页/筛选（尤其 page/page_size、价格/日期）不会相互污染
# 为什么：计数请求（page_size=1）与列表请求（page_size=20）参数不同，默认键可能未包含查询，导致命中相同缓存条目
from fastapi import Request
def cache_key_by_url(func, namespace, request: Request, response, *args, **kwargs):
    return f"{namespace}:{str(request.url)}"

# Cache helper functions for selective invalidation
async def invalidate_property_cache(property_id: str = None):
    """Invalidate cache for a specific property or all properties"""
    redis = app.state.redis
    if not redis:
        logger.info("Cache invalidation skipped: Redis backend not configured.")
        return
    if property_id:
        # Invalidate specific property detail cache
        pattern = f"fastapi-cache:get_property_by_id:property_id={property_id}*"
    else:
        # Invalidate all property-related caches
        pattern = "fastapi-cache:get_properties*"
    
    async for key in redis.scan_iter(match=pattern):
        await redis.delete(key)
    
    logger.info(f"Cache invalidated for pattern: {pattern}")

async def invalidate_all_cache():
    """Invalidate all cache entries"""
    redis = app.state.redis
    if not redis:
        logger.info("Cache invalidation skipped: Redis backend not configured.")
        return
    async for key in redis.scan_iter(match="fastapi-cache:*"):
        await redis.delete(key)
    logger.info("All cache entries invalidated")

# CORS 中间件配置（动态化）
# 说明（为什么这么做）：
# - 生产环境仅放行明确的前端域名（安全优先）
# - 开发/非生产环境放宽（使用正则）以便于本地调试与临时域名验证
# - 允许通过环境变量 FRONTEND_URL 与 ADDITIONAL_CORS 配置额外来源（逗号分隔）
env = os.getenv("ENVIRONMENT", "development").lower()
frontend_url = os.getenv("FRONTEND_URL", "").strip()
additional_cors = os.getenv("ADDITIONAL_CORS", "").strip()

# 收集允许的来源（生产使用）
allowed_origins = {
    # 常见本地来源（用于生产时也可保留以便临时联调）
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:8888",
    "http://127.0.0.1:8888",
}

if frontend_url:
    allowed_origins.add(frontend_url)

if additional_cors:
    for origin in [x.strip() for x in additional_cors.split(",") if x.strip()]:
        allowed_origins.add(origin)

if env == "production" and allowed_origins:
    # 生产：白名单明确域名；保持 allow_credentials=True
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(allowed_origins),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    # 开发/非生产：使用正则允许任意来源，便于本地与临时公网域调试
    # 说明：使用 allow_origin_regex 可与 allow_credentials=True 共存，并回显具体 Origin
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=".*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Exception Handlers
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return error_response(
        code=ErrorCodes.RATE_LIMIT_EXCEEDED,
        message=f"Rate limit exceeded: {exc.detail}",
        status_code=status.HTTP_429_TOO_MANY_REQUESTS
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        code = ErrorCodes.RESOURCE_NOT_FOUND
    elif exc.status_code == 401:
        code = ErrorCodes.AUTHENTICATION_ERROR
    elif exc.status_code == 403:
        code = ErrorCodes.AUTHORIZATION_ERROR
    # Note: Rate limit (429) would be handled by its own library if used
    else:
        code = ErrorCodes.BAD_REQUEST
    
    return error_response(code=code, message=exc.detail, status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return error_response(
        code=ErrorCodes.VALIDATION_ERROR,
        message="Input validation failed",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        details={"errors": exc.errors()}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"An unhandled exception occurred: {exc}", exc_info=True)
    return error_response(
        code=ErrorCodes.INTERNAL_SERVER_ERROR,
        message="An internal server error occurred.",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


# 自定义 GraphQL 上下文获取器
async def get_graphql_context(request: Request, db_conn: Any = Depends(get_db_conn_dependency)) -> Dict[str, Any]:
    """
    Custom context getter for GraphQL.
    Injects the database connection from the pool into the GraphQL context.
    `Depends(get_db_conn_dependency)` uses FastAPI's dependency injection.
    """
    logger.info(f"DEBUG: Type of db_conn in get_graphql_context: {type(db_conn)}") # Debug print
    # logger.debug(f"GraphQL context: db_conn type: {type(db_conn)}, id: {id(db_conn)}")
    return {
        "request": request,
        "sync_db_conn": db_conn, # The connection from the pool via get_db_conn_dependency
        # Add other context variables if needed
    }

# --- Directions Endpoint Logic ---

class TravelMode(str, Enum):
    DRIVING = "DRIVING"
    WALKING = "WALKING"
    BICYCLING = "BICYCLING"
    TRANSIT = "TRANSIT"

class DirectionsRequest(BaseModel):
    origin: str = Query(..., description="起点坐标 'lat,lng'")
    destination: str = Query(..., description="目的地地址或坐标")
    mode: TravelMode = Query(TravelMode.DRIVING, description="出行方式")

@app.get("/api/directions", tags=["Services"])
@limiter.limit("30/minute")
async def get_directions(request: Request, params: DirectionsRequest = Depends()):
    """
    获取两个地点之间的通勤时间和距离。
    """
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        logger.error("GOOGLE_MAPS_API_KEY not set in environment.")
        return error_response(
            code=ErrorCodes.INTERNAL_SERVER_ERROR,
            message="Server configuration error.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    url = "https://maps.googleapis.com/maps/api/directions/json"
    request_params = {
        "origin": params.origin,
        "destination": params.destination,
        "mode": params.mode.value.lower(),
        "key": api_key
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=request_params)
            response.raise_for_status()  # Will raise an exception for 4XX/5XX responses
            data = response.json()

            if data["status"] != "OK":
                logger.warning(f"Google Maps API Warn: {data['status']} - {data.get('error_message', '')}")
                return success_response(data={"duration": "N/A", "distance": "N/A", "error": data.get('status', 'No results')})

            route = data["routes"][0]
            leg = route["legs"][0]
            
            return success_response(data={
                "duration": leg["duration"]["text"],
                "distance": leg["distance"]["text"]
            })

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error calling Google Maps API: {e.response.status_code} - {e.response.text}")
            return error_response(
                code="EXTERNAL_API_ERROR",
                message="Failed to fetch directions from external service.",
                status_code=status.HTTP_502_BAD_GATEWAY
            )
        except Exception as e:
            logger.error(f"An unexpected error occurred while fetching directions: {e}", exc_info=True)
            return error_response(
                code=ErrorCodes.INTERNAL_SERVER_ERROR,
                message="An internal error occurred.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# 创建 GraphQL 路由器，并使用自定义上下文
graphql_app_router = GraphQLRouter(
    gql_schema, # Use the imported schema
    context_getter=get_graphql_context, # Pass our custom context getter
    graphql_ide="graphiql" # Enable GraphiQL interface
)
# Include routers
app.include_router(auth_router, tags=["Authentication"])
app.include_router(graphql_app_router, prefix="/graphql", tags=["GraphQL"])


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint providing basic server status."""
    return {"message": "Rental MCP Server is running. Access GraphQL at /graphql"}

@app.get("/api/health", tags=["Debug"])
async def health_check():
    """A simple health check endpoint."""
    logger.info("Health check endpoint was called.")
    return {"status": "ok"}

@app.post("/api/cache/invalidate", tags=["Cache Management"])
async def invalidate_cache(
    property_id: Optional[str] = None,
    invalidate_all: bool = False
):
    """
    Invalidate cache selectively.
    - If property_id is provided, invalidate cache for that specific property
    - If invalidate_all is True, invalidate all cache entries
    - Otherwise, invalidate all property-related caches
    """
    try:
        if invalidate_all:
            await invalidate_all_cache()
            return {"status": "success", "message": "All cache entries invalidated"}
        else:
            await invalidate_property_cache(property_id)
            if property_id:
                return {"status": "success", "message": f"Cache invalidated for property {property_id}"}
            else:
                return {"status": "success", "message": "All property caches invalidated"}
    except Exception as e:
        logger.error(f"Failed to invalidate cache: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/api/cache/stats", tags=["Cache Management"])
async def get_cache_stats():
    """Get cache statistics"""
    try:
        redis = app.state.redis
        if not redis:
            return {
                "backend": "memory",
                "total_keys": 0,
                "property_list_cached": 0,
                "property_details_cached": 0,
                "memory_used": "N/A",
                "connected_clients": 0
            }
        info = await redis.info()
        keys_count = await redis.dbsize()
        
        # Count cache entries by pattern
        property_list_count = 0
        property_detail_count = 0
        
        async for key in redis.scan_iter(match="fastapi-cache:get_properties*"):
            property_list_count += 1
        
        async for key in redis.scan_iter(match="fastapi-cache:get_property_by_id*"):
            property_detail_count += 1
        
        return {
            "total_keys": keys_count,
            "property_list_cached": property_list_count,
            "property_details_cached": property_detail_count,
            "memory_used": info.get("used_memory_human", "N/A"),
            "connected_clients": info.get("connected_clients", 0)
        }
    except Exception as e:
        logger.error(f"Failed to get cache stats: {e}")
        return {"status": "error", "message": str(e)}

# Optional: Test endpoint for DB connection
@app.get("/test_db_connection", tags=["Debug"])
async def test_db(db: Any = Depends(get_db_conn_dependency)): # Kept async as it was
    """
    Temporarily modified to return the type of the injected 'db' object
    and check for 'cursor' attribute for debugging purposes.
    """
    # logger.info(f"DEBUG: Type of db in test_db: {type(db)}") # This log will be superseded by the response
    return {
        "status": "ok",
        "db_type": str(type(db)),
        "has_cursor": hasattr(db, "cursor")
    }

@app.get("/api/auth/test", tags=["Authentication"])
async def test_auth_system(db: Any = Depends(get_db_conn_dependency)):
    """Test endpoint to verify authentication system is working"""
    try:
        from crud.auth_crud import AuthCRUD
        
        # Test database tables exist
        with db.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name IN ('users', 'user_addresses')")
            table_count = cursor.fetchone()[0]
        
        # Initialize tables if they don't exist
        if table_count < 2:
            AuthCRUD.init_auth_tables(db)
            
        return {
            "status": "ok", 
            "message": "Authentication system is ready",
            "tables_initialized": True,
            "endpoints_available": [
                "/api/auth/register",
                "/api/auth/login", 
                "/api/auth/verify-email",
                "/api/auth/refresh",
                "/api/auth/me",
                "/api/auth/addresses"
            ]
        }
    except Exception as e:
        logger.error(f"Auth test error: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/api/email/test", tags=["Email"])
async def test_email_service():
    """Test email service configuration"""
    try:
        from services.email_service import test_email_service
        result = await test_email_service()
        return result
    except Exception as e:
        logger.error(f"Email test error: {e}")
        return {"status": "error", "message": str(e)}

@app.post("/api/email/test-send", tags=["Email"])
async def test_send_email(
    email: str = "test@example.com",
    name: str = "Test User"
):
    """Test sending a verification email (development only)"""
    try:
        from services.email_service import send_verification_email
        from config.email_config import get_email_config
        
        config = get_email_config()
        if not config.development_mode:
            return {"status": "error", "message": "Test email sending only available in development mode"}
        
        # Generate a test token
        import secrets
        test_token = secrets.token_urlsafe(32)
        
        success = await send_verification_email(email, name, test_token)
        
        return {
            "status": "success" if success else "error",
            "message": "Test email sent successfully" if success else "Failed to send test email",
            "email": email,
            "development_mode": config.development_mode,
            "test_token": test_token[:8] + "..." if success else None
        }
    except Exception as e:
        logger.error(f"Test send email error: {e}")
        return {"status": "error", "message": str(e)}

# ============== AI聊天系统 ==============

# Pydantic模型定义
class ChatMessage(BaseModel):
    role: str  # 'user', 'assistant', 'agent'
    content: str
    timestamp: Optional[str] = None
    agent_type: Optional[str] = None  # 'general', 'property', 'legal', 'contract', 'service'

class ChatRequest(BaseModel):
    message: str
    conversation_id: str
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    message: str
    agent_type: str
    cards: Optional[List[Dict[str, Any]]] = None
    suggestions: Optional[List[str]] = None

class PropertyCard(BaseModel):
    listing_id: int
    image: str
    price: int
    address: str
    commute: str
    bedrooms: str
    bathrooms: int
    features: List[str]

class ServiceCard(BaseModel):
    type: str
    title: str
    description: str
    price: str
    features: Optional[List[str]] = None
    action: str

# AI聊天服务类
class ChatService:
    def __init__(self):
        self.conversations = {}  # 存储会话上下文
        
    def route_to_agent(self, message: str) -> str:
        """智能路由到合适的Agent"""
        msg = message.lower()
        
        # 房源搜索相关
        if any(keyword in msg for keyword in ['房源', '房子', '租房', 'uts', 'unsw', 'usyd', '通勤', '距离']):
            return 'property'
        
        # 法律咨询相关
        if any(keyword in msg for keyword in ['法律', '权益', '押金', '房东', '租客', '违约']):
            return 'legal'
        
        # 合同审核相关
        if any(keyword in msg for keyword in ['合同', '条款', '签约', '协议', '审核']):
            return 'contract'
        
        # 服务相关
        if any(keyword in msg for keyword in ['代看房', '搬家', '咨询', '预约', '服务']):
            return 'service'
        
        return 'general'
    
    async def process_message(self, request: ChatRequest, db_conn: Any) -> ChatResponse:
        """处理聊天消息"""
        message = request.message
        conversation_id = request.conversation_id
        
        # 路由到合适的Agent
        agent_type = self.route_to_agent(message)
        
        # 根据Agent类型处理消息
        if agent_type == 'property':
            return await self.handle_property_query(message, db_conn)
        elif agent_type == 'legal':
            return await self.handle_legal_query(message)
        elif agent_type == 'contract':
            return await self.handle_contract_query(message)
        elif agent_type == 'service':
            return await self.handle_service_query(message)
        else:
            return await self.handle_general_query(message)
    
    async def handle_property_query(self, message: str, db_conn: Any) -> ChatResponse:
        """处理房源查询"""
        msg = message.lower()
        
        # 检查是否询问大学相关
        universities = ['uts', 'unsw', 'usyd', 'macquarie', '悉尼科技大学', '新南威尔士大学', '悉尼大学']
        mentioned_uni = None
        for uni in universities:
            if uni in msg:
                mentioned_uni = uni
                break
        
        if mentioned_uni:
            uni_name = self.get_university_name(mentioned_uni)
            response_text = f"好的！我来为您推荐{uni_name}附近的房源。"
            
            # 模拟房源数据（实际应该从数据库查询）
            property_cards = [
                {
                    "id": 1,
                    "image": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=300&h=200&fit=crop",
                    "price": 776,
                    "address": "Central Park Student Village",
                    "commute": "UTS步行8分钟",
                    "bedrooms": "Studio",
                    "bathrooms": 1,
                    "features": ["空调", "洗衣机", "高速网络"]
                },
                {
                    "id": 2,
                    "image": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=300&h=200&fit=crop",
                    "price": 706,
                    "address": "Redfern Student Accommodation",
                    "commute": "UTS轻轨10分钟",
                    "bedrooms": "Studio",
                    "bathrooms": 1,
                    "features": ["健身房", "停车位", "安保"]
                }
            ]
            
            return ChatResponse(
                message=response_text,
                agent_type="property",
                cards=property_cards,
                suggestions=["查看更多房源", "预约代看房", "了解通勤详情"]
            )
        else:
            return ChatResponse(
                message="我来帮您找房源！请告诉我您的需求：\n\n• 您在哪所大学上学？\n• 预算范围是多少？\n• 偏好的区域或交通方式？",
                agent_type="property",
                suggestions=["UTS附近房源", "UNSW附近房源", "USYD附近房源", "预算$500-800"]
            )
    
    async def handle_legal_query(self, message: str) -> ChatResponse:
        """处理法律咨询"""
        msg = message.lower()
        
        if '押金' in msg:
            response = """关于押金的法律规定：

**押金标准**：
• 一般不超过4周租金
• 必须存入政府监管账户
• 不能用作最后一期租金

**退还条件**：
• 房屋无损坏：全额退还
• 有损坏：扣除维修费后退还
• 14天内必须处理

**我们的建议**：
签约时拍照记录房屋状态，搬出时也要拍照对比。"""
        elif '房东' in msg or '权益' in msg:
            response = """澳洲租客权益保护：

**房东不能**：
• 随意进入您的房间
• 无理由驱赶租客
• 歧视性对待

**您的权利**：
• 安静享用权
• 维修要求权
• 隐私保护权

**需要帮助时**：
• 联系当地租客协会
• 申请仲裁服务
• 寻求法律援助"""
        else:
            response = """我是您的租赁法律顾问！我可以帮您解答：

• 租房合同条款解释
• 押金和租金相关法规
• 租客权益保护
• 房东责任义务
• 违约和纠纷处理

请具体告诉我您遇到的问题？"""
        
        service_card = {
            "type": "legal",
            "title": "⚖️ 专业法律咨询",
            "description": "复杂案例人工法律顾问",
            "price": "$99",
            "features": ["30分钟专业咨询", "书面意见书", "中文全程服务"],
            "action": "预约咨询"
        }
        
        return ChatResponse(
            message=response,
            agent_type="legal",
            cards=[service_card],
            suggestions=["押金问题", "房东纠纷", "合同条款", "预约法律咨询"]
        )
    
    async def handle_contract_query(self, message: str) -> ChatResponse:
        """处理合同审核"""
        response = """我可以帮您审核租房合同！

**AI快速审核**：
• 30秒识别关键条款
• 标注潜在风险点
• 提供修改建议
• 生成审核报告

**常见风险条款**：
• 过高的违约金
• 不合理的维修责任
• 模糊的押金条款
• 限制性使用规定

上传您的合同，我来为您详细分析！"""
        
        service_card = {
            "type": "contract",
            "title": "📋 AI合同审核",
            "description": "智能识别风险条款",
            "price": "$25",
            "features": ["30秒快速分析", "风险点标注", "修改建议", "专业报告"],
            "action": "上传合同"
        }
        
        return ChatResponse(
            message=response,
            agent_type="contract",
            cards=[service_card],
            suggestions=["上传合同", "常见条款说明", "风险案例", "法律建议"]
        )
    
    async def handle_service_query(self, message: str) -> ChatResponse:
        """处理服务查询"""
        msg = message.lower()
        
        if '代看房' in msg:
            response = "我来为您介绍代看房服务！这是我们最受欢迎的服务。"
            
            service_card = {
                "type": "inspection",
                "title": "🏠 专业代看房服务",
                "description": "专业顾问实地看房拍摄",
                "price": "$35",
                "features": ["专业拍摄录像", "详细评估报告", "2小时内完成", "微信实时沟通"],
                "action": "立即预约"
            }
            
            return ChatResponse(
                message=response,
                agent_type="service",
                cards=[service_card],
                suggestions=["预约代看房", "查看服务详情", "价格说明", "服务流程"]
            )
        else:
            response = "我们提供全方位的租房服务！"
            
            service_cards = [
                {
                    "type": "inspection",
                    "title": "🏠 代看房服务",
                    "description": "专业实地看房录像",
                    "price": "$35",
                    "action": "立即预约"
                },
                {
                    "type": "moving",
                    "title": "🚚 学生搬家",
                    "description": "小件物品搬运",
                    "price": "$89起",
                    "action": "获取报价"
                },
                {
                    "type": "consultation",
                    "title": "💼 签约陪同",
                    "description": "中文全程陪同",
                    "price": "$59",
                    "action": "预约服务"
                }
            ]
            
            return ChatResponse(
                message=response,
                agent_type="service",
                cards=service_cards,
                suggestions=["代看房服务", "搬家服务", "签约陪同", "全套服务包"]
            )
    
    async def handle_general_query(self, message: str) -> ChatResponse:
        """处理通用查询"""
        msg = message.lower()
        
        if '你好' in msg or 'hello' in msg:
            response = "您好！很高兴为您服务 😊 我是您的专属租房助手，可以帮您找房源、安排看房、解答法律问题。您想了解什么？"
        elif '价格' in msg or '多少钱' in msg:
            response = """我们的服务价格透明公开：

🏠 **代看房服务**: $35/次
📋 **合同审核**: $25/份  
⚖️ **法律咨询**: $99/次
🚚 **搬家服务**: $89起
💼 **签约陪同**: $59/次

所有服务都是一次性收费，无隐藏费用！需要了解具体哪项服务？"""
        elif '大学' in msg or '学校' in msg:
            response = """我们主要服务这些大学的学生：

🏫 **悉尼科技大学** (UTS)
🏫 **新南威尔士大学** (UNSW)  
🏫 **悉尼大学** (USYD)
🏫 **麦考瑞大学** (Macquarie)

请告诉我您在哪所大学，我来为您推荐附近的优质房源！"""
        else:
            response = """我理解您的问题。作为专业的租房助手，我可以帮您：

🔍 **智能找房**: 根据大学推荐房源
🏠 **代看房服务**: $35专业实地看房  
📋 **合同审核**: AI快速识别风险条款
⚖️ **法律咨询**: 专业租房法律建议
🚚 **配套服务**: 搬家、签约陪同等

您最想了解哪方面？"""
        
        return ChatResponse(
            message=response,
            agent_type="general",
            suggestions=["找房源", "代看房服务", "法律咨询", "价格说明"]
        )
    
    def get_university_name(self, uni_code: str) -> str:
        """获取大学中文名称"""
        names = {
            'uts': '悉尼科技大学',
            'unsw': '新南威尔士大学', 
            'usyd': '悉尼大学',
            'macquarie': '麦考瑞大学',
            '悉尼科技大学': '悉尼科技大学',
            '新南威尔士大学': '新南威尔士大学',
            '悉尼大学': '悉尼大学'
        }
        return names.get(uni_code.lower(), uni_code)

# 创建聊天服务实例
chat_service = ChatService()

# AI聊天API端点
@app.post("/api/chat", response_model=ChatResponse, tags=["AI Chat"])
async def chat_endpoint(request: ChatRequest, db_conn: Any = Depends(get_db_conn_dependency)):
    """AI聊天API端点"""
    try:
        logger.info(f"收到聊天请求: {request.message}")
        response = await chat_service.process_message(request, db_conn)
        logger.info(f"聊天响应: {response.message[:100]}...")
        return response
    except Exception as e:
        logger.error(f"聊天处理错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"聊天处理失败: {str(e)}")

# Note: Ensure that `server.api.graphql_schema.py` uses `info.context.get('sync_db_conn')`
# to retrieve the database connection in its resolvers.
# The `get_db_session` context manager will handle returning the connection to the pool.

# --- Celery Task Endpoints ---
from celery_config import celery_app
from tasks import debug_task, example_db_task
from celery.result import AsyncResult

@app.post("/api/tasks/debug", status_code=status.HTTP_202_ACCEPTED, tags=["Tasks"])
async def start_debug_task(api_key: str = Security(get_api_key)):
    """Endpoint to trigger the simple debug task."""
    try:
        logger.info("Attempting to queue debug_task...")
        task = debug_task.delay()
        logger.info(f"Task {task.id} queued successfully.")
        return success_response(data={"task_id": task.id, "message": "Debug task started"})
    except Exception as e:
        logger.error(f"Failed to queue debug_task: {e}", exc_info=True)
        return error_response(
            code=ErrorCodes.INTERNAL_SERVER_ERROR,
            message="Failed to queue task.",
            status_code=500
        )

@app.post("/api/tasks/db", status_code=status.HTTP_202_ACCEPTED, tags=["Tasks"])
async def start_db_task(api_key: str = Security(get_api_key)):
    """Endpoint to trigger the example database task."""
    try:
        logger.info("Attempting to queue example_db_task...")
        # Pass some example data to the task
        task = example_db_task.delay("Hello from FastAPI endpoint!")
        logger.info(f"Task {task.id} queued successfully.")
        return success_response(data={"task_id": task.id, "message": "Database task started"})
    except Exception as e:
        logger.error(f"Failed to queue db_task: {e}", exc_info=True)
        return error_response(
            code=ErrorCodes.INTERNAL_SERVER_ERROR,
            message="Failed to queue task.",
            status_code=500
        )

@app.get("/api/tasks/{task_id}", tags=["Tasks"], response_model=APIResponse)
async def get_task_status(task_id: str, api_key: str = Security(get_api_key)):
    """Endpoint to check the status of a Celery task."""
    task_result = AsyncResult(task_id, app=celery_app)
    
    response_data = {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result if task_result.ready() else None,
    }

    if task_result.failed():
        return error_response(
            code="TASK_FAILED",
            message="The task failed to execute.",
            status_code=500,
            details=response_data
        )
        
    return success_response(data=response_data)
# --- End Celery Task Endpoints ---

from crud.properties_crud import get_property_by_id_from_db

@app.get("/api/properties/{property_id}", tags=["Properties"], response_model=APIResponse[Dict])
@cache(expire=1800)  # Cache for 30 minutes
async def get_property_by_id(property_id: str, db: Any = Depends(get_db_conn_dependency)):
    """
    Get a single property by its ID.
    """
    logger.info(f"====== HIT get_property_by_id with ID: {property_id} ======")
    # In a real app, you would have a CRUD function to get a single property
    # For now, we'll fetch all and filter, which is inefficient.
    # This should be replaced with a direct DB call.
    # NOTE: This is a placeholder implementation.
    
    # Correct implementation:
    prop = await asyncio.to_thread(get_property_by_id_from_db, property_id)
    if not prop:
        return error_response(
            code=ErrorCodes.RESOURCE_NOT_FOUND,
            message=f"Property with ID {property_id} not found.",
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    # Manually convert the Strawberry object to a dictionary
    prop_dict = {
        "listing_id": prop.listing_id,
        "address": prop.address,
        "suburb": prop.suburb,
        "rent_pw": prop.rent_pw,
        "bedrooms": prop.bedrooms,
        "bathrooms": prop.bathrooms,
        "property_type": prop.property_type,
        "property_url": prop.property_url,
        "postcode": prop.postcode,
        "bond": prop.bond,
        "parking_spaces": prop.parking_spaces,
        "available_date": prop.available_date,
        "images": prop.images,
        "property_features": prop.property_features,
        "latitude": prop.latitude,
        "longitude": prop.longitude,
        "geom_wkt": prop.geom_wkt,
        "is_furnished": prop.is_furnished,
        "description": prop.description,  # Add description field
        "property_headline": prop.property_headline,  # 添加房源标题字段
        "inspection_times": prop.inspection_times  # 补充看房时间字段，修复刷新后消失
    }
    
    return success_response(data=prop_dict)


@app.get("/api/properties", tags=["Properties"], response_model=APIResponse[List[Dict]])
@cache(expire=900, key_builder=cache_key_by_url)  # Cache for 15 minutes（包含URL查询参数到缓存键）
async def get_properties(
    pagination: PaginationParams = Depends(), 
    db: Any = Depends(get_db_conn_dependency),
    # Filter parameters
    suburb: Optional[str] = None,
    property_type: Optional[str] = None,
    bedrooms: Optional[str] = None,  # Can be comma-separated like "1,2,3"
    bathrooms: Optional[str] = None,  # Can be comma-separated like "1,2"
    parking: Optional[str] = None,  # Can be comma-separated like "0,1,2"
    minPrice: Optional[int] = None,
    maxPrice: Optional[int] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    isFurnished: Optional[bool] = None,
    # 兼容参数（V2/部分入口）：如传入 furnished=true，则等价于 isFurnished=true
    furnished: Optional[bool] = None,
    # 点名过滤（便于校验）
    listing_id: Optional[str] = None,
    # 排序参数（白名单）：price_asc/available_date_asc/suburb_az/inspection_earliest
    sort: Optional[str] = None,
):
    """
    Get a paginated list of properties with optional filters.
    Supports both page-based and cursor-based pagination.
    """
    # Build the base query with filters - 只选择列表页需要的字段，减少数据传输
    # 排除大字段如 description 和 property_features，提升性能
    base_query = """SELECT 
        listing_id, property_url, address, suburb, state, postcode, 
        property_type, rent_pw, bond, bedrooms, bathrooms, parking_spaces,
        available_date, inspection_times, agency_name, agent_name,
        property_headline, latitude, longitude, images,
        is_active, status, created_at, last_updated,
        has_air_conditioning, is_furnished, has_balcony, has_dishwasher,
        has_laundry, has_parking, has_pool, has_gym
    FROM properties"""
    count_query = "SELECT COUNT(*) FROM properties"
    
    # Build WHERE clause conditions
    conditions = []
    params = []
    
    # 始终只返回活跃的房源（关键修复：过滤已下架房源）
    conditions.append("is_active = TRUE")
    
    # 指定 listing_id 时做点名过滤（便于校验/复现单条）
    if listing_id:
        try:
            lid = int(listing_id)
            conditions.append("listing_id = %s")
            params.append(lid)
        except (ValueError, TypeError):
            # 忽略非法 id，不影响其他条件
            pass

    # Add suburb filter - support multiple suburbs (comma-separated)
    if suburb:
        # Split by comma and trim whitespace
        suburbs = [s.strip() for s in suburb.split(',')]
        if len(suburbs) == 1:
            # Single suburb - use ILIKE for partial matching
            conditions.append("suburb ILIKE %s")
            params.append(f"%{suburbs[0]}%")
        else:
            # Multiple suburbs - use ILIKE with OR for case-insensitive matching
            suburb_conditions = []
            for sub in suburbs:
                suburb_conditions.append("suburb ILIKE %s")
                params.append(f"%{sub}%")
            conditions.append(f"({' OR '.join(suburb_conditions)})")
    
    # Add property type filter
    if property_type:
        conditions.append("property_type ILIKE %s")
        params.append(f"%{property_type}%")
    
    # Add bedrooms filter (handle comma-separated values)
    if bedrooms:
        bedroom_values = bedrooms.split(',')
        bedroom_conditions = []
        bedroom_params: List[int] = []
        for value in bedroom_values:
            value = value.strip()
            if value == '4+':
                bedroom_conditions.append("bedrooms >= %s")
                bedroom_params.append(4)
            elif value.isdigit():
                bedroom_conditions.append("bedrooms = %s")
                bedroom_params.append(int(value))
        if bedroom_conditions:
            conditions.append(f"({' OR '.join(bedroom_conditions)})")
            params.extend(bedroom_params)
    
    # Add bathrooms filter (handle comma-separated values)
    if bathrooms:
        bathroom_values = bathrooms.split(',')
        bathroom_conditions = []
        bathroom_params: List[int] = []
        for value in bathroom_values:
            value = value.strip()
            if value == '3+':
                bathroom_conditions.append("bathrooms >= %s")
                bathroom_params.append(3)
            elif value.isdigit():
                bathroom_conditions.append("bathrooms = %s")
                bathroom_params.append(int(value))
        if bathroom_conditions:
            conditions.append(f"({' OR '.join(bathroom_conditions)})")
            params.extend(bathroom_params)
    
    # Add parking filter (handle comma-separated values)
    if parking:
        parking_values = parking.split(',')
        parking_conditions = []
        parking_params: List[int] = []
        for value in parking_values:
            value = value.strip()
            if value == '2+':
                parking_conditions.append("parking_spaces >= %s")
                parking_params.append(2)
            elif value.isdigit():
                parking_conditions.append("parking_spaces = %s")
                parking_params.append(int(value))
        if parking_conditions:
            conditions.append(f"({' OR '.join(parking_conditions)})")
            params.extend(parking_params)
    
    # Add price range filters
    if minPrice is not None:
        conditions.append("rent_pw >= %s")
        params.append(minPrice)
    
    if maxPrice is not None:
        conditions.append("rent_pw <= %s")
        params.append(maxPrice)
    
    # Add date filters
    # 处理空出日期筛选逻辑：
    # - NULL表示"Available now"（立即可入住）
    # - date_from到date_to：筛选在这个时间段内空出的房源
    # - 如果时间段包含今天或过去，NULL（Available now）应该被包含
    from datetime import datetime
    today = datetime.now().date()
    
    if date_from and date_to:
        # 用户选择了时间范围：找在这个时间段内空出的房源
        # 如果date_from <= 今天，包含Available now的房源
        if datetime.strptime(date_from, '%Y-%m-%d').date() <= today:
            conditions.append(
                "(available_date IS NULL OR (available_date >= %s AND available_date <= %s))"
            )
        else:
            # 未来的时间段，不包含Available now
            conditions.append(
                "(available_date >= %s AND available_date <= %s)"
            )
        params.append(date_from)
        params.append(date_to)
    elif date_from:
        # 只有开始日期：找从这个日期之后空出的房源
        if datetime.strptime(date_from, '%Y-%m-%d').date() <= today:
            conditions.append(
                "(available_date IS NULL OR available_date >= %s)"
            )
        else:
            conditions.append("available_date >= %s")
        params.append(date_from)
    elif date_to:
        # 只有结束日期：找在这个日期之前空出的房源
        conditions.append(
            "(available_date IS NULL OR available_date <= %s)"
        )
        params.append(date_to)
    
    # 家具筛选（兼容 isFurnished 与 furnished 两个键；仅当显式为 true/false 时才筛）
    # 说明：将 is_furnished 统一转为文本后做集合匹配，避免历史 text/三态导致的 500；不会把 'unknown' 当 true/false
    effectiveFurnished = isFurnished if isFurnished is not None else furnished
    if effectiveFurnished is not None:
        if effectiveFurnished:
            conditions.append("NULLIF(TRIM(LOWER(is_furnished::text)), '') IN ('t','true','yes','1')")
        else:
            conditions.append("NULLIF(TRIM(LOWER(is_furnished::text)), '') IN ('f','false','no','0')")
    
    # Build WHERE clause
    where_clause = ""
    if conditions:
        where_clause = " WHERE " + " AND ".join(conditions)
    
    # Update queries with WHERE clause
    base_query += where_clause
    count_query += where_clause

    # 排序映射（为什么：让前端 Sort 真正生效；仅允许白名单，防注入；并附加 listing_id ASC 作为稳定次序键）
    order_clause = " ORDER BY listing_id ASC"
    if sort:
        s = str(sort).strip().lower()
        if s == "price_asc":
            order_clause = " ORDER BY rent_pw ASC NULLS LAST, listing_id ASC"
        elif s == "available_date_asc":
            order_clause = " ORDER BY available_date ASC NULLS FIRST, listing_id ASC"
        elif s == "suburb_az":
            order_clause = " ORDER BY lower(suburb) ASC NULLS LAST, listing_id ASC"
        elif s == "inspection_earliest":
            # TODO：P1 精确解析 inspection_times 的“最早看房时间”进行排序
            # 当前先与 available_date_asc 等价，满足 P0 真正生效的前端表现
            order_clause = " ORDER BY available_date ASC NULLS FIRST, listing_id ASC"
    
    
    # Simple cursor implementation based on listing_id
    # A more robust implementation would handle sorting
    if pagination.cursor:
        try:
            cursor_val = int(decode_cursor(pagination.cursor))
            # Add cursor condition to existing WHERE clause
            if where_clause:
                query = f"{base_query} AND listing_id > %s ORDER BY listing_id ASC"
            else:
                query = f"{base_query} WHERE listing_id > %s ORDER BY listing_id ASC"
            # Append cursor value to existing params
            cursor_params = params + [cursor_val]
        except (ValueError, TypeError):
            raise HTTPException(status_code=400, detail="Invalid cursor")

        def _db_call_cursor():
            with db.cursor() as cur:
                # Fetch one more than page_size to check for has_next
                cur.execute(f"{query} LIMIT %s", cursor_params + [pagination.page_size + 1])
                items = cur.fetchall()
                columns = [desc[0] for desc in cur.description]
                return items, columns
        
        items, columns = await asyncio.to_thread(_db_call_cursor)
        
        has_next = len(items) > pagination.page_size
        if has_next:
            items = items[:-1] # remove extra item
        
        items_as_dicts = []
        for row in items:
            item_dict = dict(zip(columns, row))
            # Rename property_description to description if it exists
            if 'property_description' in item_dict:
                item_dict['description'] = item_dict.pop('property_description')
            items_as_dicts.append(item_dict)
        next_cursor = encode_cursor(items_as_dicts[-1]['listing_id']) if items_as_dicts and has_next else None

        pagination_info = PaginationInfo(
            total=-1, # Cursor pagination doesn't usually return total
            page=1, # Page number is not relevant for cursor
            page_size=pagination.page_size,
            pages=-1,
            has_next=has_next,
            has_prev=pagination.cursor is not None,
            next_cursor=next_cursor
        )
        return success_response(data=items_as_dicts, pagination=pagination_info)
    else:
        # Page-based pagination
        query = f"{base_query}{order_clause}"
        items, pagination_info = await paginate_query(db, query, count_query, tuple(params), pagination)
        return success_response(data=items, pagination=pagination_info)


# ========================================
# Location/Search Suggestions API
# ========================================

@app.get("/api/locations/suggestions", tags=["Locations"])
@cache(expire=900)  # Cache for 15 minutes
async def get_location_suggestions(
    q: Optional[str] = Query(None, description="Search query"),
    limit: int = Query(20, ge=1, le=100),
    db: Any = Depends(get_db_conn_dependency)
):
    """
    Get location suggestions for search autocomplete.
    Returns suburbs and postcodes with property counts.
    """
    try:
        if q and len(q.strip()) > 0:
            # Search with query
            search_term = q.strip().lower()
            
            query = """
            SELECT 
                suburb,
                REPLACE(COALESCE(postcode, '0'), '.0', '') as clean_postcode,
                COUNT(DISTINCT listing_id) as property_count
            FROM properties
            WHERE suburb IS NOT NULL
                AND is_active = TRUE
                AND (
                    LOWER(suburb) LIKE %s
                    OR REPLACE(postcode, '.0', '') LIKE %s
                )
            GROUP BY suburb, REPLACE(COALESCE(postcode, '0'), '.0', '')
            ORDER BY 
                CASE 
                    WHEN LOWER(suburb) = %s THEN 1
                    WHEN LOWER(suburb) LIKE %s THEN 2
                    ELSE 3
                END,
                property_count DESC
            LIMIT %s
            """
            
            def _db_call():
                with db.cursor() as cur:
                    cur.execute(query, (
                        f'%{search_term}%',
                        f'{search_term}%',
                        search_term,
                        f'{search_term}%',
                        limit
                    ))
                    results = cur.fetchall()
                    return results
            
            results = await asyncio.to_thread(_db_call)
            
            # Format results
            suggestions = []
            for row in results:
                suburb = row[0]
                postcode = row[1]
                count = row[2]
                
                suggestions.append({
                    "id": f"{suburb}_{postcode}",
                    "type": "suburb",
                    "name": suburb,
                    "postcode": postcode,
                    "fullName": f"{suburb}, NSW, {postcode}",
                    "count": count
                })
            
            return success_response(data=suggestions)
        
        else:
            # No query - return all locations
            query = """
            SELECT 
                suburb,
                REPLACE(COALESCE(postcode, '0'), '.0', '') as postcode,
                COUNT(DISTINCT listing_id) as property_count
            FROM properties
            WHERE suburb IS NOT NULL
              AND is_active = TRUE
            GROUP BY suburb, REPLACE(COALESCE(postcode, '0'), '.0', '')
            ORDER BY property_count DESC
            LIMIT %s
            """
            
            def _db_call():
                with db.cursor() as cur:
                    cur.execute(query, (limit,))
                    results = cur.fetchall()
                    return results
            
            results = await asyncio.to_thread(_db_call)
            
            # Format results
            suggestions = []
            for row in results:
                suburb = row[0]
                postcode = row[1]
                count = row[2]
                
                suggestions.append({
                    "id": f"{suburb}_{postcode}",
                    "type": "suburb",
                    "name": suburb,
                    "postcode": postcode,
                    "fullName": f"{suburb}, NSW, {postcode}",
                    "count": count
                })
            
            return success_response(data=suggestions)
            
    except Exception as e:
        logger.error(f"Error getting location suggestions: {str(e)}")
        return error_response(f"Failed to get location suggestions: {str(e)}")


@app.get("/api/locations/all", tags=["Locations"])
@cache(expire=900)  # Cache for 15 minutes
async def get_all_locations(
    db: Any = Depends(get_db_conn_dependency)
):
    """
    Get all unique locations with property counts.
    Used for initializing search suggestions.
    """
    try:
        query = """
        SELECT 
            suburb,
            REPLACE(COALESCE(postcode, '0'), '.0', '') as postcode,
            COUNT(DISTINCT listing_id) as property_count
        FROM properties
        WHERE suburb IS NOT NULL
          AND is_active = TRUE
        GROUP BY suburb, REPLACE(COALESCE(postcode, '0'), '.0', '')
        ORDER BY property_count DESC
        """
        
        def _db_call():
            with db.cursor() as cur:
                cur.execute(query)
                results = cur.fetchall()
                return results
        
        results = await asyncio.to_thread(_db_call)
        
        # Format results for both suburb and postcode lookups
        locations = []
        postcode_map = {}
        
        for row in results:
            suburb = row[0]
            postcode = row[1]
            count = row[2]
            
            # Add suburb entry
            locations.append({
                "id": f"{suburb}_{postcode}",
                "type": "suburb",
                "name": suburb,
                "postcode": postcode,
                "fullName": f"{suburb}, NSW, {postcode}",
                "count": count
            })
            
            # Aggregate by postcode
            if postcode not in postcode_map:
                postcode_map[postcode] = {
                    "id": f"postcode_{postcode}",
                    "type": "postcode",
                    "name": postcode,
                    "suburbs": [],
                    "fullName": f"{postcode}",
                    "count": 0
                }
            postcode_map[postcode]["suburbs"].append(suburb)
            postcode_map[postcode]["count"] += count
        
        # Update postcode fullNames with suburb list
        for postcode_data in postcode_map.values():
            suburbs_str = ", ".join(postcode_data["suburbs"][:3])  # Show first 3 suburbs
            if len(postcode_data["suburbs"]) > 3:
                suburbs_str += f" +{len(postcode_data['suburbs']) - 3} more"
            postcode_data["fullName"] = f"{postcode_data['name']} ({suburbs_str})"
            locations.append(postcode_data)
        
        # Sort by count
        locations.sort(key=lambda x: x["count"], reverse=True)
        
        return success_response(data=locations)
        
    except Exception as e:
        logger.error(f"Error getting all locations: {str(e)}")
        return error_response(f"Failed to get locations: {str(e)}")


@app.get("/api/locations/nearby", tags=["Locations"])
@cache(expire=900)  # Cache for 15 minutes
async def get_nearby_suburbs(
    suburb: str = Query(..., description="Suburb name"),
    limit: int = Query(6, ge=1, le=20),
    db: Any = Depends(get_db_conn_dependency)
):
    """
    Get nearby suburbs based on the selected suburb.
    Returns suggested suburbs that users might also be interested in.
    """
    # Define nearby suburbs mapping (Sydney area)
    nearby_mapping = {
        "Sydney": ["Haymarket", "Surry Hills", "Pyrmont", "Ultimo", "The Rocks", "Darling Harbour"],
        "Ultimo": ["Sydney", "Chippendale", "Pyrmont", "Glebe", "Surry Hills", "Camperdown"],
        "Chippendale": ["Ultimo", "Redfern", "Darlington", "Glebe", "Newtown", "Camperdown"],
        "Surry Hills": ["Sydney", "Darlinghurst", "Paddington", "Redfern", "Moore Park", "Elizabeth Bay"],
        "Redfern": ["Chippendale", "Surry Hills", "Waterloo", "Alexandria", "Eveleigh", "Darlington"],
        "Newtown": ["Erskineville", "Enmore", "Stanmore", "Camperdown", "Marrickville", "St Peters"],
        "Glebe": ["Ultimo", "Forest Lodge", "Annandale", "Camperdown", "Leichhardt", "Pyrmont"],
        "Pyrmont": ["Sydney", "Ultimo", "Glebe", "Balmain", "Rozelle", "Barangaroo"],
        "Waterloo": ["Redfern", "Alexandria", "Zetland", "Rosebery", "Surry Hills", "Moore Park"],
        "Alexandria": ["Waterloo", "Redfern", "Erskineville", "Beaconsfield", "Rosebery", "Mascot"],
        "Zetland": ["Waterloo", "Rosebery", "Kensington", "Alexandria", "Beaconsfield", "Green Square"],
        "Rosebery": ["Zetland", "Waterloo", "Alexandria", "Mascot", "Beaconsfield", "Eastlakes"],
        "Mascot": ["Rosebery", "Alexandria", "Botany", "Eastlakes", "Pagewood", "Wolli Creek"],
        "Randwick": ["Kensington", "Kingsford", "Coogee", "Clovelly", "Centennial Park", "Queens Park"],
        "Kensington": ["Randwick", "Kingsford", "Zetland", "Centennial Park", "Moore Park", "Rosebery"],
        "Kingsford": ["Randwick", "Kensington", "Maroubra", "Daceyville", "Eastlakes", "Coogee"],
        "Maroubra": ["Kingsford", "Pagewood", "Hillsdale", "Malabar", "Coogee", "South Coogee"],
        "Hurstville": ["Penshurst", "Allawah", "Mortdale", "Beverley Park", "Peakhurst", "Oatley"],
        "Burwood": ["Strathfield", "Croydon", "Ashfield", "Five Dock", "Concord", "Homebush"],
        "Campsie": ["Canterbury", "Belmore", "Lakemba", "Ashbury", "Clemton Park", "Earlwood"],
        "Parramatta": ["Westmead", "Harris Park", "North Parramatta", "Rosehill", "Granville", "Rydalmere"],
        "Chatswood": ["Artarmon", "Willoughby", "Lane Cove", "Roseville", "Lindfield", "North Willoughby"],
        "North Sydney": ["Milsons Point", "Kirribilli", "Neutral Bay", "Waverton", "McMahons Point", "Crows Nest"],
        "Bondi": ["Bondi Beach", "North Bondi", "Tamarama", "Bellevue Hill", "Waverley", "Bondi Junction"],
        "Coogee": ["Randwick", "South Coogee", "Clovelly", "Maroubra", "Kingsford", "Bronte"]
    }
    
    try:
        # Get nearby suburbs from mapping
        nearby_suburbs = nearby_mapping.get(suburb, [])[:limit]
        
        if not nearby_suburbs:
            # If no mapping found, return popular suburbs as fallback
            query = """
            SELECT 
                suburb,
                REPLACE(COALESCE(postcode, '0'), '.0', '') as postcode,
                COUNT(DISTINCT listing_id) as property_count
            FROM properties
            WHERE suburb IS NOT NULL AND suburb != %s
              AND is_active = TRUE
            GROUP BY suburb, REPLACE(COALESCE(postcode, '0'), '.0', '')
            ORDER BY property_count DESC
            LIMIT %s
            """
            
            def _db_call():
                with db.cursor() as cur:
                    cur.execute(query, (suburb, limit))
                    results = cur.fetchall()
                    return results
            
            results = await asyncio.to_thread(_db_call)
        else:
            # Get data for nearby suburbs
            placeholders = ','.join(['%s'] * len(nearby_suburbs))
            query = f"""
            SELECT 
                suburb,
                REPLACE(COALESCE(postcode, '0'), '.0', '') as postcode,
                COUNT(DISTINCT listing_id) as property_count
            FROM properties
            WHERE suburb IN ({placeholders})
              AND is_active = TRUE
            GROUP BY suburb, REPLACE(COALESCE(postcode, '0'), '.0', '')
            ORDER BY property_count DESC
            """
            
            def _db_call():
                with db.cursor() as cur:
                    cur.execute(query, nearby_suburbs)
                    results = cur.fetchall()
                    return results
            
            results = await asyncio.to_thread(_db_call)
        
        # Format results
        suggestions = []
        for row in results:
            suburb_name = row[0]
            postcode = row[1]
            count = row[2]
            
            suggestions.append({
                "id": f"{suburb_name}_{postcode}",
                "type": "suburb",
                "name": suburb_name,
                "postcode": postcode,
                "fullName": f"{suburb_name}, NSW, {postcode}",
                "count": count
            })
        
        return success_response(data={
            "current": suburb,
            "nearby": suggestions
        })
        
    except Exception as e:
        logger.error(f"Error getting nearby suburbs: {str(e)}")
        return error_response(f"Failed to get nearby suburbs: {str(e)}")
