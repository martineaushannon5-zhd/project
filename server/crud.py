from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, func, cast, Date
import models, schemas
from datetime import datetime, date

# --- User CRUD ---
async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(models.User).where(models.User.username == username))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    # 此处明文存储密码 123456
    db_user = models.User(
        username=user.username,
        password=user.password,
        real_name=user.real_name,
        role=user.role,
        avatar=user.avatar
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.User).offset(skip).limit(limit))
    return result.scalars().all()

# --- Room & Seat CRUD ---
async def get_rooms(db: AsyncSession):
    result = await db.execute(select(models.Room))
    return result.scalars().all()

async def get_seats_by_room(db: AsyncSession, room_id: int):
    result = await db.execute(select(models.Seat).where(models.Seat.room_id == room_id))
    return result.scalars().all()

# --- Reservation CRUD ---
async def create_reservation(db: AsyncSession, reservation: schemas.ReservationCreate):
    db_res = models.Reservation(**reservation.model_dump())
    db.add(db_res)
    await db.commit()
    await db.refresh(db_res)
    return db_res

async def get_reservations_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.Reservation).where(models.Reservation.user_id == user_id))
    return result.scalars().all()

async def get_dashboard_stats(db: AsyncSession):
    today = datetime.utcnow().date()
    
    # 今日总预约数
    total_res = await db.execute(
        select(func.count(models.Reservation.id)).where(models.Reservation.date == today)
    )
    total_today = total_res.scalar() or 0
    
    # 当前使用中
    active_res = await db.execute(
        select(func.count(models.Reservation.id)).where(
            models.Reservation.date == today,
            models.Reservation.status == "active"
        )
    )
    active_count = active_res.scalar() or 0
    
    # 总座位数
    total_seats_res = await db.execute(select(func.count(models.Seat.id)))
    total_seats = total_seats_res.scalar() or 0
    
    # 简单计算空闲座位（总座位 - 使用中）
    free_seats = max(0, total_seats - active_count)
    
    # 近七日趋势 (模拟或真实)
    # 此处简化，返回一个包含静态趋势数据的结构
    trend = [82, 93, 90, 104, 129, 133, total_today]
    
    return {
        "today_reservations": total_today,
        "active_now": active_count,
        "free_seats": free_seats,
        "trend_data": trend
    }