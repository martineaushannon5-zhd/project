from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True, comment="用户ID")
    username = Column(String(50), unique=True, index=True, nullable=False, comment="用户名/学号")
    password = Column(String(100), nullable=False, comment="密码（明文：123456）")
    real_name = Column(String(50), comment="真实姓名")
    role = Column(String(20), default="student", comment="角色：admin/student")
    avatar = Column(String(255), comment="头像路径")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    
    reservations = relationship("Reservation", back_populates="user", cascade="all, delete-orphan", passive_deletes=True)
    feedbacks = relationship("Feedback", back_populates="user", cascade="all, delete-orphan", passive_deletes=True)

class Room(Base):
    __tablename__ = "room"
    
    id = Column(Integer, primary_key=True, index=True, comment="自习室ID")
    name = Column(String(50), nullable=False, comment="自习室名称")
    description = Column(String(255), comment="描述")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    
    seats = relationship("Seat", back_populates="room", cascade="all, delete-orphan")

class Seat(Base):
    __tablename__ = "seat"
    
    id = Column(Integer, primary_key=True, index=True, comment="座位ID")
    room_id = Column(Integer, ForeignKey("room.id", ondelete="CASCADE"), nullable=False, comment="所属自习室ID")
    seat_number = Column(String(20), nullable=False, comment="座位号")
    status = Column(Integer, default=1, comment="状态：1-正常, 0-维护中")
    has_power = Column(Boolean, default=True, comment="是否有电源")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    
    room = relationship("Room", back_populates="seats")
    reservations = relationship("Reservation", back_populates="seat")

class Reservation(Base):
    __tablename__ = "reservation"
    
    id = Column(Integer, primary_key=True, index=True, comment="预约ID")
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, comment="预约用户ID")
    seat_id = Column(Integer, ForeignKey("seat.id", ondelete="CASCADE"), nullable=False, comment="预约座位ID")
    date = Column(Date, nullable=False, comment="预约日期")
    start_time = Column(Time, nullable=False, comment="开始时间")
    end_time = Column(Time, nullable=False, comment="结束时间")
    status = Column(String(20), default="pending", comment="状态：pending, active, completed, cancelled")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    
    user = relationship("User", back_populates="reservations")
    seat = relationship("Seat", back_populates="reservations")

class Notice(Base):
    __tablename__ = "notice"

    id = Column(Integer, primary_key=True, index=True, comment="公告ID")
    title = Column(String(100), nullable=False, comment="公告标题")
    content = Column(String(1000), nullable=False, comment="公告内容")
    level = Column(String(20), default="info", comment="公告等级")
    is_pinned = Column(Boolean, default=False, comment="是否置顶")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True, comment="反馈ID")
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, comment="反馈用户ID")
    content = Column(String(1000), nullable=False, comment="反馈内容")
    status = Column(String(20), default="pending", comment="处理状态")
    reply = Column(String(1000), comment="管理员回复")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")

    user = relationship("User", back_populates="feedbacks")
