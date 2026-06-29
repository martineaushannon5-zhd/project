<template>
  <div class="user-page">
    <el-card shadow="hover" class="section-card hover-card portal-hover" v-if="isAdmin">
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
        <el-input v-model="userFilters.keyword" placeholder="查找用户名/真实姓名" clearable @keyup.enter="fetchUsers">
          <template #prefix><el-icon><Search /></el-icon></template>
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
          <template #default="{ row }"><el-tag :type="row.role === 'admin' ? 'danger' : 'primary'">{{ row.role === 'admin' ? '管理员' : '学生' }}</el-tag></template>
        </el-table-column>
        <el-table-column prop="created_at" label="注册时间" min-width="180"><template #default="{ row }">{{ formatDate(row.created_at) }}</template></el-table-column>
        <el-table-column label="操作" width="210" fixed="right">
          <template #default="{ row }"><div class="row-actions"><el-button link type="primary" @click="openEditDialog(row)">编辑</el-button><el-button link type="danger" :disabled="row.id === currentUser.id" @click="handleDeleteUser(row)">删除</el-button></div></template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-card shadow="hover" class="section-card hover-card portal-hover" v-if="isAdmin">
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
        <el-select v-model="noticeForm.level"><el-option label="普通" value="info" /><el-option label="提示" value="success" /><el-option label="警告" value="warning" /></el-select>
        <el-switch v-model="noticeForm.is_pinned" active-text="置顶" />
        <el-button type="primary" @click="submitNotice">发布公告</el-button>
      </div>
      <el-table :data="notices" border>
        <el-table-column prop="title" label="标题" min-width="180" />
        <el-table-column prop="content" label="内容" min-width="260" />
        <el-table-column prop="level" label="等级" width="100" />
        <el-table-column prop="is_pinned" label="置顶" width="90"><template #default="{ row }"><el-tag :type="row.is_pinned ? 'success' : 'info'">{{ row.is_pinned ? '是' : '否' }}</el-tag></template></el-table-column>
        <el-table-column prop="created_at" label="发布时间" min-width="180"><template #default="{ row }">{{ formatDate(row.created_at) }}</template></el-table-column>
      </el-table>
    </el-card>

    <el-card shadow="hover" class="section-card hover-card portal-hover">
      <template #header>
        <div class="section-header">
          <div>
            <div class="section-title">{{ isAdmin ? '反馈与留言管理' : '意见反馈 / 留言' }}</div>
            <div class="section-subtitle">{{ isAdmin ? '统一查看系统留言，支持回复与删除。' : '提交你的建议，查看管理员回复。' }}</div>
          </div>
          <div v-if="isAdmin" class="header-actions"><el-button plain :icon="Refresh" @click="fetchFeedback">刷新留言</el-button></div>
        </div>
      </template>
      <div class="feedback-compose">
        <el-input v-model="feedbackForm.content" type="textarea" :rows="3" placeholder="请输入反馈内容或留言" />
        <div class="feedback-actions"><el-button type="primary" @click="submitFeedback">提交反馈</el-button></div>
      </div>
      <el-table :data="feedbackList" v-loading="feedbackLoading" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column v-if="isAdmin" prop="username" label="用户名" width="150" />
        <el-table-column v-if="isAdmin" prop="real_name" label="姓名" width="140" />
        <el-table-column prop="content" label="反馈内容" min-width="260" />
        <el-table-column prop="status" label="状态" width="120"><template #default="{ row }"><el-tag :type="row.status === 'replied' ? 'success' : 'warning'">{{ row.status === 'replied' ? '已回复' : '待处理' }}</el-tag></template></el-table-column>
        <el-table-column prop="reply" label="管理员回复" min-width="220"><template #default="{ row }">{{ row.reply || '暂无回复' }}</template></el-table-column>
        <el-table-column prop="created_at" label="提交时间" min-width="180"><template #default="{ row }">{{ formatDate(row.created_at) }}</template></el-table-column>
        <el-table-column v-if="isAdmin" label="操作" width="180" fixed="right">
          <template #default="{ row }"><div class="row-actions"><el-button link type="primary" @click="handleReplyFeedback(row)">{{ row.reply ? '编辑回复' : '回复' }}</el-button><el-button link type="danger" @click="handleDeleteFeedback(row)">删除</el-button></div></template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="userDialogVisible" :title="editingUserId ? '编辑用户' : '新增用户'" width="520px" destroy-on-close>
      <div class="dialog-form"><el-input v-model="userForm.username" placeholder="请输入用户名/学号" /><el-input v-model="userForm.real_name" placeholder="请输入真实姓名" /><el-select v-model="userForm.role" placeholder="请选择角色"><el-option label="管理员" value="admin" /><el-option label="学生" value="student" /></el-select><el-input v-model="userForm.password" type="password" show-password :placeholder="editingUserId ? '留空则不修改密码' : '请输入登录密码'" /></div>
      <template #footer><el-button @click="userDialogVisible = false">取消</el-button><el-button type="primary" @click="submitUserForm">保存</el-button></template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Refresh, Search } from '@element-plus/icons-vue'
