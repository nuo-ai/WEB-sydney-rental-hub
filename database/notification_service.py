from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import os
import json
from datetime import datetime
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart

# 处理 dotenv 导入
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    logging.warning("python-dotenv not available.")
    DOTENV_AVAILABLE = False
    def load_dotenv(*args, **kwargs):
        pass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)
    logger.info(f"Successfully loaded .env file from: {dotenv_path}")
else:
    load_dotenv(override=True)
    logger.warning(f".env file not found at {dotenv_path}. Using system environment.")

# FastAPI应用实例
app = FastAPI(
    title="Sydney Rental Hub - Notification Service",
    description="处理新房源通知的微服务",
    version="1.0.0"
)

# 邮件配置
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USERNAME)

# 通知配置
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
NOTIFICATION_ENABLED = os.getenv("NOTIFICATION_ENABLED", "true").lower() == "true"

class PropertyListing(BaseModel):
    """房源信息模型"""
    listing_id: int
    address: str
    suburb: str
    rent_pw: int
    bedrooms: int
    property_type: str
    property_url: str

class NewListingNotification(BaseModel):
    """新房源通知模型"""
    event: str
    timestamp: str
    count: int
    listings: List[PropertyListing]

class NotificationService:
    """通知服务类"""
    
    def __init__(self):
        self.is_email_configured = bool(SMTP_USERNAME and SMTP_PASSWORD)
        if not self.is_email_configured:
            logger.warning("Email configuration not complete. Email notifications will be disabled.")
            
    def format_property_html(self, listing: PropertyListing) -> str:
        """格式化房源信息为HTML"""
        return f"""
        <div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px;">
            <h3 style="color: #2563eb; margin: 0 0 10px 0;">
                <a href="{listing.property_url}" target="_blank" style="text-decoration: none; color: #2563eb;">
                    {listing.address}
                </a>
            </h3>
            <p style="margin: 5px 0;"><strong>区域:</strong> {listing.suburb}</p>
            <p style="margin: 5px 0;"><strong>周租金:</strong> ${listing.rent_pw}</p>
            <p style="margin: 5px 0;"><strong>卧室:</strong> {listing.bedrooms}间</p>
            <p style="margin: 5px 0;"><strong>房型:</strong> {listing.property_type}</p>
            <p style="margin: 10px 0 0 0;">
                <a href="{listing.property_url}" target="_blank" 
                   style="background-color: #2563eb; color: white; padding: 8px 16px; 
                          text-decoration: none; border-radius: 4px; display: inline-block;">
                    查看详情
                </a>
            </p>
        </div>
        """
        
    def create_notification_email(self, notification: NewListingNotification) -> str:
        """创建通知邮件的HTML内容"""
        timestamp = datetime.fromisoformat(notification.timestamp.replace('Z', '+00:00'))
        formatted_time = timestamp.strftime('%Y年%m月%d日 %H:%M:%S')
        
        properties_html = "".join([
            self.format_property_html(listing) for listing in notification.listings
        ])
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>新房源通知 - Sydney Rental Hub</title>
        </head>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background-color: #2563eb; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0;">
                <h1 style="margin: 0; font-size: 24px;">🏠 Sydney Rental Hub</h1>
                <p style="margin: 10px 0 0 0; font-size: 16px;">新房源通知</p>
            </div>
            
            <div style="background-color: #f8fafc; padding: 20px; border: 1px solid #e2e8f0; border-top: none;">
                <h2 style="color: #1e40af; margin: 0 0 15px 0;">
                    🎉 发现 {notification.count} 个新房源！
                </h2>
                <p style="color: #64748b; margin: 0 0 20px 0;">
                    更新时间: {formatted_time}
                </p>
                
                <div style="background-color: white; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                    {properties_html}
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="https://your-domain.com" target="_blank" 
                       style="background-color: #10b981; color: white; padding: 12px 24px; 
                              text-decoration: none; border-radius: 6px; font-weight: bold;">
                        访问完整平台
                    </a>
                </div>
            </div>
            
            <div style="background-color: #f1f5f9; padding: 15px; text-align: center; 
                        border: 1px solid #e2e8f0; border-top: none; border-radius: 0 0 8px 8px;">
                <p style="margin: 0; color: #64748b; font-size: 14px;">
                    Sydney Rental Hub - 专为中国学生打造的悉尼租房平台
                </p>
            </div>
        </body>
        </html>
        """
        
        return html_content
        
    async def send_email_notification(self, notification: NewListingNotification):
        """发送邮件通知"""
        if not self.is_email_configured or not ADMIN_EMAIL:
            logger.warning("Email configuration incomplete, skipping email notification")
            return False
            
        try:
            # 创建邮件
            msg = MimeMultipart('alternative')
            msg['Subject'] = f"🏠 Sydney Rental Hub - 发现{notification.count}个新房源"
            msg['From'] = FROM_EMAIL
            msg['To'] = ADMIN_EMAIL
            
            # 添加HTML内容
            html_content = self.create_notification_email(notification)
            html_part = MimeText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # 发送邮件
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.send_message(msg)
                
            logger.info(f"Successfully sent email notification for {notification.count} new listings")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")
            return False
            
    async def log_notification(self, notification: NewListingNotification):
        """记录通知到日志文件"""
        log_file = os.path.join(os.path.dirname(__file__), 'notifications.log')
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                log_entry = {
                    'timestamp': notification.timestamp,
                    'event': notification.event,
                    'count': notification.count,
                    'listings': [listing.dict() for listing in notification.listings]
                }
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
                
            logger.info(f"Logged notification for {notification.count} new listings")
            return True
            
        except Exception as e:
            logger.error(f"Failed to log notification: {e}")
            return False

# 创建通知服务实例
notification_service = NotificationService()

@app.get("/")
async def root():
    """健康检查端点"""
    return {
        "service": "Sydney Rental Hub Notification Service",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "email_configured": notification_service.is_email_configured
    }

@app.get("/health")
async def health_check():
    """详细的健康检查"""
    return {
        "status": "healthy",
        "services": {
            "email": notification_service.is_email_configured,
            "logging": True
        },
        "config": {
            "notification_enabled": NOTIFICATION_ENABLED,
            "admin_email_configured": bool(ADMIN_EMAIL),
            "smtp_server": SMTP_SERVER
        }
    }

@app.post("/webhook/new-listings")
async def receive_new_listings(
    notification: NewListingNotification,
    background_tasks: BackgroundTasks
):
    """接收新房源通知的Webhook端点"""
    logger.info(f"Received new listings notification: {notification.count} properties")
    
    if not NOTIFICATION_ENABLED:
        logger.info("Notifications are disabled, skipping processing")
        return {"status": "disabled", "message": "Notifications are currently disabled"}
    
    # 验证通知数据
    if notification.event != "new_listings":
        raise HTTPException(status_code=400, detail="Invalid event type")
        
    if notification.count != len(notification.listings):
        raise HTTPException(status_code=400, detail="Count mismatch with listings array")
    
    # 在后台处理通知
    background_tasks.add_task(notification_service.log_notification, notification)
    
    if notification_service.is_email_configured and ADMIN_EMAIL:
        background_tasks.add_task(notification_service.send_email_notification, notification)
    
    return {
        "status": "received",
        "event": notification.event,
        "count": notification.count,
        "timestamp": notification.timestamp,
        "processing": "background"
    }

@app.post("/test/notification")
async def test_notification(background_tasks: BackgroundTasks):
    """测试通知功能的端点"""
    # 创建测试数据
    test_notification = NewListingNotification(
        event="new_listings",
        timestamp=datetime.now().isoformat(),
        count=2,
        listings=[
            PropertyListing(
                listing_id=12345,
                address="123 Test Street",
                suburb="Sydney",
                rent_pw=500,
                bedrooms=2,
                property_type="Apartment",
                property_url="https://example.com/property/12345"
            ),
            PropertyListing(
                listing_id=12346,
                address="456 Demo Avenue",
                suburb="Redfern",
                rent_pw=600,
                bedrooms=1,
                property_type="Studio",
                property_url="https://example.com/property/12346"
            )
        ]
    )
    
    # 处理测试通知
    background_tasks.add_task(notification_service.log_notification, test_notification)
    
    if notification_service.is_email_configured and ADMIN_EMAIL:
        background_tasks.add_task(notification_service.send_email_notification, test_notification)
        
    return {
        "status": "test_sent",
        "message": "Test notification queued for processing",
        "test_data": test_notification.dict()
    }

if __name__ == "__main__":
    import uvicorn
    
    # 获取配置
    host = os.getenv("NOTIFICATION_HOST", "0.0.0.0")
    port = int(os.getenv("NOTIFICATION_PORT", "8001"))
    
    logger.info(f"Starting notification service on {host}:{port}")
    
    uvicorn.run(
        "notification_service:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )
