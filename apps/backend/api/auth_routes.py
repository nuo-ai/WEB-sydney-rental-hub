# Authentication API routes

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Header
from fastapi.security import OAuth2PasswordBearer
from typing import Any, Dict, Optional
import asyncio
from datetime import datetime, timedelta
import logging

# Import JWT and password utilities
from jose import JWTError, jwt
import os
from models.user_models import (
    UserCreate, UserLogin, UserResponse, Token, TokenData, 
    EmailVerificationRequest, RefreshTokenRequest,
    UserAddressCreate, UserAddressResponse
)
from crud.auth_crud import AuthCRUD
from db import get_db_conn_dependency

logger = logging.getLogger(__name__)

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "a_very_secret_key_for_development")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# OAuth2 scheme for extracting Bearer tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Utility functions
def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token() -> str:
    """Create refresh token"""
    return AuthCRUD.generate_refresh_token()

async def get_current_user(token: str, db_conn: Any) -> UserResponse:
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    
    user = await asyncio.to_thread(AuthCRUD.get_user_by_id, db_conn, token_data.user_id)
    if user is None or user.status != "verified":
        raise credentials_exception
    
    return UserResponse(**user.dict())

async def send_verification_email(email: str, name: str, token: str):
    """Send verification email using the email service"""
    try:
        from services.email_service import email_service
        
        # Use synchronous email service method
        success = email_service.send_verification_email(email, token, name)
        
        if success:
            logger.info(f"✅ Verification email sent successfully to {email}")
        else:
            logger.error(f"❌ Failed to send verification email to {email}")
            
        return success
        
    except Exception as e:
        logger.error(f"Error in send_verification_email: {e}")
        return False

async def send_welcome_email(email: str, name: str):
    """Send welcome email using the email service"""
    try:
        from services.email_service import send_welcome_email as send_welcome
        
        success = await send_welcome(email, name)
        
        if success:
            logger.info(f"✅ Welcome email sent successfully to {email}")
        else:
            logger.error(f"❌ Failed to send welcome email to {email}")
            
        return success
        
    except Exception as e:
        logger.error(f"Error in send_welcome_email: {e}")
        return False

# Authentication endpoints
@router.post("/register", response_model=Dict[str, str])
async def register(
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
    db_conn: Any = Depends(get_db_conn_dependency)
):
    """Register a new user"""
    try:
        # Initialize auth tables if they don't exist
        await asyncio.to_thread(AuthCRUD.init_auth_tables, db_conn)
        
        # Create user
        user = await asyncio.to_thread(AuthCRUD.create_user, db_conn, user_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists with this email"
            )
        
        # Send verification email in background
        background_tasks.add_task(
            send_verification_email, 
            user_data.email,
            user_data.full_name or "User",
            user.verification_token
        )
        
        logger.info(f"User registered successfully: {user_data.email}")
        return {
            "status": "success",
            "message": "Registration successful. Please check your email for verification.",
            "temp_token": user.verification_token  # For development testing
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed. Please try again."
        )

@router.post("/login", response_model=Token)
async def login(
    user_credentials: UserLogin,
    db_conn: Any = Depends(get_db_conn_dependency)
):
    """Login user and return JWT tokens"""
    try:
        # Get user by email
        user = await asyncio.to_thread(AuthCRUD.get_user_by_email, db_conn, user_credentials.email)
        
        if not user or not AuthCRUD.verify_password(user_credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        if user.status != "verified":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please verify your email before logging in"
            )
        
        # Create tokens
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        
        refresh_token = create_refresh_token()
        
        # Save refresh token to database
        await asyncio.to_thread(AuthCRUD.update_refresh_token, db_conn, user.id, refresh_token)
        
        logger.info(f"User logged in successfully: {user.email}")
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed. Please try again."
        )

