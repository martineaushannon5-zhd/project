from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
import models, schemas

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