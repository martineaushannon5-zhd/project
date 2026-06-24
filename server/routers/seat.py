from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from schemas import RoomResponse, SeatResponse, ReservationResponse, ReservationCreate
from crud import get_rooms, get_seats_by_room, create_reservation, get_reservations_by_user
from database import get_db

router = APIRouter(prefix="/api/seats", tags=["自习室与座位模块"])

@router.get("/rooms", response_model=List[RoomResponse])
async def get_rooms_endpoint(db: AsyncSession = Depends(get_db)):
    """获取所有自习室"""
    return await get_rooms(db)

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