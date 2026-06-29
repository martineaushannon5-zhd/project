# Debug Session: natapp-blank-page

- Status: OPEN
- Started At: 2026-06-25
- Symptom: `https://pd7648d3.natappfree.cc/` 打不开，浏览器 `Network`/`Console` 没明显业务报错。

## Hypotheses

1. `natapp` 隧道虽然在线，但没有真正转发到本地 `5173` 的 Vite 服务。
2. Vite 服务已启动，但响应内容被 `natapp` 或本地环境拦截，导致浏览器拿到空白/异常 HTML。
3. 前端首页已经返回，但脚本资源未正确加载，浏览器因此停留在空白页。
4. 当前运行的 `natapp` 进程不是项目内这个启动器拉起的，绑定了错误的本地端口或旧工作目录。
5. 页面请求被重定向或返回非预期内容，导致浏览器看起来“无报错但打不开”。

## Planned Evidence

- 对公网 `natapp` 地址抓取响应头和响应体
- 对本地 `5173` 抓取响应头和响应体
- 检查本地 Vite 进程与端口占用
- 检查 `natapp` 进程状态与启动日志

## Evidence Collected

- `5173` 初始未监听，本地前端当时没有启动。
- 本机同时存在 3 个 `natapp.exe` 进程，存在残留隧道进程。
- 公网抓取结果一度返回：
  - `HTTP/1.0 404 Not Found`
  - `Tunnel pd7648d3.natappfree.cc not found`
- 清理旧 `natapp` 进程并重新启动后，日志显示：
  - `Tunnel established at http://pd7648d3.natappfree.cc`
  - `Tunnel established at https://pd7648d3.natappfree.cc`
- 本地前端重新启动后：
  - `http://127.0.0.1:5173/` 返回 `200`
  - `https://pd7648d3.natappfree.cc/` 返回 `200`
  - `natapp` 监控页显示 `LocalAddr=127.0.0.1:5173`

## Hypothesis Status

1. `natapp` 没有转发到本地 `5173`：已否定，重启后已确认转发到 `127.0.0.1:5173`
2. 公网地址返回了被替换的错误页面：部分成立，之前确实返回了 `Tunnel not found`
3. 前端脚本资源未加载导致空白页：暂无证据支持，当前首页 HTML 已正常返回
4. 旧 `natapp` 进程绑定错误状态：成立，存在多个残留进程且导致隧道状态异常
5. 公网请求返回非预期内容：成立，之前公网根路径返回的是隧道不存在提示

## Current Conclusion

- 根因是“前端未运行 + 残留 `natapp` 进程导致隧道状态异常/失效”。
- 当前状态下，公网首页与本地首页都已恢复可访问。

## Additional Verification

- 公网资源检查结果：
  - `/` -> `200 OK`
  - `/@vite/client` -> `200 OK`
  - `/src/main.ts` -> `200 OK`
- `natapp` 监控页已观察到这些资源请求，说明浏览器访问确实到达了 `natapp` 并被转发到本地 Vite。
- 用户提供的 `natapp` 运行面板显示：
  - `Tunnel Status: Online`
  - `Forwarding http://pd7648d3.natappfree.cc -> http://127.0.0.1:5173`
  - `Forwarding https://pd7648d3.natappfree.cc -> http://127.0.0.1:5173`
  - 多个前端静态资源请求返回 `200 OK / 304 Not Modified`
  - `GET /` 出现 `101 Switching Protocols`

## Latest Assessment

- 当前剩余问题更可能位于“用户本机浏览器/代理环境”，而不是项目代码、Vite 配置或 `natapp` 隧道本身。
