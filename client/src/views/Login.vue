<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <el-card class="w-96 shadow-lg rounded-2xl">
      <template #header>
        <div class="text-center text-2xl font-bold text-gray-700">
          Python自习室预约系统
        </div>
      </template>
      <el-form :model="form" :rules="rules" ref="loginForm" label-width="0">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名/学号" :prefix-icon="User" size="large" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码 (123456)" :prefix-icon="Lock" size="large" show-password @keyup.enter="handleLogin" />
        </el-form-item>
        <el-button type="primary" class="w-full mt-4" size="large" @click="handleLogin" :loading="loading">
          登 录
        </el-button>
      </el-form>
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
  username: 'admin',
  password: '123456'
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
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
          router.push('/')
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