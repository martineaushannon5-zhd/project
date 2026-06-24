from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from routers import user, seat

app = FastAPI(
    title="Python自习室预约管理系统",
    description="前后端分离，Vue3 + FastAPI + MySQL 8",
    version="1.0.0"
)

# 1. 配置跨域 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境应配置为前端实际域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 请求头
)

# 2. 挂载静态文件目录（统一使用 resource 目录存放图片、文件与生成资源）
RESOURCE_DIR = os.path.join(os.path.dirname(__file__), "resource")
if not os.path.exists(RESOURCE_DIR):
    os.makedirs(RESOURCE_DIR)

app.mount("/resource", StaticFiles(directory=RESOURCE_DIR), name="resource")

# 3. 注册业务路由
app.include_router(user.router)
app.include_router(seat.router)

# 4. 根路由测试
@app.get("/")
async def root():
    """
    根路由测试接口
    """
    return {"message": "欢迎使用Python自习室预约管理系统API", "status": "success"}