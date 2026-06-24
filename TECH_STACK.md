# 自习室预约管理系统 - 技术栈架构文档

本项目采用现代化的前后端分离架构，旨在提供一个高性能、易维护、且具备良好用户体验的自习室预约服务。以下是完整的技术栈及选型说明。

## 1. 总体架构概述

- **前端架构**：采用 Vue 3 生态，根据业务场景拆分为“后台管理端”与“移动用户端”。
- **后端架构**：采用 FastAPI 异步框架，提供高性能的 RESTful API。
- **数据与缓存**：采用 MySQL 8 作为核心持久化存储，引入 Redis 处理高并发预约及缓存。

---

## 2. 前端技术栈 (Frontend)

前端通过 Vite 构建，根据用户角色的不同，拆分为两个子系统或不同视图：

### 2.1 核心框架与构建
- **核心框架**: [Vue 3](https://vuejs.org/) (Composition API, `<script setup>`)
- **构建工具**: [Vite](https://vitejs.dev/) (极速冷启动，模块热替换 HMR)
- **开发语言**: TypeScript (提供严格的类型检查)

### 2.2 状态管理与路由
- **状态管理**: [Pinia](https://pinia.vuejs.org/) (取代 Vuex，更轻量，完美契合 TS)
- **前端路由**: [Vue Router 4](https://router.vuejs.org/)

### 2.3 UI 组件库选型 (按场景拆分)
- **后台管理端 (PC)**: [Element Plus](https://element-plus.org/)
  - 适用场景：管理员进行座位排布设计、订单管理、用户管理、数据可视化看板等。
- **学生用户端 (移动端)**: [Vant 4](https://vant-contrib.gitee.io/vant) 或 微信小程序 (Taro / uni-app)
  - 适用场景：学生通过手机浏览器或微信扫码进行快速选座、查看预约记录、扫码签到。

### 2.4 网络请求与工具
- **HTTP 客户端**: [Axios](https://axios-http.com/)
- **API 类型生成**: `openapi-typescript` / `openapi-typescript-codegen`
  - 优势：直接解析 FastAPI 自动生成的 OpenAPI 规范，自动生成请求函数和 TS 类型，实现端到端的类型安全。
- **CSS 框架**: [Tailwind CSS](https://tailwindcss.com/) (实用优先的 CSS 框架，方便精细化调优 UI)

---

## 3. 后端技术栈 (Backend)

后端完全拥抱 Python 的异步生态，确保系统在抢座等高并发场景下的吞吐量。

### 3.1 核心框架
- **Web 框架**: [FastAPI](https://fastapi.tiangolo.com/) 
  - 优势：原生异步支持 (`asyncio`)，极高的运行性能，自带交互式 API 文档 (Swagger UI / ReDoc)。
- **开发语言**: Python 3.10+
- **服务器网关**: Uvicorn (基于 uvloop，高性能的 ASGI 服务器)

### 3.2 数据验证与序列化
- **数据校验**: [Pydantic v2](https://docs.pydantic.dev/)
  - 作用：定义请求体、响应体模型，自动验证前端传入的时间格式、座位号类型等，拒绝非法请求。

### 3.3 数据库 ORM 与迁移
- **异步 ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
  - 作用：利用其最新的异步特性进行数据库读写。
- **数据库驱动**: `asyncmy` 或 `aiomysql` (异步 MySQL 驱动)
- **数据迁移工具**: [Alembic](https://alembic.sqlalchemy.org/)
  - 作用：对数据库表结构进行版本控制和增量迁移。

### 3.4 认证与授权
- **鉴权方案**: JWT (JSON Web Tokens)
  - 结合 FastAPI 的 `OAuth2PasswordBearer` 实现无状态登录鉴权。

---

## 4. 数据库与中间件 (Data & Middleware)

### 4.1 核心数据库
- **关系型数据库**: MySQL 8.x
  - 作用：持久化存储用户数据、座位元数据、历史订单记录。利用 ACID 特性确保计费和订单数据的绝对安全。

### 4.2 缓存与并发处理 (核心提升点)
- **内存数据库**: [Redis](https://redis.io/)
  - **核心作用 1：防超卖与抢座**。使用 Redis Lua 脚本或分布式锁处理早高峰抢座逻辑，将并发压力挡在 MySQL 之前。
  - **核心作用 2：状态缓存**。缓存当日的座位预约状态图，极大提升用户端刷新页面的响应速度。

---

## 5. 部署与运维规划 (Ops)

为了配合现代化的技术栈，建议采用容器化部署：

- **容器化**: Docker & Docker Compose (一键编排 FastAPI, MySQL, Redis)
- **反向代理**: Nginx (处理 HTTPS 证书、静态资源托管、请求转发)
- **进程管理**: PM2 (如前端部署 SSR) / Supervisor

---

## 总结

此技术架构兼顾了：
1. **极致的开发体验** (Vite + FastAPI OpenAPI 自动类型生成)
2. **高并发下的系统稳定性** (FastAPI 异步 + Redis 缓存/锁)
3. **多终端的用户体验** (Element Plus 管后台，Vant 管前台移动端)

是一个非常适合作为毕业设计、个人亮点开源项目，甚至可以直接用于商业落地的全栈方案。



## 6. 开发要求与作业规范 (Implementation Requirements & Workflow)

为了确保项目（Python自习室预约管理系统）的顺利推进，并符合大学本科毕业设计的标准，制定以下开发要求与标准作业流程（SOP）。

### 6.1 项目基本要求

1. **项目名称**: Python自习室预约管理系统
2. **目录规范**: 
   - 采用标准的前后端分离目录结构。
   - `server/`：后端 FastAPI 项目目录。
   - `client/`：前端 Vue 3 + Vite 项目目录。
3. **数据层要求**:
   - 数据库：MySQL 8 (实际运行端口 `3306`)。
   - 提供完整的建表 SQL 脚本及包含合理业务逻辑的测试数据初始化脚本。
   - 选做提升：可预留 Redis 接口用于后续并发优化的扩展。
4. **认证与安全**:
   - 考虑到毕业设计的演示便捷性，用户密码暂不进行哈希加密（明文存储为 `123456`），但需在代码中预留密码加密的扩展点。
5. **代码规范**:
   - **全面中文注释**：所有核心类、函数、方法、复杂业务逻辑（如抢座校验）必须包含详尽的中文注释。
6. **功能与界面要求**:
   - **后台主页 (Home)**：必须集成 ECharts 或类似图表库，实现数据可视化（如：今日预约趋势、热门座位统计等）。
   - **UI 风格**：前端需利用 Element Plus 结合 Tailwind CSS 进行深度样式定制，确保界面现代、美观大方，具备良好的交互动效（拒绝原生古板样式）。
7. **文件存储规范**:
   - 所有用户上传的静态资源（如头像、环境图）统一存储于物理绝对路径：`D:\uploads9\` 目录下，并在后端配置静态资源路由映射。

### 6.2 标准作业流程 (SOP)

为保证项目质量，开发将严格按照以下步骤推进：

- **步骤一：后端基建 (Backend Setup)**
  - 在 `server` 目录下初始化 FastAPI 虚拟环境。
  - 配置 SQLAlchemy (Async) 与数据库连接池，编写数据模型 (Models) 和 Pydantic 校验模型 (Schemas)。
  - 编写核心 CRUD 接口，并通过 Swagger UI 进行接口联调测试。

- **步骤二：前端基建 (Frontend Setup)**
  - 在 `client` 目录下执行 `npm create vite@latest` 初始化 Vue 3 + TypeScript 项目。
  - 安装并配置 Element Plus、Pinia、Vue Router 及 Tailwind CSS。
  - 建立基础布局 (Layout)，配置 Axios 请求拦截器与 API 统一管理。

- **步骤三：AI 辅助业务生成 (AI-Assisted Development)**
  - 结合本架构文档与具体需求，利用 AI (如 Cursor / Trae) 逐个模块生成核心业务代码（如：用户鉴权、座位排布图渲染、预约逻辑）。
  - 在生成过程中，严格审查 AI 输出的代码是否符合“中文注释”及“美观大方”的要求。

- **步骤四：端到端联调与 UI 优化 (Integration & Polish)**
  - 前后端接口联调，确保数据统计图表能正确渲染后端数据。
  - 精细化调优前端样式，确保页面响应式和视觉美观度。
  - 完善文件上传逻辑并测试 `D:\uploads9\` 目录的读写权限。

- **步骤五：测试与 Bug 修复 (Testing & Debugging)**
  - 编写并执行测试用例（正常预约流程、时间冲突测试、座位状态刷新）。
  - 修复联调中发现的 Bug，最终产出可用于毕业设计答辩的稳定版本及完整 SQL 文件。



