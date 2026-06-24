import axios from 'axios'

// 优先使用环境变量中的 VITE_API_BASE_URL，如果没有则默认指向本地 8000 端口
const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const request = axios.create({
  baseURL,
  timeout: 10000
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    // 可以在这里统一添加 token 等
    const token = localStorage.getItem('token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    return Promise.reject(error)
  }
)

export default request
