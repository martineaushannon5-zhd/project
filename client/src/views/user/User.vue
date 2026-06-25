<template>
  <div class="user-page">
    <el-card v-if="isAdmin" shadow="hover" class="section-card hover-card">
      <template #header>
        <div class="section-header">
          <div>
            <div class="section-title">用户管理</div>
            <div class="section-subtitle">查看系统用户，支持查找、新增、编辑和删除操作。</div>
          </div>
          <div class="header-actions">
            <el-button type="primary" plain :icon="Refresh" @click="fetchUsers">刷新用户</el-button>
            <el-button type="primary" :icon="Plus" @click="openCreateDialog">新增用户</el-button>
          </div>
        </div>
      </template>

      <div class="toolbar">
        <el-input
          v-model="userFilters.keyword"
          placeholder="查找用户名/真实姓名"
          clearable
          @keyup.enter="fetchUsers"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-select v-model="userFilters.role" placeholder="全部角色" clearable>
          <el-option label="管理员" value="admin" />
          <el-option label="学生" value="student" />
        </el-select>
        <el-button type="primary" @click="fetchUsers">查找</el-button>
        <el-button @click="resetUserFilters">重置</el-button>
      </div>

      <el-table :data="users" v-loading="userLoading" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名/学号" min-width="160" />
        <el-table-column prop="real_name" label="真实姓名" min-width="140" />
        <el-table-column prop="role" label="角色" width="120">
          <template #default="{ row }">
            <el-tag :type="row.role === 'admin' ? 'danger' : 'primary'">
              {{ row.role === 'admin' ? '管理员' : '学生' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="注册时间" min-width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="210" fixed="right">
          <template #default="{ row }">
            <div class="row-actions">
              <el-button link type="primary" @click="openEditDialog(row)">编辑</el-button>
              <el-button
                link
                type="danger"
                :disabled="row.id === currentUser.id"
                @click="handleDeleteUser(row)"
              >
                删除
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-card v-if="isAdmin" shadow="hover" class="section-card hover-card">
      <template #header>
        <div class="section-header">
          <div>
            <div class="section-title">公告通知管理</div>
            <div class="section-subtitle">发布系统公告，支持置顶和等级区分。</div>
          </div>
        </div>
      </template>

      <div class="notice-form-grid">
        <el-input v-model="noticeForm.title" placeholder="公告标题" />
        <el-input v-model="noticeForm.content" placeholder="公告内容" />
        <el-select v-model="noticeForm.level">
          <el-option label="普通" value="info" />
          <el-option label="提示" value="success" />
          <el-option label="警告" value="warning" />
        </el-select>
        <el-switch v-model="noticeForm.is_pinned" active-text="置顶" />
        <el-button type="primary" @click="submitNotice">发布公告</el-button>
      </div>

      <el-table :data="notices" border>
        <el-table-column prop="title" label="标题" min-width="180" />
        <el-table-column prop="content" label="内容" min-width="260" />
        <el-table-column prop="level" label="等级" width="100" />
        <el-table-column prop="is_pinned" label="置顶" width="90">
          <template #default="{ row }">
            <el-tag :type="row.is_pinned ? 'success' : 'info'">{{ row.is_pinned ? '是' : '否' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="发布时间" min-width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-card shadow="hover" class="section-card hover-card">
      <template #header>
        <div class="section-header">
          <div>
            <div class="section-title">{{ isAdmin ? '反馈与留言管理' : '意见反馈 / 留言' }}</div>
            <div class="section-subtitle">
              {{ isAdmin ? '统一查看系统留言，支持回复与删除。' : '提交你的建议，查看管理员回复。' }}
            </div>
          </div>
          <div v-if="isAdmin" class="header-actions">
            <el-button plain :icon="Refresh" @click="fetchFeedback">刷新留言</el-button>
          </div>
        </div>
      </template>

      <div class="feedback-compose">
        <el-input
          v-model="feedbackForm.content"
          type="textarea"
          :rows="3"
          placeholder="请输入反馈内容或留言"
        />
        <div class="feedback-actions">
          <el-button type="primary" @click="submitFeedback">提交反馈</el-button>
        </div>
      </div>

      <el-table :data="feedbackList" v-loading="feedbackLoading" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column v-if="isAdmin" prop="username" label="用户名" width="150" />
        <el-table-column v-if="isAdmin" prop="real_name" label="姓名" width="140" />
        <el-table-column prop="content" label="反馈内容" min-width="260" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="row.status === 'replied' ? 'success' : 'warning'">
              {{ row.status === 'replied' ? '已回复' : '待处理' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="reply" label="管理员回复" min-width="220">
          <template #default="{ row }">
            {{ row.reply || '暂无回复' }}
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="提交时间" min-width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column v-if="isAdmin" label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <div class="row-actions">
              <el-button link type="primary" @click="handleReplyFeedback(row)">
                {{ row.reply ? '编辑回复' : '回复' }}
              </el-button>
              <el-button link type="danger" @click="handleDeleteFeedback(row)">删除</el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog
      v-model="userDialogVisible"
      :title="editingUserId ? '编辑用户' : '新增用户'"
      width="520px"
      destroy-on-close
    >
      <div class="dialog-form">
        <el-input v-model="userForm.username" placeholder="请输入用户名/学号" />
        <el-input v-model="userForm.real_name" placeholder="请输入真实姓名" />
        <el-select v-model="userForm.role" placeholder="请选择角色">
          <el-option label="管理员" value="admin" />
          <el-option label="学生" value="student" />
        </el-select>
        <el-input
          v-model="userForm.password"
          type="password"
          show-password
          :placeholder="editingUserId ? '留空则不修改密码' : '请输入登录密码'"
        />
      </div>
      <template #footer>
        <el-button @click="userDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitUserForm">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Refresh, Search } from '@element-plus/icons-vue'
import request from '../../utils/request'

interface UserRecord {
  id: number
  username: string
  real_name?: string
  role: string
  created_at?: string
}

interface NoticeRecord {
  id: number
  title: string
  content: string
  level: string
  is_pinned: boolean
  created_at?: string
}

interface FeedbackRecord {
  id: number
  user_id: number
  username?: string
  real_name?: string
  content: string
  status: string
  reply?: string
  created_at?: string
}

const currentUser = ref<any>(JSON.parse(localStorage.getItem('user') || '{}'))
const isAdmin = computed(() => currentUser.value?.role === 'admin')

const users = ref<UserRecord[]>([])
const notices = ref<NoticeRecord[]>([])
const feedbackList = ref<FeedbackRecord[]>([])

const userLoading = ref(false)
const feedbackLoading = ref(false)
const userDialogVisible = ref(false)
const editingUserId = ref<number | null>(null)

const userFilters = reactive({
  keyword: '',
  role: ''
})

const userForm = reactive({
  username: '',
  real_name: '',
  role: 'student',
  password: ''
})

const noticeForm = reactive({
  title: '',
  content: '',
  level: 'info',
  is_pinned: false
})

const feedbackForm = reactive({
  content: ''
})

const resetUserForm = () => {
  userForm.username = ''
  userForm.real_name = ''
  userForm.role = 'student'
  userForm.password = ''
}

const formatDate = (value?: string) => {
  if (!value) return '-'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleString('zh-CN', { hour12: false })
}

const fetchUsers = async () => {
  if (!isAdmin.value) return
  userLoading.value = true
  try {
    const params: Record<string, string> = {}
    if (userFilters.keyword.trim()) params.keyword = userFilters.keyword.trim()
    if (userFilters.role) params.role = userFilters.role
    users.value = await request.get('/api/users/', { params })
  } catch (error) {
    ElMessage.error('获取用户列表失败')
  } finally {
    userLoading.value = false
  }
}

const resetUserFilters = async () => {
  userFilters.keyword = ''
  userFilters.role = ''
  await fetchUsers()
}

const fetchNotices = async () => {
  if (!isAdmin.value) return
  try {
    notices.value = await request.get('/api/seats/notices')
  } catch (error) {
    ElMessage.error('获取公告失败')
  }
}

const fetchFeedback = async () => {
  feedbackLoading.value = true
  try {
    const params = !isAdmin.value && currentUser.value?.id ? { user_id: currentUser.value.id } : undefined
    feedbackList.value = await request.get('/api/users/feedback', { params })
  } catch (error) {
    ElMessage.error('获取留言失败')
  } finally {
    feedbackLoading.value = false
  }
}

const submitNotice = async () => {
  if (!noticeForm.title || !noticeForm.content) {
    ElMessage.warning('请填写完整公告信息')
    return
  }
  try {
    await request.post('/api/seats/notices', noticeForm)
    ElMessage.success('公告发布成功')
    noticeForm.title = ''
    noticeForm.content = ''
    noticeForm.level = 'info'
    noticeForm.is_pinned = false
    await fetchNotices()
  } catch (error) {
    ElMessage.error('公告发布失败')
  }
}

const submitFeedback = async () => {
  if (!feedbackForm.content.trim()) {
    ElMessage.warning('请输入反馈内容')
    return
  }
  if (!currentUser.value?.id) {
    ElMessage.error('未获取到当前登录用户')
    return
  }
  try {
    await request.post('/api/users/feedback', {
      user_id: currentUser.value.id,
      content: feedbackForm.content.trim()
    })
    ElMessage.success('反馈提交成功')
    feedbackForm.content = ''
    await fetchFeedback()
  } catch (error) {
    ElMessage.error('反馈提交失败')
  }
}

const openCreateDialog = () => {
  editingUserId.value = null
  resetUserForm()
  userDialogVisible.value = true
}

const openEditDialog = (row: UserRecord) => {
  editingUserId.value = row.id
  userForm.username = row.username
  userForm.real_name = row.real_name || ''
  userForm.role = row.role
  userForm.password = ''
  userDialogVisible.value = true
}

const submitUserForm = async () => {
  if (!userForm.username.trim()) {
    ElMessage.warning('请输入用户名')
    return
  }
  if (!editingUserId.value && !userForm.password.trim()) {
    ElMessage.warning('请输入登录密码')
    return
  }

  const payload: Record<string, string> = {
    username: userForm.username.trim(),
    real_name: userForm.real_name.trim(),
    role: userForm.role
  }

  if (userForm.password.trim()) {
    payload.password = userForm.password.trim()
  }

  try {
    if (editingUserId.value) {
      await request.put(`/api/users/${editingUserId.value}`, payload)
      ElMessage.success('用户更新成功')
    } else {
      await request.post('/api/users/', payload)
      ElMessage.success('用户新增成功')
    }
    userDialogVisible.value = false
    await fetchUsers()
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '保存用户失败')
  }
}

const handleDeleteUser = async (row: UserRecord) => {
  try {
    await ElMessageBox.confirm(`确定删除用户“${row.username}”吗？`, '删除确认', {
      type: 'warning'
    })
    await request.delete(`/api/users/${row.id}`)
    ElMessage.success('用户删除成功')
    await fetchUsers()
    await fetchFeedback()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '删除用户失败')
    }
  }
}

const handleReplyFeedback = async (row: FeedbackRecord) => {
  try {
    const { value } = await ElMessageBox.prompt('请输入管理员回复内容', '回复留言', {
      confirmButtonText: '提交回复',
      cancelButtonText: '取消',
      inputValue: row.reply || '',
      inputType: 'textarea',
      inputPattern: /.+/,
      inputErrorMessage: '回复内容不能为空'
    })
    await request.post(`/api/users/feedback/${row.id}/reply`, { reply: value })
    ElMessage.success('回复成功')
    await fetchFeedback()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '回复失败')
    }
  }
}

