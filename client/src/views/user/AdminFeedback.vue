<template>
  <div class="feedback-admin-page">
    <section class="hero-card portal-fade-up">
      <div class="hero-copy">
        <div class="hero-badge">Feedback Center</div>
        <h1>反馈处理中心</h1>
        <p>集中查看学生反馈、快速回复留言、跟踪处理状态，让后台沟通闭环更高效。</p>
      </div>
      <div class="hero-stats">
        <div class="stat-box"><span>总留言</span><strong>{{ stats.total }}</strong></div>
        <div class="stat-box"><span>待处理</span><strong>{{ stats.pending }}</strong></div>
        <div class="stat-box"><span>已回复</span><strong>{{ stats.replied }}</strong></div>
      </div>
    </section>

    <el-card class="panel-card portal-hover" shadow="hover">
      <template #header>
        <div class="panel-header">
          <div>
            <div class="panel-title">留言列表</div>
            <div class="panel-subtitle">点击回复按钮进行快速处理。</div>
          </div>
          <el-button :icon="Refresh" @click="fetchFeedback">刷新</el-button>
        </div>
      </template>

      <div class="toolbar">
        <el-input v-model="keyword" placeholder="搜索内容、用户名或姓名" clearable>
          <template #prefix><el-icon><Search /></el-icon></template>
        </el-input>
        <el-select v-model="statusFilter" placeholder="全部状态" clearable>
          <el-option label="待处理" value="pending" />
          <el-option label="已回复" value="replied" />
        </el-select>
        <el-button type="primary" @click="fetchFeedback">筛选</el-button>
      </div>

      <div class="feedback-grid">
        <article v-for="item in filteredFeedback" :key="item.id" class="feedback-card">
          <div class="feedback-top">
            <div>
              <div class="feedback-name">{{ item.real_name || item.username || '匿名留言' }}</div>
              <div class="feedback-meta">{{ formatDate(item.created_at) }}</div>
            </div>
            <el-tag :type="item.status === 'replied' ? 'success' : 'warning'">{{ item.status === 'replied' ? '已回复' : '待处理' }}</el-tag>
          </div>

          <div class="feedback-content">{{ item.content }}</div>

          <div class="reply-box" v-if="item.reply">
            <span class="reply-label">管理员回复</span>
            <p>{{ item.reply }}</p>
          </div>

          <div class="feedback-actions">
            <el-button type="primary" plain @click="reply(item)">{{ item.reply ? '编辑回复' : '回复留言' }}</el-button>
            <el-button type="danger" plain @click="remove(item)">删除</el-button>
          </div>
        </article>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh, Search } from '@element-plus/icons-vue'
import request from '../../utils/request'

const feedbackList = ref<any[]>([])
const keyword = ref('')
const statusFilter = ref('')
const stats = computed(() => ({
  total: feedbackList.value.length,
  pending: feedbackList.value.filter((i) => i.status !== 'replied').length,
  replied: feedbackList.value.filter((i) => i.status === 'replied').length
}))

const filteredFeedback = computed(() => {
  const kw = keyword.value.trim().toLowerCase()
  return feedbackList.value.filter((item) => {
    const matchedKeyword = !kw || [item.username, item.real_name, item.content, item.reply].some((v) => String(v || '').toLowerCase().includes(kw))
    const matchedStatus = !statusFilter.value || item.status === statusFilter.value
    return matchedKeyword && matchedStatus
  })
})

const fetchFeedback = async () => {
  try { feedbackList.value = await request.get('/api/users/feedback') } catch { ElMessage.error('获取反馈失败') }
}
const formatDate = (v?: string) => v ? new Date(v).toLocaleString('zh-CN', { hour12: false }) : '-'
const reply = async (item:any) => {
  const { value } = await ElMessageBox.prompt('请输入回复内容', '回复留言', { inputType: 'textarea', inputValue: item.reply || '', confirmButtonText: '提交' })
  await request.post(`/api/users/feedback/${item.id}/reply`, { reply: value })
  ElMessage.success('回复成功')
  fetchFeedback()
}
const remove = async (item:any) => {
  await ElMessageBox.confirm('确认删除这条留言吗？', '提示', { type: 'warning' })
  await request.delete(`/api/users/feedback/${item.id}`)
  ElMessage.success('删除成功')
  fetchFeedback()
}
onMounted(fetchFeedback)
</script>

<style scoped>
.feedback-admin-page { display:flex; flex-direction:column; gap:20px; }
.hero-card { border:none; border-radius:28px; padding:28px; color:#fff; background: linear-gradient(135deg, #2563eb, #7c3aed); display:flex; justify-content:space-between; gap:20px; }
.hero-copy h1 { margin:10px 0 8px; font-size:30px; font-weight:900; }
.hero-copy p { margin:0; opacity:.92; max-width:680px; }
.hero-badge { display:inline-flex; padding:6px 12px; border-radius:999px; background:rgba(255,255,255,.16); }
.hero-stats { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:12px; min-width:320px; }
.stat-box { padding:16px; border-radius:18px; background:rgba(255,255,255,.14); }
.stat-box span { display:block; font-size:12px; opacity:.8; }
.stat-box strong { display:block; margin-top:6px; font-size:26px; font-weight:900; }
.panel-card { border:none; border-radius:24px; }
.panel-header { display:flex; justify-content:space-between; align-items:center; gap:16px; }
.panel-title { font-size:18px; font-weight:800; color:#0f172a; }
.panel-subtitle { margin-top:4px; color:#64748b; font-size:12px; }
.toolbar { display:grid; grid-template-columns: 1.3fr .8fr auto; gap:12px; margin-bottom:18px; }
.feedback-grid { display:grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap:16px; }
.feedback-card { padding:18px; border-radius:22px; border:1px solid rgba(148,163,184,.14); background: linear-gradient(180deg, #fff, #f8fbff); box-shadow:0 12px 26px rgba(15,23,42,.04); }
.feedback-top { display:flex; justify-content:space-between; gap:12px; align-items:flex-start; }
.feedback-name { font-weight:800; color:#0f172a; }
.feedback-meta { color:#64748b; font-size:12px; margin-top:4px; }
.feedback-content { margin-top:14px; color:#334155; line-height:1.8; white-space:pre-wrap; }
.reply-box { margin-top:14px; padding:14px; border-radius:16px; background:#eef4ff; }
.reply-label { display:block; font-size:12px; color:#2563eb; font-weight:700; margin-bottom:6px; }
.reply-box p { margin:0; color:#1e293b; line-height:1.7; }
.feedback-actions { display:flex; gap:10px; margin-top:16px; flex-wrap:wrap; }
@media (max-width: 960px) { .feedback-grid, .hero-card { grid-template-columns:1fr; display:grid; } .toolbar { grid-template-columns:1fr; } .hero-stats { min-width:unset; } }
</style>
