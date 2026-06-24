<template>
  <div class="portal-shell">
    <el-card class="portal-card portal-hover">
      <template #header>
        <div>
          <div class="portal-section-title">公告通知</div>
          <div class="portal-section-subtitle">查看最新校园通知与自习室公告。</div>
        </div>
      </template>

      <div class="notice-grid">
        <div v-for="item in notices" :key="item.id" class="notice-panel portal-hover">
          <div class="notice-head">
            <div class="notice-title">{{ item.title }}</div>
            <el-tag size="small">{{ item.level }}</el-tag>
          </div>
          <div class="notice-content">{{ item.content }}</div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import request from '../../utils/request'

const notices = ref<any[]>([])

onMounted(async () => {
  notices.value = await request.get('/api/seats/notices')
})
</script>

<style scoped>
.notice-grid {
  display: grid;
  gap: 14px;
}
.notice-panel {
  padding: 18px;
  border-radius: 18px;
  background: #f8fbff;
}
.notice-head {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
}
.notice-title {
  font-weight: 800;
  color: #0f172a;
}
.notice-content {
  margin-top: 10px;
  color: #64748b;
  line-height: 1.7;
}
</style>
