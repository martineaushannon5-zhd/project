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
        <button
          v-for="item in notices"
          :key="item.id"
          type="button"
          class="notice-panel portal-hover"
          :class="{ pinned: item.is_pinned }"
          @click="openNotice(item)"
        >
          <div class="notice-head">
            <div class="notice-title-wrap">
              <el-tag v-if="item.is_pinned" size="small" type="danger" effect="dark">置顶</el-tag>
              <div class="notice-title">{{ item.title }}</div>
            </div>
            <el-tag size="small">{{ item.level }}</el-tag>
          </div>
          <div class="notice-content">{{ item.content }}</div>
          <div class="notice-hint">点击查看全文</div>
        </button>
      </div>
    </el-card>

    <el-dialog
      v-model="dialogVisible"
      width="min(760px, calc(100vw - 24px))"
      class="notice-dialog"
      :title="selectedNotice?.title || '公告详情'"
    >
      <div v-if="selectedNotice" class="notice-dialog-body">
        <div class="notice-dialog-hero" :class="{ pinned: selectedNotice.is_pinned }">
          <div class="notice-dialog-hero-top">
            <div class="notice-dialog-tags">
              <el-tag v-if="selectedNotice.is_pinned" size="small" type="danger" effect="dark">置顶公告</el-tag>
              <el-tag size="small" effect="light" :type="noticeTagType(selectedNotice.level)">
                {{ selectedNotice.level || 'info' }}
              </el-tag>
              <span class="notice-dialog-hero-label">Study Room Notice</span>
            </div>
            <span class="notice-dialog-hero-time">{{ formatTime(selectedNotice.created_at) }}</span>
          </div>
          <div class="notice-dialog-hero-title">{{ selectedNotice.title }}</div>
          <div class="notice-dialog-hero-desc">{{ noticeSummary(selectedNotice) }}</div>
          <div class="notice-dialog-metrics">
            <div class="notice-metric-card">
              <span>阅读建议</span>
              <strong>{{ noticeReadingMinutes(selectedNotice.content) }} 分钟</strong>
            </div>
            <div class="notice-metric-card">
              <span>当前进度</span>
              <strong>第 {{ selectedIndex + 1 }} / {{ notices.length }} 条</strong>
            </div>
            <div class="notice-metric-card">
              <span>浏览方式</span>
              <strong>支持左右切换</strong>
            </div>
          </div>
        </div>

        <div class="notice-dialog-content-card">
          <div class="notice-dialog-section-title">公告正文</div>
          <div class="notice-dialog-content">{{ selectedNotice.content }}</div>
        </div>

        <div class="notice-dialog-nav">
          <button
            type="button"
            class="notice-nav-card"
            :disabled="selectedIndex <= 0"
            @click="openPrevious"
          >
            <span>上一条</span>
            <strong>{{ previousNotice?.title || '已经是第一条公告' }}</strong>
          </button>
          <button
            type="button"
            class="notice-nav-card next"
            :disabled="selectedIndex >= notices.length - 1"
            @click="openNext"
          >
            <span>下一条</span>
            <strong>{{ nextNotice?.title || '已经是最后一条公告' }}</strong>
          </button>
        </div>

        <div class="notice-dialog-footer">
          <div class="notice-dialog-progress">
            可使用键盘 `←` / `→` 快速切换公告
          </div>
          <div class="notice-dialog-actions">
            <el-button :disabled="selectedIndex <= 0" @click="openPrevious">上一条</el-button>
            <el-button :disabled="selectedIndex >= notices.length - 1" @click="openNext">下一条</el-button>
            <el-button @click="goNoticeCenter">返回公告列表</el-button>
            <el-button type="primary" @click="goBooking">去预约座位</el-button>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import request from '../../utils/request'

interface NoticeItem {
  id: number
  title: string
  content: string
  level?: string
  created_at?: string
  is_pinned?: boolean
}

const router = useRouter()
const notices = ref<NoticeItem[]>([])
const selectedNotice = ref<NoticeItem | null>(null)
const dialogVisible = ref(false)
const selectedIndex = computed(() => notices.value.findIndex((item) => item.id === selectedNotice.value?.id))
const previousNotice = computed(() => {
  if (selectedIndex.value > 0) {
    return notices.value[selectedIndex.value - 1]
  }
  return null
})
const nextNotice = computed(() => {
  if (selectedIndex.value >= 0 && selectedIndex.value < notices.value.length - 1) {
    return notices.value[selectedIndex.value + 1]
  }
  return null
})

const openNotice = (item: NoticeItem) => {
  selectedNotice.value = item
  dialogVisible.value = true
}

const openPrevious = () => {
  if (selectedIndex.value > 0) {
    selectedNotice.value = notices.value[selectedIndex.value - 1]
  }
}

const openNext = () => {
  if (selectedIndex.value >= 0 && selectedIndex.value < notices.value.length - 1) {
    selectedNotice.value = notices.value[selectedIndex.value + 1]
  }
}

const noticeTagType = (level?: string) => {
  const map: Record<string, 'success' | 'warning' | 'info' | 'danger'> = {
    success: 'success',
    warning: 'warning',
    info: 'info',
    danger: 'danger'
  }
  return map[level || 'info'] || 'info'
}

const goBooking = () => {
  dialogVisible.value = false
  router.push('/portal/booking')
}

const goNoticeCenter = () => {
  dialogVisible.value = false
}

const formatTime = (value?: string) => {
  if (!value) return '未提供时间'
  const date = new Date(value)
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString()
}

const noticeReadingMinutes = (content = '') => {
  const length = content.trim().length
  return Math.max(1, Math.ceil(length / 180))
}

