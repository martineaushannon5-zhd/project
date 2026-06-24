<template>
  <div class="user-container space-y-6">
    <el-card shadow="hover" class="section-card hover-card">
      <template #header>
        <div class="section-header">
          <div>
            <div class="section-title">用户管理</div>
            <div class="section-subtitle">查看系统用户、提交反馈并管理留言。</div>
          </div>
          <div class="actions">
            <el-button type="primary" @click="fetchUsers" :icon="Refresh">刷新用户</el-button>
            <el-button @click="fetchFeedback">刷新留言</el-button>
          </div>
        </div>
      </template>

      <el-table :data="users" v-loading="loading" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名/学号" width="150" />
        <el-table-column prop="real_name" label="真实姓名" width="150" />
        <el-table-column prop="role" label="角色" width="120">
          <template #default="{ row }">
            <el-tag :type="row.role === 'admin' ? 'danger' : 'primary'">
              {{ row.role === 'admin' ? '管理员' : '学生' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="注册时间" />
      </el-table>
    </el-card>

    <el-card shadow="hover" class="section-card hover-card">
      <template #header>
        <div class="section-header">
          <div>
            <div class="section-title">公告通知管理</div>
            <div class="section-subtitle">发布系统公告，支持置顶和等级区分。</div>
          </div>
        </div>
      </template>

      <el-form :model="noticeForm" inline class="mb-4">
        <el-form-item>
          <el-input v-model="noticeForm.title" placeholder="公告标题" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="noticeForm.content" placeholder="公告内容" style="width: 320px" />
        </el-form-item>
        <el-form-item>
          <el-select v-model="noticeForm.level" style="width: 120px">
            <el-option label="普通" value="info" />
            <el-option label="提示" value="success" />
            <el-option label="警告" value="warning" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-switch v-model="noticeForm.is_pinned" active-text="置顶" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitNotice">发布公告</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="notices" border>
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="content" label="内容" min-width="260" />
        <el-table-column prop="level" label="等级" width="100" />
        <el-table-column prop="is_pinned" label="置顶" width="90">
          <template #default="{ row }">
            <el-tag :type="row.is_pinned ? 'success' : 'info'">{{ row.is_pinned ? '是' : '否' }}</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-card shadow="hover" class="section-card hover-card">
      <template #header>
        <div class="section-header">
          <div>
            <div class="section-title">意见反馈 / 留言</div>
            <div class="section-subtitle">收集学生意见，并支持管理员回复。</div>
          </div>
        </div>
      </template>

      <el-form :model="feedbackForm" inline class="mb-4">
        <el-form-item>
          <el-input v-model="feedbackForm.content" placeholder="请输入反馈内容" style="width: 420px" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitFeedback">提交反馈</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="feedbackList" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="content" label="反馈内容" min-width="260" />
        <el-table-column prop="status" label="状态" width="120" />
        <el-table-column prop="reply" label="管理员回复" min-width="220" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import request from '../../utils/request'
import { Refresh } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const users = ref<any[]>([])
const notices = ref<any[]>([])
const feedbackList = ref<any[]>([])
const loading = ref(false)
const user = ref(JSON.parse(localStorage.getItem('user') || '{}'))

const noticeForm = reactive({ title: '', content: '', level: 'info', is_pinned: false })
const feedbackForm = reactive({ content: '' })

const fetchUsers = async () => {
  loading.value = true
  try {
    users.value = await request.get('/api/users/')
  } catch (error) {
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

const fetchNotices = async () => {
  notices.value = await request.get('/api/seats/notices')
}

const fetchFeedback = async () => {
  feedbackList.value = await request.get('/api/users/feedback')
}

const submitNotice = async () => {
  if (!noticeForm.title || !noticeForm.content) {
    ElMessage.warning('请填写完整公告信息')
    return
  }
  await request.post('/api/seats/notices', noticeForm)
  ElMessage.success('公告发布成功')
  noticeForm.title = ''
  noticeForm.content = ''
  noticeForm.level = 'info'
  noticeForm.is_pinned = false
  fetchNotices()
}

const submitFeedback = async () => {
  if (!feedbackForm.content) {
    ElMessage.warning('请输入反馈内容')
    return
  }
  await request.post('/api/users/feedback', { user_id: user.value.id, content: feedbackForm.content })
  ElMessage.success('反馈提交成功')
  feedbackForm.content = ''
  fetchFeedback()
}

onMounted(() => {
  fetchUsers()
  fetchNotices()
  fetchFeedback()
})
</script>
