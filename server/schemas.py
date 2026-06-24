from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date, time

# --- User Schemas ---
class UserBase(BaseModel):
    username: str
    real_name: Optional[str] = None
    role: Optional[str] = "student"
    avatar: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# --- Seat Schemas ---
class SeatBase(BaseModel):
    seat_number: str
    status: Optional[int] = 1
    has_power: Optional[bool] = True

class SeatResponse(SeatBase):
    id: int
    room_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# --- Room Schemas ---
class RoomBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoomResponse(RoomBase):
    id: int
    created_at: datetime
    # seats: List[SeatResponse] = []
    
    class Config:
        from_attributes = True

# --- Reservation Schemas ---
class ReservationBase(BaseModel):
    seat_id: int
    date: date
    start_time: time
    end_time: time

class ReservationCreate(ReservationBase):
    user_id: int

class ReservationResponse(ReservationBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True