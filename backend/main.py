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
from redis import asyncio as aioredis
from pydantic import BaseModel, Field, validator
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from jose import JWTError, jwt
from datetime import datetime, timedelta, date
# import os # os and load_dotenv are now handled in server.db
import logging
from typing import Any, Dict, List, Optional, TypeVar, Generic
import json
import asyncio
import os
from contextlib import asynccontextmanager
import math
import base64

# 从我们的模块导入
from .api.graphql_schema import schema as gql_schema # Renamed to avoid conflict with strawberry.Schema
from . import db as db_module # Import the module itself
from .db import init_db_pool, close_db_pool, get_db_conn_dependency # Import specific functions

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
# We set config_filename="" to prevent slowapi from trying to read the .env file,
# which causes encoding issues on Windows. We load .env manually elsewhere.
limiter = Limiter(key_func=get_remote_address, config_filename="")

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
        username: Optional[str] = payload.get("sub")
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
async def paginate_query(db_conn: Any, query: str, count_query: str, params: tuple, pagination: PaginationParams) -> tuple[List[Dict], PaginationInfo]:
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
    return [dict(zip(columns, row)) for row in items], pagination_info


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

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("FastAPI application startup event triggered...")
    init_db_pool()
    if db_module.db_pool is not None:
        app.state.db_pool_initialized = True
        logger.info("Database pool reported as initialized.")
    else:
        app.state.db_pool_initialized = False
        logger.error("Database pool is None after init.")
    
    # Initialize Redis Cache
    # Assuming Redis is running on localhost. In production, use env variables.
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    logger.info("FastAPI Cache initialized with Redis backend.")

    yield
    # Shutdown
    logger.info("FastAPI application shutdown event triggered...")
    close_db_pool()

# FastAPI 应用实例
app = FastAPI(title="Rental MCP Server", version="1.0.0", lifespan=lifespan)
app.state.limiter = limiter

# CORS Middleware Configuration
origins = [
    "http://localhost",
    "http://localhost:5500", # The origin for our frontend dev server
    "http://127.0.0.1:5500",
    "http://localhost:8080", # 新增：支持Python简易服务器端口
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
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

# 创建 GraphQL 路由器，并使用自定义上下文
graphql_app_router = GraphQLRouter(
    gql_schema, # Use the imported schema
    context_getter=get_graphql_context, # Pass our custom context getter
    graphql_ide="graphiql" # Enable GraphiQL interface
)
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
from .celery_config import celery_app
from .tasks import debug_task, example_db_task
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


@app.get("/api/properties/", tags=["Properties"], response_model=APIResponse[List[Dict]])
@cache(expire=900) # Cache for 15 minutes
async def get_properties(pagination: PaginationParams = Depends(), db: Any = Depends(get_db_conn_dependency)):
    """
    Get a paginated list of properties.
    Supports both page-based and cursor-based pagination.
    """
    # For now, we will just paginate all properties. Filtering can be added later.
    base_query = "SELECT * FROM properties"
    count_query = "SELECT COUNT(*) FROM properties"
    
    # Simple cursor implementation based on listing_id
    # A more robust implementation would handle sorting
    if pagination.cursor:
        try:
            cursor_val = int(decode_cursor(pagination.cursor))
            query = f"{base_query} WHERE listing_id > %s ORDER BY listing_id ASC"
            params = (cursor_val,)
        except (ValueError, TypeError):
            raise HTTPException(status_code=400, detail="Invalid cursor")

        def _db_call_cursor():
            with db.cursor() as cur:
                # Fetch one more than page_size to check for has_next
                cur.execute(f"{query} LIMIT %s", params + (pagination.page_size + 1,))
                items = cur.fetchall()
                columns = [desc[0] for desc in cur.description]
                return items, columns
        
        items, columns = await asyncio.to_thread(_db_call_cursor)
        
        has_next = len(items) > pagination.page_size
        if has_next:
            items = items[:-1] # remove extra item
        
        items_as_dicts = [dict(zip(columns, row)) for row in items]
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
        query = f"{base_query} ORDER BY listing_id ASC"
        items, pagination_info = await paginate_query(db, query, count_query, (), pagination)
        return success_response(data=items, pagination=pagination_info)
