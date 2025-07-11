from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from pydantic import BaseModel
# import os # os and load_dotenv are now handled in server.db
import logging
from typing import Any, Dict, List, Optional
import json
import asyncio
import os
from contextlib import asynccontextmanager

# 从我们的模块导入
from .api.graphql_schema import schema as gql_schema # Renamed to avoid conflict with strawberry.Schema
from . import db as db_module # Import the module itself
from .db import init_db_pool, close_db_pool, get_db_conn_dependency # Import specific functions

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
    yield
    # Shutdown
    logger.info("FastAPI application shutdown event triggered...")
    close_db_pool()

# FastAPI 应用实例
app = FastAPI(title="Rental MCP Server", version="1.0.0", lifespan=lifespan)

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
    id: int
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

@app.get("/api/properties/latest", tags=["Properties"])
async def get_latest_properties(db: Any = Depends(get_db_conn_dependency)):
    """
    Get the latest properties with status 'new' or 'updated' in the last 24 hours.
    """
    try:
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT *
                FROM properties
                WHERE status IN ('new', 'updated')
                  AND status_changed_at >= NOW() - INTERVAL '24 hours'
                ORDER BY status_changed_at DESC;
            """)
            properties = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in properties]
    except Exception as e:
        logger.error(f"Error fetching latest properties: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch latest properties")