const noticeSummary = (item: NoticeItem) => {
  const summary = item.content.replace(/\s+/g, ' ').trim()
  return summary.length > 88 ? `${summary.slice(0, 88)}...` : summary
}

const handleKeydown = (event: KeyboardEvent) => {
  if (!dialogVisible.value) return
  if (event.key === 'ArrowLeft') {
    openPrevious()
  }
  if (event.key === 'ArrowRight') {
    openNext()
  }
}

onMounted(async () => {
  notices.value = await request.get('/api/seats/notices')
})

watch(dialogVisible, (visible) => {
  if (visible) {
    window.addEventListener('keydown', handleKeydown)
    return
  }
  window.removeEventListener('keydown', handleKeydown)
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
.notice-grid {
  display: grid;
  gap: 14px;
}
.notice-panel {
  appearance: none;
  width: 100%;
  border: none;
  text-align: left;
  cursor: pointer;
  padding: 18px;
  border-radius: 18px;
  background: #f8fbff;
  transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
}
.notice-panel.pinned {
  background: linear-gradient(180deg, #fff7ed, #fef3c7);
  border: 1px solid rgba(249, 115, 22, 0.12);
}
.notice-panel:hover,
.notice-panel:focus-visible {
  background: #f2f7ff;
  box-shadow: 0 14px 28px rgba(37, 99, 235, 0.08);
  outline: none;
  transform: translateY(-2px);
}
.notice-panel.pinned:hover,
.notice-panel.pinned:focus-visible {
  background: linear-gradient(180deg, #fff1df, #fde7b1);
}
.notice-head {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
}
.notice-title-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
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
.notice-hint {
  margin-top: 12px;
  color: #2563eb;
  font-size: 13px;
  font-weight: 700;
}
.notice-dialog-body {
  display: grid;
  gap: 16px;
}

.notice-dialog-hero {
  position: relative;
  overflow: hidden;
  padding: 20px;
  border-radius: 24px;
  background: linear-gradient(135deg, #eff6ff 0%, #f8fbff 52%, #f5f3ff 100%);
  border: 1px solid rgba(96, 165, 250, 0.16);
}
.notice-dialog-hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at top right, rgba(59, 130, 246, 0.16), transparent 28%),
    radial-gradient(circle at bottom left, rgba(124, 58, 237, 0.14), transparent 30%);
  pointer-events: none;
}
.notice-dialog-hero.pinned {
  background: linear-gradient(135deg, #fff7ed 0%, #fffaf0 54%, #fffbeb 100%);
  border-color: rgba(249, 115, 22, 0.18);
}
.notice-dialog-hero-top,
.notice-dialog-metrics {
  position: relative;
  z-index: 1;
}
.notice-dialog-hero-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}
.notice-dialog-hero-label,
.notice-dialog-hero-time {
  color: #64748b;
  font-size: 13px;
}
.notice-dialog-hero-title {
  position: relative;
  z-index: 1;
  margin-top: 14px;
  font-size: 28px;
  line-height: 1.25;
  font-weight: 800;
  color: #0f172a;
}
.notice-dialog-hero-desc {
  position: relative;
  z-index: 1;
  margin-top: 10px;
  color: #475569;
  line-height: 1.8;
}
.notice-dialog-metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-top: 18px;
}
.notice-metric-card {
  padding: 14px 16px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.78);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.7);
}
.notice-metric-card span {
  display: block;
  color: #64748b;
  font-size: 12px;
}
.notice-metric-card strong {
  display: block;
  margin-top: 6px;
  color: #0f172a;
  font-size: 15px;
}
.notice-dialog-content-card {
  padding: 18px 20px;
  border-radius: 22px;
  background: linear-gradient(180deg, #ffffff, #f8fbff);
  border: 1px solid rgba(148, 163, 184, 0.12);
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.8);
}
.notice-dialog-section-title {
  margin-bottom: 12px;
  color: #0f172a;
  font-size: 14px;
  font-weight: 800;
}
.notice-dialog-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  color: #64748b;
  font-size: 13px;
}
.notice-dialog-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.notice-dialog-content {
  white-space: pre-wrap;
  color: #334155;
  line-height: 1.9;
}
.notice-dialog-nav {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}
.notice-nav-card {
  appearance: none;
  width: 100%;
  text-align: left;
  border: 1px solid rgba(148, 163, 184, 0.16);
  background: #f8fbff;
  border-radius: 20px;
  padding: 16px 18px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.notice-nav-card.next {
  background: linear-gradient(180deg, #f8fbff, #eef4ff);
}
.notice-nav-card:hover:not(:disabled),
.notice-nav-card:focus-visible:not(:disabled) {
  transform: translateY(-2px);
  border-color: rgba(37, 99, 235, 0.2);
  box-shadow: 0 12px 26px rgba(37, 99, 235, 0.08);
  outline: none;
}
.notice-nav-card:disabled {
  opacity: 0.56;
  cursor: not-allowed;
}
.notice-nav-card span {
  display: block;
  color: #64748b;
  font-size: 12px;
}
.notice-nav-card strong {
  display: block;
  margin-top: 8px;
  color: #0f172a;
  line-height: 1.5;
}
.notice-dialog-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding-top: 4px;
}
.notice-dialog-progress {
  color: #64748b;
  font-size: 13px;
}
.notice-dialog-actions {
  display: flex;
  gap: 10px;
}
@media (max-width: 768px) {
  .notice-dialog-footer,
  .notice-dialog-meta {
    flex-direction: column;
    align-items: flex-start;
  }
  .notice-dialog-hero-top,
  .notice-dialog-metrics,
  .notice-dialog-nav {
    grid-template-columns: 1fr;
  }
  .notice-dialog-actions {
    width: 100%;
    flex-wrap: wrap;
  }
}
</style>