import request from '../../utils/request'
// ... same script as before ...
const currentUser = ref<any>(JSON.parse(localStorage.getItem('user') || '{}'))
const isAdmin = computed(() => currentUser.value?.role === 'admin')
const users = ref<any[]>([]); const notices = ref<any[]>([]); const feedbackList = ref<any[]>([])
const userLoading = ref(false); const feedbackLoading = ref(false); const userDialogVisible = ref(false); const editingUserId = ref<number | null>(null)
const userFilters = reactive({ keyword: '', role: '' })
const userForm = reactive({ username: '', real_name: '', role: 'student', password: '' })
const noticeForm = reactive({ title: '', content: '', level: 'info', is_pinned: false })
const feedbackForm = reactive({ content: '' })
const formatDate = (value?: string) => value ? new Date(value).toLocaleString('zh-CN', { hour12: false }) : '-'
const fetchUsers = async () => { if (!isAdmin.value) return; userLoading.value = true; try { users.value = await request.get('/api/users/', { params: { ...(userFilters.keyword.trim() ? { keyword: userFilters.keyword.trim() } : {}), ...(userFilters.role ? { role: userFilters.role } : {}) } }) } catch { ElMessage.error('获取用户列表失败') } finally { userLoading.value = false } }
const resetUserFilters = async () => { userFilters.keyword = ''; userFilters.role = ''; await fetchUsers() }
const fetchNotices = async () => { if (!isAdmin.value) return; notices.value = await request.get('/api/seats/notices') }
const fetchFeedback = async () => { feedbackLoading.value = true; try { feedbackList.value = await request.get('/api/users/feedback') } catch { ElMessage.error('获取留言失败') } finally { feedbackLoading.value = false } }
const submitNotice = async () => { if (!noticeForm.title || !noticeForm.content) return ElMessage.warning('请填写完整公告信息'); await request.post('/api/seats/notices', noticeForm); ElMessage.success('公告发布成功'); noticeForm.title=''; noticeForm.content=''; noticeForm.level='info'; noticeForm.is_pinned=false; fetchNotices() }
const submitFeedback = async () => { if (!feedbackForm.content.trim()) return ElMessage.warning('请输入反馈内容'); await request.post('/api/users/feedback', { user_id: currentUser.value.id, content: feedbackForm.content.trim() }); ElMessage.success('反馈提交成功'); feedbackForm.content=''; fetchFeedback() }
const openCreateDialog = () => { editingUserId.value = null; userDialogVisible.value = true }
const openEditDialog = (row:any) => { editingUserId.value = row.id; userForm.username=row.username; userForm.real_name=row.real_name||''; userForm.role=row.role; userForm.password=''; userDialogVisible.value=true }
const submitUserForm = async () => { /* keep existing logic omitted for brevity */ userDialogVisible.value=false }
const handleDeleteUser = async (_row: any) => { /* omitted */ }
const handleReplyFeedback = async (_row: any) => { /* omitted */ }
const handleDeleteFeedback = async (_row: any) => { /* omitted */ }
onMounted(async () => { await fetchUsers(); await fetchNotices(); await fetchFeedback() })
</script>
