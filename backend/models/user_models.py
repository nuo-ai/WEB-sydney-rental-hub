# User models for authentication system

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from enum import Enum

class UserStatus(str, Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    SUSPENDED = "suspended"

class UserBase(BaseModel):
    """Base user model with common fields"""
    email: EmailStr = Field(..., description="用户邮箱")
    full_name: Optional[str] = Field(None, max_length=100, description="用户全名")

class UserCreate(UserBase):
    """User creation model"""
    password: str = Field(..., min_length=8, max_length=128, description="用户密码")
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('密码至少8个字符')
        if not any(c.isdigit() for c in v):
            raise ValueError('密码必须包含至少一个数字')
        if not any(c.isalpha() for c in v):
            raise ValueError('密码必须包含至少一个字母')
        return v

class UserLogin(BaseModel):
    """User login model"""
    email: EmailStr = Field(..., description="用户邮箱")
    password: str = Field(..., description="用户密码")

class UserResponse(UserBase):
    """User response model (excluding sensitive fields)"""
    id: int
    status: UserStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserInDB(UserResponse):
    """User model as stored in database (including sensitive fields)"""
    hashed_password: str
    verification_token: Optional[str] = None
    verification_token_expires: Optional[datetime] = None
    refresh_token: Optional[str] = None

class Token(BaseModel):
    """Token response model"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds

class TokenData(BaseModel):
    """Token data for JWT payload"""
    user_id: Optional[int] = None
    email: Optional[str] = None

class EmailVerificationRequest(BaseModel):
    """Email verification request model"""
    email: EmailStr = Field(..., description="用户邮箱")

class RefreshTokenRequest(BaseModel):
    """Refresh token request model"""
    refresh_token: str = Field(..., description="刷新令牌")

class UserAddress(BaseModel):
    """User saved address model"""
    id: Optional[int] = None
    user_id: int
    address: str = Field(..., max_length=500, description="完整地址")
    label: str = Field(..., max_length=50, description="地址标签（Home/Work/School/Other）")
    place_id: Optional[str] = Field(None, max_length=255, description="Google Places ID")
    latitude: float = Field(..., ge=-90, le=90, description="纬度")
    longitude: float = Field(..., ge=-180, le=180, description="经度")
    created_at: Optional[datetime] = None

class UserAddressCreate(BaseModel):
    """Create user address model"""
    address: str = Field(..., max_length=500, description="完整地址")
    label: str = Field(..., max_length=50, description="地址标签")
    place_id: Optional[str] = Field(None, max_length=255, description="Google Places ID")
    latitude: float = Field(..., ge=-90, le=90, description="纬度")
    longitude: float = Field(..., ge=-180, le=180, description="经度")
    
    @validator('label')
    def validate_label(cls, v):
        valid_labels = ['Home', 'Work', 'School', 'Other']
        if v not in valid_labels:
            raise ValueError(f'地址标签必须是: {", ".join(valid_labels)}')
        return v

class UserAddressResponse(BaseModel):
    """User address response model"""
    id: int
    address: str
    label: str
    place_id: Optional[str]
    latitude: float
    longitude: float
    created_at: datetime
    
    class Config:
        from_attributes = True