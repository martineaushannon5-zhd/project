from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from schemas import UserCreate, UserResponse
from crud import get_user_by_username, create_user, get_users
from database import get_db

router = APIRouter(prefix="/api/users", tags=["用户模块"])

@router.post("/login")
async def login(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """用户登录 (测试用，明文验证)"""
    db_user = await get_user_by_username(db, user.username)
    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    return {"message": "登录成功", "user": {"id": db_user.id, "username": db_user.username, "role": db_user.role}}

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """用户注册"""
    db_user = await get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    return await create_user(db, user)

@router.get("/", response_model=List[UserResponse])
async def get_all_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """获取用户列表"""
    return await get_users(db, skip=skip, limit=limit)