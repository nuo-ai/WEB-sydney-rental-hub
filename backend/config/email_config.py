# Email service configuration for Sydney Rental Hub

import os
from typing import Optional, Dict, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class EmailConfig:
    """Email service configuration"""
    # Required fields (no defaults)
    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    from_email: str
    from_name: str
    
    # Optional fields (with defaults)
    smtp_use_tls: bool = True
    smtp_use_ssl: bool = False
    development_mode: bool = True
    log_emails: bool = True
    provider: str = "smtp"  # smtp, sendgrid, mailgun, aws_ses
    sendgrid_api_key: Optional[str] = None
    mailgun_api_key: Optional[str] = None
    mailgun_domain: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: Optional[str] = None

def get_email_config() -> EmailConfig:
    """Get email configuration from environment variables"""
    
    # Determine if we're in development mode
    development_mode = os.getenv("ENVIRONMENT", "development").lower() != "production"
    
    # Get provider preference (smtp, sendgrid, mailgun, aws_ses)
    provider = os.getenv("EMAIL_PROVIDER", "smtp").lower()
    
    config = EmailConfig(
        # SMTP Configuration (fallback and default)
        smtp_host=os.getenv("SMTP_HOST", "smtp.gmail.com"),
        smtp_port=int(os.getenv("SMTP_PORT", "587")),
        smtp_username=os.getenv("SMTP_USERNAME", ""),
        smtp_password=os.getenv("SMTP_PASSWORD", ""),
        smtp_use_tls=os.getenv("SMTP_USE_TLS", "true").lower() == "true",
        smtp_use_ssl=os.getenv("SMTP_USE_SSL", "false").lower() == "true",
        
        # Email settings
        from_email=os.getenv("FROM_EMAIL", "noreply@sydneyrentalhub.com"),
        from_name=os.getenv("FROM_NAME", "Sydney Rental Hub"),
        
        # Development settings
        development_mode=development_mode,
        log_emails=os.getenv("LOG_EMAILS", "true").lower() == "true",
        
        # Provider settings
        provider=provider,
        
        # SendGrid
        sendgrid_api_key=os.getenv("SENDGRID_API_KEY"),
        
        # Mailgun
        mailgun_api_key=os.getenv("MAILGUN_API_KEY"),
        mailgun_domain=os.getenv("MAILGUN_DOMAIN"),
        
        # AWS SES
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_region=os.getenv("AWS_REGION", "us-east-1"),
    )
    
    # Log configuration (without sensitive data)
    logger.info(f"Email service configured:")
    logger.info(f"  - Provider: {config.provider}")
    logger.info(f"  - Development mode: {config.development_mode}")
    logger.info(f"  - From email: {config.from_email}")
    logger.info(f"  - SMTP host: {config.smtp_host}:{config.smtp_port}")
    logger.info(f"  - Log emails: {config.log_emails}")
    
    return config

def validate_email_config(config: EmailConfig) -> bool:
    """Validate email configuration based on provider"""
    
    if config.provider == "sendgrid":
        if not config.sendgrid_api_key:
            logger.warning("SendGrid API key not configured, falling back to SMTP")
            return False
    
    elif config.provider == "mailgun":
        if not config.mailgun_api_key or not config.mailgun_domain:
            logger.warning("Mailgun configuration incomplete, falling back to SMTP")
            return False
    
    elif config.provider == "aws_ses":
        if not config.aws_access_key_id or not config.aws_secret_access_key:
            logger.warning("AWS SES configuration incomplete, falling back to SMTP")
            return False
    
    elif config.provider == "smtp":
        if not config.smtp_username or not config.smtp_password:
            if not config.development_mode:
                logger.warning("SMTP configuration incomplete for production")
                return False
            else:
                logger.info("SMTP credentials not configured, using development mode")
    
    return True

# Email template configurations
EMAIL_TEMPLATES = {
    "verification": {
        "subject": "Verify your Sydney Rental Hub account",
        "template_path": "templates/email_verification.html"
    },
    "welcome": {
        "subject": "Welcome to Sydney Rental Hub!",
        "template_path": "templates/email_welcome.html"
    },
    "password_reset": {
        "subject": "Reset your Sydney Rental Hub password",
        "template_path": "templates/email_password_reset.html"
    }
}

# URL configurations
def get_verification_url(token: str, config: EmailConfig) -> str:
    """Generate verification URL based on environment"""
    base_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    return f"{base_url}/verify-email?token={token}"

def get_app_url(config: EmailConfig) -> str:
    """Get application URL based on environment"""
    return os.getenv("FRONTEND_URL", "http://localhost:5173")