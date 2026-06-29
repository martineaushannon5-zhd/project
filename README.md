# 自习室预约系统

一个基于 `Vue 3 + Vite + Element Plus + FastAPI + SQLAlchemy` 的自习室预约管理系统，支持学生端预约使用，也支持管理员端进行用户管理、留言处理、公告管理和预约管理。

## 项目简介

本项目采用前后端分离架构：

- 前端：`Vue 3 + Vite + Element Plus`
- 后端：`FastAPI + SQLAlchemy + aiomysql`
- 云数据库：`TiDB Cloud Starter`
- 前端部署平台：`Vercel`
- 后端部署平台：`Render`

系统为单前端入口模式，不同角色登录后显示不同功能：

- 学生端：预约座位、查看公告、提交反馈、查看个人信息
- 管理端：数据看板、用户管理、留言回复、公告管理、自习室和预约管理

## 线上访问地址

- 官方网站：[https://project1-beige-mu.vercel.app/](https://project1-beige-mu.vercel.app/)
- 管理端页面：[https://project1-beige-mu.vercel.app/admin/user](https://project1-beige-mu.vercel.app/admin/user)
- 后端 API 根地址：[https://project-82no.onrender.com](https://project-82no.onrender.com)
- 后端接口文档：[https://project-82no.onrender.com/docs](https://project-82no.onrender.com/docs)

说明：

- 前端由 `Vercel` 托管，负责页面展示与静态资源分发
- 后端由 `Render` 托管，负责业务接口与数据处理
- 数据库存储在 `TiDB Cloud Starter`，通过公网 TLS 连接供 Render 后端访问

## 部署架构

- 前端仓库目录：`client`
- Vercel Root Directory：`client`
- 前端生产环境变量：`VITE_API_BASE_URL=https://project-82no.onrender.com`
- 后端运行目录：`server`
- 后端关键环境变量：`DATABASE_URL`
- 数据库平台：`TiDB Cloud Starter`

当前生产环境的数据流向：

1. 用户访问 `Vercel` 上的前端页面
2. 前端通过 `VITE_API_BASE_URL` 请求 `Render` 上的 FastAPI 接口
3. FastAPI 再连接 `TiDB Cloud` 中的 MySQL 兼容数据库

## 本地开发地址

- 前端开发地址：[http://localhost:5173/](http://localhost:5173/)
- 后端开发地址：`http://127.0.0.1:8000`
- 本地接口文档：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

说明：

- 本地开发时前端默认运行在 `5173`
- 如果出现 `5174`，通常说明重复启动了前端开发服务器
- 建议本地只保留一个前端 dev 进程，避免端口混乱

## 本地启动方式

请分别打开两个终端窗口。

### 终端 1：启动后端

```bash
cd server
..\venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
```

当终端出现 `Application startup complete` 时，表示后端启动成功。

### 终端 2：启动前端

```bash
cd client
npm run dev
```

当终端出现 `Local: http://localhost:5173/` 时，表示前端启动成功。

## 目录结构

```text
project/
├─ client/          # Vue 3 前端
├─ server/          # FastAPI 后端
├─ database.sql     # 初始数据结构参考
└─ README.md
```

## 生产环境说明

### 前端

- 部署平台：`Vercel`
- 线上域名：`https://project1-beige-mu.vercel.app/`
- 构建命令：`npm run build`
- 输出目录：`dist`

### 后端

- 部署平台：`Render`
- 线上地址：`https://project-82no.onrender.com`
- 启动命令：`uvicorn main:app --host 0.0.0.0 --port $PORT`

### 数据库

- 平台：`TiDB Cloud Starter`
- 数据库类型：MySQL 兼容
- 连接方式：公网 TLS 连接

## 常见说明

### 为什么线上前端不能请求 `localhost:8000`

因为线上环境中的 `localhost` 指向访问者自己的设备，而不是云服务器。  
因此生产环境必须通过 `VITE_API_BASE_URL` 指向真正的线上后端地址：

```env
VITE_API_BASE_URL=https://project-82no.onrender.com
```

### 为什么要把前后端分开部署

- 前端更适合托管到 `Vercel`
- FastAPI 后端更适合运行在 `Render`
- 数据库独立放在 `TiDB Cloud`，更贴近真实生产部署方式

这种拆分方式更符合现代全栈项目的实际使用习惯，也更方便后续扩展与维护。
