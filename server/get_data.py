import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from models import Room, Seat, Reservation

# Get database URL from database.py to reuse its logic
from database import engine, SessionLocal

async def main():
    async with SessionLocal() as db:
        result = await db.execute(select(Room))
        rooms = result.scalars().all()
        print(f"Current rooms: {[r.name for r in rooms]}")

if __name__ == "__main__":
    asyncio.run(main())