const handleDeleteFeedback = async (row: FeedbackRecord) => {
  try {
    await ElMessageBox.confirm('确定删除这条留言吗？', '删除确认', {
      type: 'warning'
    })
    await request.delete(`/api/users/feedback/${row.id}`)
    ElMessage.success('留言删除成功')
    await fetchFeedback()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '删除留言失败')
    }
  }
}

onMounted(async () => {
  if (isAdmin.value) {
    await fetchUsers()
    await fetchNotices()
  }
  await fetchFeedback()
})
</script>

<style scoped>
.user-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.section-card {
  border: none;
  border-radius: 24px;
  box-shadow: 0 20px 45px rgba(15, 23, 42, 0.06);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}

.section-title {
  font-size: 20px;
  font-weight: 800;
  color: #0f172a;
}

.section-subtitle {
  margin-top: 6px;
  color: #64748b;
  font-size: 13px;
}

.header-actions,
.row-actions,
.feedback-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.toolbar {
  display: grid;
  grid-template-columns: minmax(240px, 1.4fr) minmax(140px, 0.7fr) auto auto;
  gap: 12px;
  margin-bottom: 18px;
}

.notice-form-grid {
  display: grid;
  grid-template-columns: 1fr 1.4fr 140px 120px 120px;
  gap: 12px;
  margin-bottom: 18px;
}

.feedback-compose {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-bottom: 18px;
}

.feedback-actions {
  justify-content: flex-end;
}

.dialog-form {
  display: grid;
  gap: 14px;
}

@media (max-width: 1100px) {
  .toolbar,
  .notice-form-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .section-header {
    flex-direction: column;
  }

  .header-actions {
    width: 100%;
    flex-wrap: wrap;
  }
}
</style>
