"""
用户偏好设置API路由
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional, Dict, Any, List
from models.user_models import UserPreferences, UserPreferencesResponse
from crud.auth_crud import AuthCRUD
from db import get_db_conn_dependency

router = APIRouter(prefix="/api/user/preferences", tags=["User Preferences"])

@router.get("/", response_model=UserPreferencesResponse)
async def get_user_preferences(
    token: str = Query(..., description="用户认证token"),
    db_conn: Any = Depends(get_db_conn_dependency)
):
    """
    获取用户偏好设置
    """
    try:
        # 通过token获取用户信息
        user = await AuthCRUD.get_user_by_refresh_token(db_conn, token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的认证token"
            )
        
        # 获取用户的偏好设置
        preferences = AuthCRUD.get_user_preferences(db_conn, user.id)
        
        if not preferences:
            # 如果没有偏好设置，返回默认值
            preferences = UserPreferences(
                preferred_suburbs=[],
                min_price=0,
                max_price=1000,
                min_bedrooms=1,
                max_bedrooms=3,
                preferred_property_types=[],
                is_furnished_only=False,
                has_parking=False,
                has_air_conditioning=False,
                allows_pets=False
            )
        
        return UserPreferencesResponse(
            data=preferences,
            message="获取用户偏好设置成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取用户偏好设置失败: {str(e)}"
        )

@router.post("/", response_model=UserPreferencesResponse)
async def update_user_preferences(
    preferences: UserPreferences,
    token: str = Query(..., description="用户认证token"),
    db_conn: Any = Depends(get_db_conn_dependency)
):
    """
    更新用户偏好设置
    """
    try:
        # 通过token获取用户信息
        user = await AuthCRUD.get_user_by_refresh_token(db_conn, token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的认证token"
            )
        
        # 更新用户偏好设置
        success = AuthCRUD.update_user_preferences(db_conn, user.id, preferences)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="更新用户偏好设置失败"
            )
        
        return UserPreferencesResponse(
            data=preferences,
            message="更新用户偏好设置成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新用户偏好设置失败: {str(e)}"
        )