@router.post("/verify-email")
async def verify_email(
    token: str,
    background_tasks: BackgroundTasks,
    db_conn: Any = Depends(get_db_conn_dependency)
):
    """Verify user email with token"""
    try:
        # Get user info before verification (to send welcome email)
        user = await asyncio.to_thread(AuthCRUD.get_user_by_verification_token, db_conn, token)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired verification token"
            )
        
        # Verify the email
        success = await asyncio.to_thread(AuthCRUD.verify_user_email, db_conn, token)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired verification token"
            )
        
        # Send welcome email in background
        background_tasks.add_task(send_welcome_email, user.email, user.full_name or "User")
        
        return {"status": "success", "message": "Email verified successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Email verification error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Verification failed. Please try again."
        )

@router.post("/resend-verification")
async def resend_verification(
    request: EmailVerificationRequest,
    background_tasks: BackgroundTasks,
    db_conn: Any = Depends(get_db_conn_dependency)
):
    """Resend verification email"""
    try:
        new_token = await asyncio.to_thread(AuthCRUD.resend_verification_email, db_conn, request.email)
        
        if not new_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found or already verified"
            )
        
        # Send verification email in background
        background_tasks.add_task(send_verification_email, request.email, "User", new_token)
        
        return {
            "status": "success",
            "message": "Verification email sent successfully",
            "temp_token": new_token  # For development testing
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Resend verification error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to resend verification. Please try again."
        )

@router.post("/refresh", response_model=Token)
async def refresh_token(
    request: RefreshTokenRequest,
    db_conn: Any = Depends(get_db_conn_dependency)
):
    """Refresh access token using refresh token"""
    try:
        user = await asyncio.to_thread(AuthCRUD.get_user_by_refresh_token, db_conn, request.refresh_token)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Create new tokens
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        
        new_refresh_token = create_refresh_token()
        
        # Update refresh token in database
        await asyncio.to_thread(AuthCRUD.update_refresh_token, db_conn, user.id, new_refresh_token)
        
        return Token(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed. Please try again."
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    token: str = Depends(oauth2_scheme),
    db_conn: Any = Depends(get_db_conn_dependency)
):
    """Get current user profile"""
    try:
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No token provided"
            )
        user = await get_current_user(token, db_conn)
        return user
    except Exception as e:
        logger.error(f"Get user profile error: {e}")
        raise

# User address endpoints
@router.get("/addresses", response_model=list[UserAddressResponse])
async def get_user_addresses(
    token: str = Depends(oauth2_scheme),
    db_conn: Any = Depends(get_db_conn_dependency)
):
    """Get user saved addresses"""
    try:
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No token provided"
            )
        current_user = await get_current_user(token, db_conn)
        addresses = await asyncio.to_thread(AuthCRUD.get_user_addresses, db_conn, current_user.id)
        return [UserAddressResponse(**addr.dict()) for addr in addresses]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get addresses error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get addresses"
        )

@router.post("/addresses", response_model=UserAddressResponse)
async def create_address(
    address_data: UserAddressCreate,
    token: str = Depends(oauth2_scheme),
    db_conn: Any = Depends(get_db_conn_dependency)
):
    """Create a new user address"""
    try:
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No token provided"
            )
        current_user = await get_current_user(token, db_conn)
        address = await asyncio.to_thread(
            AuthCRUD.create_user_address, db_conn, current_user.id, address_data
        )
        
        if not address:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create address"
            )
        
        return UserAddressResponse(**address.dict())
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Create address error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create address"
        )

@router.delete("/addresses/{address_id}")
async def delete_address(
    address_id: int,
    token: str = Depends(oauth2_scheme),
    db_conn: Any = Depends(get_db_conn_dependency)
):
    """Delete a user address"""
    try:
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No token provided"
            )
        current_user = await get_current_user(token, db_conn)
        success = await asyncio.to_thread(
            AuthCRUD.delete_user_address, db_conn, current_user.id, address_id
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found"
            )
        
        return {"status": "success", "message": "Address deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete address error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete address"
        )