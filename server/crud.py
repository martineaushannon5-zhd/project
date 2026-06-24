from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
import models, schemas
from datetime import datetime, timedelta

# --- User CRUD ---
async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(models.User).where(models.User.username == username))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
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

async def get_room_by_id(db: AsyncSession, room_id: int):
    """根据ID获取自习室信息"""
    result = await db.execute(select(models.Room).where(models.Room.id == room_id))
    return result.scalars().first()

async def get_seats_by_room(db: AsyncSession, room_id: int):
    result = await db.execute(select(models.Seat).where(models.Seat.room_id == room_id))
    return result.scalars().all()

async def create_room(db: AsyncSession, room_data: schemas.RoomBase):
    """创建自习室"""
    db_room = models.Room(**room_data.model_dump())
    db.add(db_room)
    await db.commit()
    await db.refresh(db_room)
    return db_room

async def update_room(db: AsyncSession, room_id: int, room_data: schemas.RoomBase):
    """更新自习室"""
    db_room = await get_room_by_id(db, room_id)
    if not db_room:
        return None
    db_room.name = room_data.name
    db_room.description = room_data.description
    await db.commit()
    await db.refresh(db_room)
    return db_room

async def delete_room(db: AsyncSession, room_id: int):
    """删除自习室"""
    db_room = await get_room_by_id(db, room_id)
    if not db_room:
        return None
    await db.delete(db_room)
    await db.commit()
    return db_room

async def batch_create_seats(db: AsyncSession, room_id: int, prefix: str, count: int, has_power: bool = True):
    """批量生成座位"""
    seats = []
    for i in range(1, count + 1):
        seats.append(models.Seat(room_id=room_id, seat_number=f"{prefix}{i:02d}", has_power=has_power))
    db.add_all(seats)
    await db.commit()
    for seat in seats:
        await db.refresh(seat)
    return seats

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

async def cancel_reservation(db: AsyncSession, reservation_id: int, user_id: int):
    result = await db.execute(
        select(models.Reservation).where(models.Reservation.id == reservation_id, models.Reservation.user_id == user_id)
    )
    reservation = result.scalars().first()
    if not reservation:
        return None
    reservation.status = "cancelled"
    await db.commit()
    await db.refresh(reservation)
    return reservation

async def checkin_reservation(db: AsyncSession, reservation_id: int, user_id: int):
    result = await db.execute(
        select(models.Reservation).where(models.Reservation.id == reservation_id, models.Reservation.user_id == user_id)
    )
    reservation = result.scalars().first()
    if not reservation:
        return None
    reservation.status = "active"
    await db.commit()
    await db.refresh(reservation)
    return reservation

# --- Notice CRUD ---
async def get_notices(db: AsyncSession):
    result = await db.execute(select(models.Notice).order_by(models.Notice.is_pinned.desc(), models.Notice.created_at.desc()))
    return result.scalars().all()

async def create_notice(db: AsyncSession, notice: schemas.NoticeCreate):
    db_notice = models.Notice(**notice.model_dump())
    db.add(db_notice)
    await db.commit()
    await db.refresh(db_notice)
    return db_notice

# --- Feedback CRUD ---
async def get_feedback_list(db: AsyncSession):
    result = await db.execute(select(models.Feedback).order_by(models.Feedback.created_at.desc()))
    return result.scalars().all()

async def create_feedback(db: AsyncSession, feedback: schemas.FeedbackCreate):
    db_feedback = models.Feedback(**feedback.model_dump())
    db.add(db_feedback)
    await db.commit()
    await db.refresh(db_feedback)
    return db_feedback

async def reply_feedback(db: AsyncSession, feedback_id: int, reply: str):
    result = await db.execute(select(models.Feedback).where(models.Feedback.id == feedback_id))
    feedback = result.scalars().first()
    if not feedback:
        return None
    feedback.reply = reply
    feedback.status = "replied"
    await db.commit()
    await db.refresh(feedback)
    return feedback

# --- Dashboard Stats ---
async def get_dashboard_stats(db: AsyncSession):
    """获取后台首页统计数据"""
    today = datetime.utcnow().date()
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]

    total_today_res = await db.execute(select(func.count(models.Reservation.id)).where(models.Reservation.date == today))
    total_today = total_today_res.scalar() or 0

    active_res = await db.execute(select(func.count(models.Reservation.id)).where(models.Reservation.date == today, models.Reservation.status == "active"))
    active_count = active_res.scalar() or 0

    completed_res = await db.execute(select(func.count(models.Reservation.id)).where(models.Reservation.date == today, models.Reservation.status == "completed"))
    completed_count = completed_res.scalar() or 0

    total_rooms = (await db.execute(select(func.count(models.Room.id)))).scalar() or 0
    total_seats = (await db.execute(select(func.count(models.Seat.id)))).scalar() or 0
    occupied_count = (await db.execute(select(func.count(models.Reservation.id)).where(models.Reservation.status.in_(["active", "pending"])))).scalar() or 0
    free_seats = max(0, total_seats - occupied_count)
    seat_usage_rate = round((occupied_count / total_seats * 100) if total_seats else 0, 1)

    trend_data = []
    for day in last_7_days:
        trend_data.append((await db.execute(select(func.count(models.Reservation.id)).where(models.Reservation.date == day))).scalar() or 0)

    room_rows = await db.execute(
        select(models.Room.name, func.count(models.Reservation.id))
        .join(models.Seat, models.Seat.room_id == models.Room.id)
        .join(models.Reservation, models.Reservation.seat_id == models.Seat.id)
        .group_by(models.Room.id)
        .order_by(func.count(models.Reservation.id).desc())
    )
    room_distribution = [{"name": row[0], "value": row[1]} for row in room_rows.all()]

    return {
        "today_reservations": total_today,
        "active_now": active_count,
        "completed_today": completed_count,
        "free_seats": free_seats,
        "total_rooms": total_rooms,
        "total_seats": total_seats,
        "seat_usage_rate": seat_usage_rate,
        "trend_labels": [day.strftime("%m-%d") for day in last_7_days],
        "trend_data": trend_data,
        "room_distribution": room_distribution,
    }
