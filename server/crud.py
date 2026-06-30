from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, or_
import models, schemas
from datetime import datetime, timedelta
from fastapi import HTTPException

ACTIVE_RESERVATION_STATUSES = ("pending", "active")

# --- User CRUD ---
async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(models.User).where(models.User.username == username))
    return result.scalars().first()

async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
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

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100, keyword: str | None = None, role: str | None = None):
    stmt = select(models.User)
    if keyword:
        stmt = stmt.where(
            or_(
                models.User.username.like(f"%{keyword}%"),
                models.User.real_name.like(f"%{keyword}%")
            )
        )
    if role:
        stmt = stmt.where(models.User.role == role)
    stmt = stmt.order_by(models.User.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def update_user(db: AsyncSession, user_id: int, user_data: schemas.UserUpdate):
    db_user = await get_user_by_id(db, user_id)
    if not db_user:
        return None

    payload = user_data.model_dump(exclude_unset=True)
    for field, value in payload.items():
        setattr(db_user, field, value)

    await db.commit()
    await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, user_id: int):
    db_user = await get_user_by_id(db, user_id)
    if not db_user:
        return None

    await db.delete(db_user)
    await db.commit()
    return db_user

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

async def get_seat_by_id(db: AsyncSession, seat_id: int):
    result = await db.execute(select(models.Seat).where(models.Seat.id == seat_id))
    return result.scalars().first()

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
    today = datetime.now().date()
    if reservation.date < today:
        raise HTTPException(status_code=400, detail="不能预约过去的日期")

    if reservation.start_time >= reservation.end_time:
        raise HTTPException(status_code=400, detail="结束时间必须晚于开始时间")

    db_user = await get_user_by_id(db, reservation.user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="预约用户不存在")

    db_seat = await get_seat_by_id(db, reservation.seat_id)
    if not db_seat:
        raise HTTPException(status_code=404, detail="座位不存在")
    if db_seat.status != 1:
        raise HTTPException(status_code=400, detail="该座位当前不可预约")

    overlapping_seat_reservation = await db.execute(
        select(models.Reservation).where(
            models.Reservation.seat_id == reservation.seat_id,
            models.Reservation.date == reservation.date,
            models.Reservation.status.in_(ACTIVE_RESERVATION_STATUSES),
            models.Reservation.start_time < reservation.end_time,
            models.Reservation.end_time > reservation.start_time,
        )
    )
    if overlapping_seat_reservation.scalars().first():
        raise HTTPException(status_code=400, detail="该座位在所选时间段已被预约")

    overlapping_user_reservation_result = await db.execute(
        select(models.Reservation).where(
            models.Reservation.user_id == reservation.user_id,
            models.Reservation.date == reservation.date,
            models.Reservation.status.in_(ACTIVE_RESERVATION_STATUSES),
            models.Reservation.start_time < reservation.end_time,
            models.Reservation.end_time > reservation.start_time,
        )
    )
    overlapping_user_reservation = overlapping_user_reservation_result.scalars().first()
    if overlapping_user_reservation:
        if (
            overlapping_user_reservation.seat_id == reservation.seat_id
            and overlapping_user_reservation.start_time == reservation.start_time
            and overlapping_user_reservation.end_time == reservation.end_time
        ):
            raise HTTPException(status_code=400, detail="你已预约过该座位的这个时间段，请勿重复提交")
        raise HTTPException(status_code=400, detail="该时间段你已有其他预约，请勿重复预约")

    db_res = models.Reservation(**reservation.model_dump())
    db.add(db_res)
    await db.commit()
    await db.refresh(db_res)
    return db_res

async def get_reservations_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(models.Reservation)
        .where(models.Reservation.user_id == user_id)
        .order_by(models.Reservation.date.desc(), models.Reservation.start_time.desc(), models.Reservation.created_at.desc())
    )
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
def serialize_feedback(feedback: models.Feedback, username: str | None = None, real_name: str | None = None):
    return {
        "id": feedback.id,
        "user_id": feedback.user_id,
        "username": username,
        "real_name": real_name,
        "content": feedback.content,
        "status": feedback.status,
        "reply": feedback.reply,
        "created_at": feedback.created_at,
    }

async def get_feedback_list(db: AsyncSession, user_id: int | None = None):
    stmt = (
        select(models.Feedback, models.User.username, models.User.real_name)
        .join(models.User, models.User.id == models.Feedback.user_id)
        .order_by(models.Feedback.created_at.desc())
    )
    if user_id:
        stmt = stmt.where(models.Feedback.user_id == user_id)
    result = await db.execute(stmt)
    feedback_list = result.all()
    return [serialize_feedback(item[0], item[1], item[2]) for item in feedback_list]

async def create_feedback(db: AsyncSession, feedback: schemas.FeedbackCreate):
    db_feedback = models.Feedback(**feedback.model_dump())
    db.add(db_feedback)
    await db.commit()
    await db.refresh(db_feedback)
    db_user = await get_user_by_id(db, db_feedback.user_id)
    return serialize_feedback(
        db_feedback,
        db_user.username if db_user else None,
        db_user.real_name if db_user else None,
    )

async def reply_feedback(db: AsyncSession, feedback_id: int, reply: str):
    result = await db.execute(select(models.Feedback).where(models.Feedback.id == feedback_id))
    feedback = result.scalars().first()
    if not feedback:
        return None
    feedback.reply = reply
    feedback.status = "replied"
    await db.commit()
    await db.refresh(feedback)
    db_user = await get_user_by_id(db, feedback.user_id)
    return serialize_feedback(
        feedback,
        db_user.username if db_user else None,
        db_user.real_name if db_user else None,
    )

async def delete_feedback(db: AsyncSession, feedback_id: int):
    result = await db.execute(select(models.Feedback).where(models.Feedback.id == feedback_id))
    feedback = result.scalars().first()
    if not feedback:
        return None

    await db.delete(feedback)
    await db.commit()
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
