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

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    real_name: Optional[str] = None
    role: Optional[str] = None
    avatar: Optional[str] = None

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

class RoomCreate(RoomBase):
    pass

class RoomUpdate(RoomBase):
    pass

class RoomResponse(RoomBase):
    id: int
    created_at: datetime
    
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

# --- Notice Schemas ---
class NoticeBase(BaseModel):
    title: str
    content: str
    level: Optional[str] = "info"
    is_pinned: Optional[bool] = False

class NoticeCreate(NoticeBase):
    pass

class NoticeResponse(NoticeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Feedback Schemas ---
class FeedbackBase(BaseModel):
    content: str

class FeedbackCreate(FeedbackBase):
    user_id: int

class FeedbackReply(BaseModel):
    reply: str

class FeedbackResponse(FeedbackBase):
    id: int
    user_id: int
    username: Optional[str] = None
    real_name: Optional[str] = None
    status: str
    reply: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
