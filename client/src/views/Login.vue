<template>
  <div class="login-page">
    <div class="login-hero">
      <div class="hero-tag">Python 自习室预约系统</div>
      <h1>学生门户与管理员后台分流</h1>
      <p>学生登录后进入网站风格门户，管理员登录后进入后台管理中心。</p>
      <div class="hero-features">
        <span>座位预约</span>
        <span>公告通知</span>
        <span>我的预约</span>
        <span>意见反馈</span>
      </div>
    </div>

    <el-card class="login-card hover-card" shadow="hover">
      <template #header>
        <div class="text-center text-2xl font-bold text-gray-700">欢迎登录</div>
      </template>
      <el-form :model="form" :rules="rules" ref="loginForm" label-width="0">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名/学号" :prefix-icon="User" size="large" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" :prefix-icon="Lock" size="large" show-password @keyup.enter="handleLogin" />
        </el-form-item>
        <el-button type="primary" class="w-full mt-4" size="large" @click="handleLogin" :loading="loading">
          立即进入
        </el-button>
      </el-form>
      <div class="login-tips">学生账号：student1 / 123456　管理员账号：admin / 123456</div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import request from '../utils/request'

const router = useRouter()
const loginForm = ref()
const loading = ref(false)

const form = reactive({
  username: 'student1',
  password: '123456'
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

/** 根据角色跳转到不同端 */
const resolveRedirect = (role?: string) => {
  return role === 'admin' ? '/admin/home' : '/portal/home'
}

const handleLogin = async () => {
  if (!loginForm.value) return
  await loginForm.value.validate(async (valid: boolean) => {
    if (valid) {
      loading.value = true
      try {
        const res: any = await request.post('/api/users/login', form)
        if (res) {
          ElMessage.success('登录成功')
          localStorage.setItem('user', JSON.stringify(res.user || res))
          const role = res.user?.role || res.role
          router.push(resolveRedirect(role))
        }
      } catch (error: any) {
        ElMessage.error(error.response?.data?.detail || '登录失败，请检查网络')
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 32px;
  align-items: center;
  padding: 40px;
  background: linear-gradient(135deg, #eff6ff 0%, #f8fbff 45%, #eef2ff 100%);
}

.login-hero {
  padding: 48px;
  border-radius: 28px;
  background: linear-gradient(135deg, rgba(37,99,235,0.95), rgba(124,58,237,0.92));
  color: #fff;
  box-shadow: 0 24px 60px rgba(37, 99, 235, 0.22);
}

.hero-tag {
  display: inline-flex;
  padding: 6px 14px;
  border-radius: 999px;
  background: rgba(255,255,255,0.14);
  font-size: 12px;
  margin-bottom: 20px;
}

.login-hero h1 {
  margin: 0;
  font-size: 42px;
  line-height: 1.15;
}

.login-hero p {
  margin-top: 16px;
  max-width: 520px;
  opacity: 0.92;
  font-size: 16px;
}

.hero-features {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 28px;
}

.hero-features span {
  padding: 10px 14px;
  border-radius: 999px;
  background: rgba(255,255,255,0.14);
}

.login-card {
  border: none;
  border-radius: 24px;
  padding: 6px;
}

.login-tips {
  margin-top: 16px;
  color: #64748b;
  font-size: 12px;
  text-align: center;
}

@media (max-width: 960px) {
  .login-page {
    grid-template-columns: 1fr;
  }

  .login-hero h1 {
    font-size: 32px;
  }
}
</style>
