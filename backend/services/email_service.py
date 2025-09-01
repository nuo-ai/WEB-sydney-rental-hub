# Email Service for Sydney Rental Hub

import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class EmailService:
    """Email service with development and production modes"""
    
    def __init__(self):
        # Check if we're in development or production mode
        self.dev_mode = os.getenv("EMAIL_DEV_MODE", "true").lower() == "true"
        
        # SMTP configuration for production
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@sydneyrentalhub.com")
        self.from_name = os.getenv("FROM_NAME", "Sydney Rental Hub")
        
        # Application URLs
        self.app_url = os.getenv("APP_URL", "http://localhost:5173")
        
    def send_verification_email(self, to_email: str, verification_token: str, user_name: Optional[str] = None) -> bool:
        """Send email verification email"""
        
        verification_url = f"{self.app_url}/verify-email?token={verification_token}"
        
        # Create email content
        subject = "Verify Your Email - Sydney Rental Hub"
        
        # HTML email template
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 50px auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    background-color: #FF5824;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                    margin: -20px -20px 20px -20px;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 24px;
                }}
                .content {{
                    padding: 20px 0;
                }}
                .button {{
                    display: inline-block;
                    padding: 12px 30px;
                    background-color: #FF5824;
                    color: white;
                    text-decoration: none;
                    border-radius: 6px;
                    font-weight: bold;
                    margin: 20px 0;
                }}
                .button:hover {{
                    background-color: #E64100;
                }}
                .code-box {{
                    background-color: #f8f9fa;
                    border: 1px solid #dee2e6;
                    padding: 15px;
                    border-radius: 5px;
                    font-family: monospace;
                    font-size: 16px;
                    color: #495057;
                    margin: 20px 0;
                    word-break: break-all;
                }}
                .footer {{
                    text-align: center;
                    color: #666;
                    font-size: 12px;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #eee;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🏠 Sydney Rental Hub</h1>
                </div>
                <div class="content">
                    <h2>Welcome{' ' + user_name if user_name else ''}!</h2>
                    <p>Thank you for registering with Sydney Rental Hub. To complete your registration and start exploring the best rental properties in Sydney, please verify your email address.</p>
                    
                    <div style="text-align: center;">
                        <a href="{verification_url}" class="button">Verify Email Address</a>
                    </div>
                    
                    <p>Or copy and paste this link into your browser:</p>
                    <div class="code-box">
                        {verification_url}
                    </div>
                    
                    <p><strong>This verification link will expire in 24 hours.</strong></p>
                    
                    <p>If you didn't create an account with Sydney Rental Hub, you can safely ignore this email.</p>
                </div>
                <div class="footer">
                    <p>© 2025 Sydney Rental Hub. All rights reserved.</p>
                    <p>This is an automated email, please do not reply.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version
        text_content = f"""
        Welcome to Sydney Rental Hub!
        
        Thank you for registering. To complete your registration, please verify your email address by clicking the link below:
        
        {verification_url}
        
        This verification link will expire in 24 hours.
        
        If you didn't create an account with Sydney Rental Hub, you can safely ignore this email.
        
        Best regards,
        Sydney Rental Hub Team
        """
        
        return self._send_email(to_email, subject, text_content, html_content, verification_token)
    
    def send_password_reset_email(self, to_email: str, reset_token: str, user_name: Optional[str] = None) -> bool:
        """Send password reset email"""
        
        reset_url = f"{self.app_url}/reset-password?token={reset_token}"
        
        subject = "Password Reset Request - Sydney Rental Hub"
        
        # HTML email template
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 50px auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    background-color: #FF5824;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                    margin: -20px -20px 20px -20px;
                }}
                .button {{
                    display: inline-block;
                    padding: 12px 30px;
                    background-color: #FF5824;
                    color: white;
                    text-decoration: none;
                    border-radius: 6px;
                    font-weight: bold;
                    margin: 20px 0;
                }}
                .warning {{
                    background-color: #fff3cd;
                    border: 1px solid #ffc107;
                    padding: 10px;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔒 Password Reset Request</h1>
                </div>
                <div class="content">
                    <h2>Hello{' ' + user_name if user_name else ''}!</h2>
                    <p>We received a request to reset the password for your Sydney Rental Hub account.</p>
                    
                    <div style="text-align: center;">
                        <a href="{reset_url}" class="button">Reset Password</a>
                    </div>
                    
                    <div class="warning">
                        <strong>⚠️ This link will expire in 1 hour for security reasons.</strong>
                    </div>
                    
                    <p>If you didn't request a password reset, please ignore this email. Your password won't be changed.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Password Reset Request
        
        We received a request to reset the password for your Sydney Rental Hub account.
        
        Click here to reset your password: {reset_url}
        
        This link will expire in 1 hour.
        
        If you didn't request this, please ignore this email.
        """
        
        return self._send_email(to_email, subject, text_content, html_content)
    
    def _send_email(self, to_email: str, subject: str, text_content: str, html_content: str, 
                   verification_token: Optional[str] = None) -> bool:
        """Internal method to send email"""
        
        if self.dev_mode:
            # Development mode: just log the email details
            logger.info("=" * 60)
            logger.info("📧 EMAIL (DEV MODE)")
            logger.info("=" * 60)
            logger.info(f"TO: {to_email}")
            logger.info(f"SUBJECT: {subject}")
            logger.info("-" * 60)
            if verification_token:
                logger.info(f"🔑 VERIFICATION TOKEN: {verification_token}")
                logger.info(f"📎 Verify URL: {self.app_url}/verify-email?token={verification_token}")
            logger.info("-" * 60)
            logger.info("EMAIL CONTENT (Text):")
            logger.info(text_content)
            logger.info("=" * 60)
            
            # Also print to console for easy access during development
            print(f"\n{'='*60}")
            print(f"[EMAIL] DEV MODE - EMAIL VERIFICATION")
            print(f"{'='*60}")
            print(f"Email would be sent to: {to_email}")
            if verification_token:
                print(f"Verification Token: {verification_token}")
                print(f"Verification URL: {self.app_url}/verify-email?token={verification_token}")
            print(f"{'='*60}\n")
            
            return True
        
        else:
            # Production mode: send actual email
            try:
                # Create message
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = f"{self.from_name} <{self.from_email}>"
                msg['To'] = to_email
                
                # Add text and HTML parts
                part1 = MIMEText(text_content, 'plain')
                part2 = MIMEText(html_content, 'html')
                
                msg.attach(part1)
                msg.attach(part2)
                
                # Send email via SMTP
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    server.starttls()
                    if self.smtp_user and self.smtp_password:
                        server.login(self.smtp_user, self.smtp_password)
                    server.send_message(msg)
                
                logger.info(f"Email sent successfully to {to_email}")
                return True
                
            except Exception as e:
                logger.error(f"Failed to send email to {to_email}: {str(e)}")
                return False

# Global email service instance
email_service = EmailService()