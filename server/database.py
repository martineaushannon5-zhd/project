import os
import ssl
from urllib.parse import parse_qsl, unquote, urlparse
import aiomysql
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

# MySQL 8 数据库配置
# 优先从环境变量 DATABASE_URL 获取，如果没有则使用本地开发环境的配置
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+aiomysql://root:Zhd%406266@localhost:3306/study_room?charset=utf8mb4"
)

parsed_database_url = urlparse(DATABASE_URL)
is_remote_database = parsed_database_url.hostname not in {None, "localhost", "127.0.0.1"}

query_params = dict(parse_qsl(parsed_database_url.query, keep_blank_values=True))

engine_kwargs = {
    "echo": True,
    "pool_pre_ping": True,
    "pool_recycle": 300,
}

if is_remote_database:
    ssl_ca = os.getenv("DB_SSL_CA")
    if not ssl_ca:
        default_render_ca = "/etc/ssl/certs/ca-certificates.crt"
        ssl_ca = default_render_ca if os.path.exists(default_render_ca) else None

    ssl_context = ssl.create_default_context(cafile=ssl_ca)
    db_name = parsed_database_url.path.lstrip("/")
    charset = query_params.get("charset", "utf8mb4")

    async def remote_async_creator():
        return await aiomysql.connect(
            host=parsed_database_url.hostname,
            port=parsed_database_url.port or 3306,
            user=unquote(parsed_database_url.username or ""),
            password=unquote(parsed_database_url.password or ""),
            db=db_name,
            charset=charset,
            autocommit=False,
            ssl=ssl_context,
        )

    engine_kwargs["async_creator"] = remote_async_creator

# 创建异步数据库引擎
# 云数据库/Serverless 环境会主动回收空闲连接，这里开启连接预检查与定期回收，
# 避免 Render 运行一段时间后从连接池取到失效连接而触发 500。
engine = create_async_engine(
    DATABASE_URL,
    **engine_kwargs,
)

# 创建异步会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# 声明模型基类
Base = declarative_base()

async def get_db():
    """获取数据库Session的依赖注入"""
    async with SessionLocal() as session:
        yield session
