# Debug Session: render-login-failed

- Status: OPEN
- Started At: 2026-06-25
- Symptom: 前端已切回 Vercel，但线上登录提示“登录失败，请检查网络”，怀疑 Render 后端异常或登录接口存在 bug。

## Hypotheses

1. Render 后端服务已休眠、崩溃或返回 5xx，导致前端把错误统一显示为“请检查网络”。
2. `/api/users/login` 接口在线，但请求体或响应结构与前端预期不一致，导致前端进入错误提示分支。
3. 后端连接云端数据库失败，根路径可访问但登录时查询用户报错。
4. Vercel 前端的 `VITE_API_BASE_URL` 配置错误，请求并没有真正打到 `https://project-82no.onrender.com`。
5. 登录账号本身在当前线上数据库中不存在或密码不匹配，因此返回 400，被前端当成普通失败展示。

## Planned Evidence

- 验证 Render 根路由可访问性
- 直接请求线上 `/api/users/login` 收集状态码和响应体
- 检查前端当前 API 基地址配置来源
- 必要时查看线上页面实际发出的请求地址

## Evidence Collected

- `GET https://project-82no.onrender.com/` -> `200`
- `POST https://project-82no.onrender.com/api/users/login` with `admin / 123456` -> `500 Internal Server Error`
- `GET https://project-82no.onrender.com/api/users/` -> `500 Internal Server Error`
- `GET https://project-82no.onrender.com/api/seats/notices` -> `500 Internal Server Error`
- Vercel 前端登录页可以正常打开，说明前端站点本身已上线。

## Hypothesis Status

1. Render 后端服务已休眠、崩溃或返回 5xx：部分否定。根路由正常，但数据库相关接口返回 500。
2. `/api/users/login` 响应结构不一致：暂不支持。接口在进入正常业务返回前就已 500。
3. 后端连接云端数据库失败：高度可疑。
4. Vercel 前端 `VITE_API_BASE_URL` 配置错误：基本否定。直接请求 Render 接口也能复现 500。
5. 线上账号本身不存在或密码不匹配：基本否定。正常应返回 400，而不是 500。

## Current Assessment

- 当前最可能的根因是“Render 上数据库查询链路异常”，包括但不限于：
  - 云数据库连接/权限异常
  - 线上表结构与当前 SQLAlchemy 模型不一致
  - 查询阶段触发了数据库层异常

## New Evidence

- 本地 `git status --short` 显示以下关键文件仍未提交：
  - `server/database.py`
  - `server/crud.py`
  - `server/main.py`
  - `server/models.py`
  - `server/routers/user.py`
  - `server/schemas.py`
- Render 日志显示当前部署提交是 `9ccadb2...`，而本地连接池修复并未进入远端部署版本。

## Updated Assessment

- 当前线上 500 仍然大概率是旧版本后端在运行。
- 在拿到新的运行时日志之前，必须先把真正的后端修复提交并部署到 Render，再验证修复是否生效。
