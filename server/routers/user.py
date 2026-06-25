from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from schemas import UserCreate, UserUpdate, UserResponse, FeedbackCreate, FeedbackResponse, FeedbackReply
from crud import (
    get_user_by_id, get_user_by_username, create_user, get_users, update_user, delete_user,
    create_feedback, get_feedback_list, reply_feedback, delete_feedback
)
from database import get_db

router = APIRouter(prefix="/api/users", tags=["用户模块"])

@router.post("/login")
async def login(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """用户登录（测试用，明文验证）"""
    db_user = await get_user_by_username(db, user.username)
    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    return {"message": "登录成功", "user": {"id": db_user.id, "username": db_user.username, "role": db_user.role, "real_name": db_user.real_name}}

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """用户注册"""
    db_user = await get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    return await create_user(db, user)

@router.post("/", response_model=UserResponse)
async def create_user_by_admin(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """管理员新增用户"""
    db_user = await get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    return await create_user(db, user)

@router.get("/", response_model=List[UserResponse])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    keyword: Optional[str] = None,
    role: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """获取用户列表"""
    return await get_users(db, skip=skip, limit=limit, keyword=keyword, role=role)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user_endpoint(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    """更新用户信息"""
    db_user = await get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")

    if user.username and user.username != db_user.username:
        existed_user = await get_user_by_username(db, user.username)
        if existed_user:
            raise HTTPException(status_code=400, detail="用户名已存在")

    updated_user = await update_user(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return updated_user

@router.get("/feedback", response_model=List[FeedbackResponse])
async def feedback_list(user_id: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    """获取反馈列表"""
    return await get_feedback_list(db, user_id=user_id)

@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(feedback: FeedbackCreate, db: AsyncSession = Depends(get_db)):
    """提交反馈"""
    return await create_feedback(db, feedback)

@router.post("/feedback/{feedback_id}/reply", response_model=FeedbackResponse)
async def reply_to_feedback(feedback_id: int, reply: FeedbackReply, db: AsyncSession = Depends(get_db)):
    """回复反馈"""
    result = await reply_feedback(db, feedback_id, reply.reply)
    if not result:
        raise HTTPException(status_code=404, detail="反馈不存在")
    return result

@router.delete("/feedback/{feedback_id}")
async def delete_feedback_endpoint(feedback_id: int, db: AsyncSession = Depends(get_db)):
    """删除反馈"""
    result = await delete_feedback(db, feedback_id)
    if not result:
        raise HTTPException(status_code=404, detail="反馈不存在")
    return {"message": "删除成功"}

@router.delete("/{user_id}")
async def delete_user_endpoint(user_id: int, db: AsyncSession = Depends(get_db)):
    """删除用户"""
    deleted_user = await delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"message": "删除成功"}
