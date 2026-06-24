from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from schemas import RoomResponse, SeatResponse, ReservationResponse, ReservationCreate, RoomCreate, RoomUpdate, NoticeCreate, NoticeResponse
from crud import (
    get_rooms, get_room_by_id, get_seats_by_room, create_reservation, get_reservations_by_user,
    get_dashboard_stats, create_room, update_room, delete_room, batch_create_seats,
    cancel_reservation, checkin_reservation, get_notices, create_notice
)
from database import get_db

router = APIRouter(prefix="/api/seats", tags=["自习室与座位模块"])

@router.get("/stats")
async def get_stats_endpoint(db: AsyncSession = Depends(get_db)):
    """获取数据看板统计信息"""
    return await get_dashboard_stats(db)

@router.get("/rooms", response_model=List[RoomResponse])
async def get_rooms_endpoint(db: AsyncSession = Depends(get_db)):
    """获取所有自习室"""
    return await get_rooms(db)

@router.post("/rooms", response_model=RoomResponse)
async def create_room_endpoint(room: RoomCreate, db: AsyncSession = Depends(get_db)):
    """创建自习室"""
    return await create_room(db, room)

@router.put("/rooms/{room_id}", response_model=RoomResponse)
async def update_room_endpoint(room_id: int, room: RoomUpdate, db: AsyncSession = Depends(get_db)):
    """更新自习室"""
    updated = await update_room(db, room_id, room)
    if not updated:
        raise HTTPException(status_code=404, detail="自习室不存在")
    return updated

@router.delete("/rooms/{room_id}")
async def delete_room_endpoint(room_id: int, db: AsyncSession = Depends(get_db)):
    """删除自习室"""
    deleted = await delete_room(db, room_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="自习室不存在")
    return {"message": "删除成功"}

@router.post("/rooms/{room_id}/seats/batch")
async def batch_create_seats_endpoint(room_id: int, prefix: str, count: int, has_power: bool = True, db: AsyncSession = Depends(get_db)):
    """批量生成座位"""
    return await batch_create_seats(db, room_id, prefix, count, has_power)

@router.get("/rooms/{room_id}/seats", response_model=List[SeatResponse])
async def get_seats_endpoint(room_id: int, db: AsyncSession = Depends(get_db)):
    """获取指定自习室的座位列表"""
    return await get_seats_by_room(db, room_id)

@router.post("/reservations", response_model=ReservationResponse)
async def create_reservation_endpoint(res: ReservationCreate, db: AsyncSession = Depends(get_db)):
    """预约座位"""
    return await create_reservation(db, res)

@router.get("/reservations/user/{user_id}", response_model=List[ReservationResponse])
async def get_user_reservations_endpoint(user_id: int, db: AsyncSession = Depends(get_db)):
    """获取某用户的预约记录"""
    return await get_reservations_by_user(db, user_id)

@router.post("/reservations/{reservation_id}/cancel")
async def cancel_reservation_endpoint(reservation_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    """取消预约"""
    result = await cancel_reservation(db, reservation_id, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="预约不存在")
    return {"message": "取消成功", "data": result}

@router.post("/reservations/{reservation_id}/checkin")
async def checkin_reservation_endpoint(reservation_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    """签到"""
    result = await checkin_reservation(db, reservation_id, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="预约不存在")
    return {"message": "签到成功", "data": result}

@router.get("/notices", response_model=List[NoticeResponse])
async def list_notices(db: AsyncSession = Depends(get_db)):
    """获取公告列表"""
    return await get_notices(db)

@router.post("/notices", response_model=NoticeResponse)
async def add_notice(notice: NoticeCreate, db: AsyncSession = Depends(get_db)):
    """新增公告"""
    return await create_notice(db, notice)
