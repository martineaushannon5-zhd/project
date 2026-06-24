# 测试文档

## 1. 启动信息

### 后端 API (FastAPI)
- **启动状态**: 已启动
- **服务地址**: http://localhost:8000
- **接口文档**: [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)

### 前端应用 (Vue 3 + Vite)
- **启动状态**: 已启动
- **服务地址**: http://localhost:5173

## 2. 测试账号
在登录页输入以下账号进行测试：
- **管理员**: `admin` / `123456`
- **学生 1**: `student1` / `123456`
- **学生 2**: `student2` / `123456`

## 3. 功能测试指南
1. 访问 http://localhost:5173 进入登录页，输入管理员账号登录。
2. 登录成功后将进入系统后台主页。
3. 您可以查看到包含图表展示的数据看板（Echarts 渲染）。
4. 验证 API 文档：访问 http://localhost:8000/docs 查看 FastAPI 自动生成的接口文档，可直接测试用户、自习室、预约等接口。

*注：确保本地已启动 MySQL 8 服务（端口 3306），并已导入 `database.sql` 脚本，同时在 `server/database.py` 中配置了正确的数据库密码，否则登录接口会因无法连接数据库而报错。*