<template>
  <div class="portal-shell">
    <el-card class="portal-card portal-hover">
      <template #header>
        <div>
          <div class="portal-section-title">意见反馈 / 留言</div>
          <div class="portal-section-subtitle">提交你的建议，帮助我们持续优化自习室系统。</div>
        </div>
      </template>

      <div class="feedback-layout">
        <div class="feedback-form-panel">
          <el-form :model="form" label-position="top">
            <el-form-item label="留言内容">
              <el-input
                v-model="form.content"
                type="textarea"
                :rows="6"
                placeholder="请输入你对系统、预约体验或自习室环境的建议"
              />
            </el-form-item>
            <el-button type="primary" size="large" @click="submitFeedback">提交反馈</el-button>
          </el-form>
        </div>

        <div class="feedback-tips">
          <div class="tip-card">
            <div class="tip-title">建议类型</div>
            <div class="tip-text">功能建议、页面优化、座位体验、公告提醒等都可以提交。</div>
          </div>
          <div class="tip-card">
            <div class="tip-title">提交后</div>
            <div class="tip-text">管理员可在后台查看留言并进行回复，形成闭环反馈。</div>
          </div>
          <div class="tip-card">
            <div class="tip-title">小提示</div>
            <div class="tip-text">描述越具体，越有助于快速定位并改进问题。</div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import request from '../../utils/request'
import { ElMessage } from 'element-plus'

const user = JSON.parse(localStorage.getItem('user') || '{}')
const form = reactive({ content: '' })

const submitFeedback = async () => {
  if (!form.content.trim()) {
    ElMessage.warning('请输入反馈内容')
    return
  }
  await request.post('/api/users/feedback', { user_id: user.id, content: form.content })
  ElMessage.success('反馈提交成功')
  form.content = ''
}
</script>

<style scoped>
.feedback-layout {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 18px;
}
.feedback-form-panel,
.tip-card {
  padding: 18px;
  border-radius: 18px;
  background: linear-gradient(180deg, #f8fbff, #eef4ff);
}
.feedback-tips {
  display: grid;
  gap: 14px;
}
.tip-title {
  font-weight: 800;
  color: #ffffff;
}
.tip-text {
  margin-top: 8px;
  color: #ffffff;
  line-height: 1.7;
}
@media (max-width: 960px) {
  .feedback-layout { grid-template-columns: 1fr; }
}
</style>
