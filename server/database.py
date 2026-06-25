import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

# MySQL 8 数据库配置
# 优先从环境变量 DATABASE_URL 获取，如果没有则使用本地开发环境的配置
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+aiomysql://root:Zhd%406266@localhost:3306/study_room?charset=utf8mb4"
)

# 创建异步数据库引擎
# 云数据库/Serverless 环境会主动回收空闲连接，这里开启连接预检查与定期回收，
# 避免 Render 运行一段时间后从连接池取到失效连接而触发 500。
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=1800,
)

# 创建异步会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# 声明模型基类
Base = declarative_base()

async def get_db():
    """获取数据库Session的依赖注入"""
    async with SessionLocal() as session:
        yield session
