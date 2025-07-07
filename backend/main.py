from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
# import os # os and load_dotenv are now handled in server.db
import logging
from typing import Any, Dict

# 从我们的模块导入
from api.graphql_schema import schema as gql_schema # Renamed to avoid conflict with strawberry.Schema
import db as db_module # Import the module itself
from db import init_db_pool, close_db_pool, get_db_conn_dependency # Import specific functions

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

# FastAPI 应用实例
app = FastAPI(title="Rental MCP Server", version="1.0.0")

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

# 应用启动时初始化数据库连接池
@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI application startup event triggered...")
    init_db_pool() # Initialize the database pool
    # Check if the pool was successfully initialized by checking the db_pool attribute from the imported db_module
    # init_db_pool itself logs success/failure and includes a test connection.
    if db_module.db_pool is not None: # Check the live attribute from the module
        app.state.db_pool_initialized = True # Use app.state to store custom state
        logger.info("Database pool reported as initialized by init_db_pool (checked via db_module.db_pool).")
    else:
        app.state.db_pool_initialized = False
        logger.error("Database pool (db_module.db_pool) is None after init_db_pool call. Check server.db logs for initialization errors.")


# 应用关闭时关闭数据库连接池
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("FastAPI application shutdown event triggered...")
    close_db_pool() # Close the database pool

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
    graphiql=True # Enable GraphiQL interface, True by default
)
app.include_router(graphql_app_router, prefix="/graphql", tags=["GraphQL"])


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint providing basic server status."""
    return {"message": "Rental MCP Server is running. Access GraphQL at /graphql"}

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

# Note: Ensure that `server.api.graphql_schema.py` uses `info.context.get('sync_db_conn')`
# to retrieve the database connection in its resolvers.
# The `get_db_session` context manager will handle returning the connection to the pool.
