<template>
  <div class="portal-home">
    <section class="art-hero portal-fade-up">
      <div class="art-orb art-orb-1"></div>
      <div class="art-orb art-orb-2"></div>
      <div class="hero-content">
        <div class="hero-copy">
          <div class="hero-kicker">Campus Study Space</div>
          <h1>让每一次自习，都拥有更好的位置与节奏</h1>
          <p>
            学生门户首页以“轻盈、艺术、清爽”为核心，快速查看公告、预约入口、推荐自习室与个人使用情况，
            让你在学习前就先感受到秩序与安静。
          </p>

          <div class="hero-actions">
            <el-button type="primary" size="large" class="primary-btn" @click="go('/portal/booking')">
              立即选座
            </el-button>
            <el-button size="large" class="ghost-btn" @click="go('/portal/notices')">
              查看公告
            </el-button>
          </div>

          <div class="hero-tags">
            <button
              v-for="entry in quickLinks"
              :key="entry.path"
              type="button"
              class="hero-tag-button"
              @click="go(entry.path)"
            >
              {{ entry.label }}
            </button>
          </div>
        </div>

        <div class="hero-visual">
          <div class="glass-panel floating-card">
            <div class="glass-title">今日概览</div>
            <div class="glass-grid">
              <div>
                <span>今日预约</span>
                <strong>{{ stats.today_reservations }}</strong>
              </div>
              <div>
                <span>可用座位</span>
                <strong>{{ stats.free_seats }}</strong>
              </div>
              <div>
                <span>公告数量</span>
                <strong>{{ notices.length }}</strong>
              </div>
              <div>
                <span>占用率</span>
                <strong>{{ stats.seat_usage_rate }}%</strong>
              </div>
            </div>
          </div>

          <div class="mini-card card-a floating-card">
            <el-icon><Calendar /></el-icon>
            <div>
              <span>推荐预约</span>
              <strong>今天 18:00-22:00</strong>
            </div>
          </div>

          <div class="mini-card card-b floating-card">
            <el-icon><Bowl /></el-icon>
            <div>
              <span>学习氛围</span>
              <strong>安静 · 稳定 · 舒适</strong>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="portal-section">
      <div class="section-head">
        <div>
          <div class="portal-section-title">快捷入口</div>
          <div class="portal-section-subtitle">像浏览一个高质感网站一样，快速进入常用功能。</div>
        </div>
      </div>

      <div class="feature-grid">
        <div class="feature-card portal-hover feature-one" @click="go('/portal/booking')">
          <div class="feature-icon"><EditPen /></div>
          <div class="feature-title">自习室预约</div>
          <div class="feature-desc">从自习室到座位，直接完成预约。</div>
        </div>

        <div class="feature-card portal-hover feature-two" @click="go('/portal/my-reservations')">
          <div class="feature-icon"><Tickets /></div>
          <div class="feature-title">我的预约</div>
          <div class="feature-desc">查看预约状态、签到、取消。</div>
        </div>

        <div class="feature-card portal-hover feature-three" @click="go('/portal/notices')">
          <div class="feature-icon"><Bell /></div>
          <div class="feature-title">公告通知</div>
          <div class="feature-desc">掌握最新通知与系统动态。</div>
        </div>

        <div class="feature-card portal-hover feature-four" @click="go('/portal/feedback')">
          <div class="feature-icon"><ChatDotRound /></div>
          <div class="feature-title">意见反馈</div>
          <div class="feature-desc">提交建议，让系统更好用。</div>
        </div>
      </div>
    </section>

    <section class="portal-section split-layout">
      <el-card class="soft-card portal-hover notice-panel" shadow="hover">
        <template #header>
          <div class="card-header">
            <div>
              <div class="card-title">最新公告</div>
              <div class="card-subtitle">重要通知会优先展示在这里</div>
            </div>
            <el-button text @click="go('/portal/notices')">更多</el-button>
          </div>
        </template>

        <div class="notice-list">
          <button
            v-for="item in notices.slice(0, 4)"
            :key="item.id"
            type="button"
            class="notice-item"
            :class="{ pinned: item.is_pinned }"
            @click="openNotice(item)"
          >
            <div class="notice-top">
              <div class="notice-dot"></div>
              <div class="notice-title-wrap">
                <el-tag v-if="item.is_pinned" size="small" type="danger" effect="dark">置顶</el-tag>
                <div class="notice-title">{{ item.title }}</div>
              </div>
              <el-tag size="small" :type="noticeTagType(item.level)">{{ item.level || 'info' }}</el-tag>
            </div>
            <div class="notice-content">{{ item.content }}</div>
            <div class="notice-more">点击查看全文</div>
          </button>
        </div>
      </el-card>

      <el-card class="soft-card portal-hover chart-panel" shadow="hover">
        <template #header>
          <div class="card-header">
            <div>
              <div class="card-title">近七日预约趋势</div>
              <div class="card-subtitle">用数据感受校园学习空间的使用节奏</div>
            </div>
          </div>
        </template>
        <div ref="trendRef" class="chart-box"></div>
      </el-card>
    </section>

    <el-dialog
      v-model="noticeDialogVisible"
      width="min(760px, calc(100vw - 24px))"
      class="notice-dialog"
      :title="selectedNotice?.title || '公告详情'"
    >
      <div v-if="selectedNotice" class="notice-dialog-body">
        <div class="notice-dialog-hero" :class="{ pinned: selectedNotice.is_pinned }">
          <div class="notice-dialog-hero-top">
            <div class="notice-dialog-tags">
              <el-tag v-if="selectedNotice.is_pinned" size="small" type="danger" effect="dark">置顶公告</el-tag>
              <el-tag size="small" effect="light" :type="noticeTagType(selectedNotice.level || 'info')">
                {{ selectedNotice.level || 'info' }}
              </el-tag>
              <span class="notice-dialog-hero-label">Campus Notice</span>
            </div>
            <span class="notice-dialog-hero-time">{{ formatTime(selectedNotice.created_at) }}</span>
          </div>
          <div class="notice-dialog-hero-title">{{ selectedNotice.title }}</div>
          <div class="notice-dialog-hero-desc">
            {{ noticeSummary(selectedNotice) }}
          </div>
          <div class="notice-dialog-metrics">
            <div class="notice-metric-card">
              <span>阅读建议</span>
              <strong>{{ noticeReadingMinutes(selectedNotice.content) }} 分钟</strong>
            </div>
            <div class="notice-metric-card">
              <span>当前进度</span>
              <strong>第 {{ selectedNoticeIndex + 1 }} / {{ notices.length }} 条</strong>
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
            :disabled="selectedNoticeIndex <= 0"
            @click="openPreviousNotice"
          >
            <span>上一条</span>
            <strong>{{ previousNotice?.title || '已经是第一条公告' }}</strong>
          </button>
          <button
            type="button"
            class="notice-nav-card next"
            :disabled="selectedNoticeIndex >= notices.length - 1"
            @click="openNextNotice"
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
            <el-button :disabled="selectedNoticeIndex <= 0" @click="openPreviousNotice">上一条</el-button>
            <el-button :disabled="selectedNoticeIndex >= notices.length - 1" @click="openNextNotice">下一条</el-button>
            <el-button @click="goNoticeCenter">进入公告中心</el-button>
            <el-button type="primary" @click="goBooking">去预约座位</el-button>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import request from '../../utils/request'
import * as echarts from 'echarts'
import { Calendar, Bowl, EditPen, Tickets, Bell, ChatDotRound } from '@element-plus/icons-vue'

interface NoticeItem {
  id: number
  title: string
  content: string
  level?: string
  created_at?: string
  is_pinned?: boolean
}

const router = useRouter()
const quickLinks = [
  { label: '座位预约', path: '/portal/booking' },
  { label: '公告通知', path: '/portal/notices' },
  { label: '我的预约', path: '/portal/my-reservations' },
  { label: '反馈留言', path: '/portal/feedback' }
]
const stats = ref<any>({
  today_reservations: 0,
  free_seats: 0,
  seat_usage_rate: 0,
  trend_labels: [],
  trend_data: []
})
const notices = ref<NoticeItem[]>([])
const trendRef = ref<HTMLDivElement | null>(null)
const selectedNotice = ref<NoticeItem | null>(null)
const noticeDialogVisible = ref(false)
const selectedNoticeIndex = computed(() => notices.value.findIndex((item) => item.id === selectedNotice.value?.id))
const previousNotice = computed(() => {
  if (selectedNoticeIndex.value > 0) {
    return notices.value[selectedNoticeIndex.value - 1]
  }
  return null
})
const nextNotice = computed(() => {
  if (selectedNoticeIndex.value >= 0 && selectedNoticeIndex.value < notices.value.length - 1) {
    return notices.value[selectedNoticeIndex.value + 1]
  }
  return null
})
let chart: echarts.ECharts | null = null

const go = (path: string) => router.push(path)
const openNotice = (item: NoticeItem) => {
  selectedNotice.value = item
  noticeDialogVisible.value = true
}
const openPreviousNotice = () => {
  if (selectedNoticeIndex.value > 0) {
    selectedNotice.value = notices.value[selectedNoticeIndex.value - 1]
  }
}

const openNextNotice = () => {
  if (selectedNoticeIndex.value >= 0 && selectedNoticeIndex.value < notices.value.length - 1) {
    selectedNotice.value = notices.value[selectedNoticeIndex.value + 1]
  }
}

const noticeTagType = (level?: string) => {
  const map: Record<string, any> = {
    success: 'success',
    warning: 'warning',
    info: 'info'
  }
  const key = level || 'info'
  return map[key] || 'info'
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

const goNoticeCenter = () => {
  noticeDialogVisible.value = false
  router.push('/portal/notices')
}

const goBooking = () => {
  noticeDialogVisible.value = false
  router.push('/portal/booking')
}

const handleNoticeKeydown = (event: KeyboardEvent) => {
  if (!noticeDialogVisible.value) return
  if (event.key === 'ArrowLeft') {
    openPreviousNotice()
  }
  if (event.key === 'ArrowRight') {
    openNextNotice()
  }
}

const loadData = async () => {
  const [statRes, noticeRes] = await Promise.all([
    request.get('/api/seats/stats'),
    request.get('/api/seats/notices')
  ])
  stats.value = statRes as any
  notices.value = (noticeRes as any) || []
  await nextTick()
  initChart()
}

const initChart = () => {
  if (!trendRef.value) return
  chart?.dispose()
  chart = echarts.init(trendRef.value)
  chart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: 20, right: 18, top: 20, bottom: 20, containLabel: true },
    xAxis: {
      type: 'category',
      data: stats.value.trend_labels,
      axisLine: { lineStyle: { color: '#dbeafe' } },
      axisTick: { show: false },
      axisLabel: { color: '#64748b' }
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { type: 'dashed', color: '#edf2f7' } },
      axisLabel: { color: '#64748b' }
    },
    series: [
      {
        type: 'line',
        smooth: true,
        data: stats.value.trend_data,
        symbol: 'circle',
        symbolSize: 8,
        lineStyle: {
          width: 4,
          color: '#2563eb'
        },
        itemStyle: { color: '#2563eb' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(37,99,235,0.34)' },
            { offset: 1, color: 'rgba(37,99,235,0.03)' }
          ])
        }
      }
    ]
  })
}

onMounted(loadData)

watch(noticeDialogVisible, (visible) => {
  if (visible) {
    window.addEventListener('keydown', handleNoticeKeydown)
    return
  }
  window.removeEventListener('keydown', handleNoticeKeydown)
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleNoticeKeydown)
})
</script>

<style scoped>
.portal-home {
  position: relative;
}

.art-hero {
  position: relative;
  overflow: hidden;
  border-radius: 32px;
  padding: 28px;
  background: linear-gradient(135deg, #eaf2ff 0%, #f7f9ff 40%, #eef7ff 100%);
  border: 1px solid rgba(37, 99, 235, 0.10);
  box-shadow: 0 24px 60px rgba(37, 99, 235, 0.10);
}

.art-hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top right, rgba(124,58,237,0.12), transparent 28%),
              radial-gradient(circle at bottom left, rgba(37,99,235,0.14), transparent 24%);
  pointer-events: none;
}

.art-orb {
  position: absolute;
  border-radius: 999px;
  filter: blur(4px);
  opacity: 0.75;
}

.art-orb-1 {
  width: 180px;
  height: 180px;
  right: -40px;
  top: -24px;
  background: radial-gradient(circle, rgba(59,130,246,0.28), rgba(59,130,246,0));
}

.art-orb-2 {
  width: 240px;
  height: 240px;
  left: 26%;
  bottom: -110px;
  background: radial-gradient(circle, rgba(124,58,237,0.16), rgba(124,58,237,0));
}

.hero-content {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 28px;
  align-items: center;
}

.hero-kicker {
  display: inline-flex;
  padding: 8px 14px;
  border-radius: 999px;
  background: rgba(37,99,235,0.10);
  color: #1d4ed8;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.hero-copy h1 {
  margin: 16px 0 14px;
  font-size: 44px;
  line-height: 1.15;
  color: #0f172a;
  letter-spacing: -0.02em;
}

.hero-copy p {
  margin: 0;
  max-width: 760px;
  color: #475569;
  line-height: 1.8;
  font-size: 16px;
}

.hero-actions {
  display: flex;
  gap: 14px;
  margin-top: 26px;
}

.primary-btn,
.ghost-btn {
  border-radius: 999px;
  padding: 0 22px;
  height: 46px;
}

.hero-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 24px;
}

.hero-tag-button {
  appearance: none;
  border: 1px solid rgba(148, 163, 184, 0.16);
  background: rgba(255,255,255,0.72);
  cursor: pointer;
  font: inherit;
  transition: all 0.2s ease;
}

.hero-tag-button:hover,
.hero-tag-button:focus-visible {
  background: #ffffff;
  color: #1d4ed8;
  border-color: rgba(37, 99, 235, 0.26);
  box-shadow: 0 8px 18px rgba(37, 99, 235, 0.12);
  outline: none;
  transform: translateY(-1px);
}

.hero-tags span,
.hero-tag-button {
  padding: 9px 14px;
  border-radius: 999px;
  color: #334155;
}

.hero-visual {
  position: relative;
  min-height: 360px;
}

.glass-panel {
  position: absolute;
  right: 24px;
  top: 0;
  width: min(100%, 340px);
  padding: 20px;
  border-radius: 24px;
  background: rgba(255,255,255,0.72);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255,255,255,0.6);
  box-shadow: 0 18px 42px rgba(37,99,235,0.12);
}

.glass-title {
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 16px;
}

.glass-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.glass-grid div {
  padding: 14px;
  border-radius: 18px;
  background: linear-gradient(180deg, #f8fbff, #eef4ff);
}

.glass-grid span,
.mini-card span {
  display: block;
  font-size: 12px;
  color: #64748b;
}

.glass-grid strong {
  display: block;
  margin-top: 8px;
  font-size: 26px;
  color: #0f172a;
}

.mini-card {
  position: absolute;
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 230px;
  padding: 16px 18px;
  border-radius: 22px;
  background: rgba(255,255,255,0.84);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(148,163,184,0.15);
  box-shadow: 0 18px 34px rgba(15,23,42,0.08);
}

.mini-card strong {
  display: block;
  margin-top: 4px;
  font-size: 14px;
  color: #0f172a;
}

.mini-card .el-icon {
  width: 42px;
  height: 42px;
  border-radius: 14px;
  display: grid;
  place-items: center;
  font-size: 20px;
  color: #fff;
}

.card-a {
  left: 24px;
  top: 120px;
}

.card-a .el-icon {
  background: linear-gradient(135deg, #2563eb, #60a5fa);
}

.card-b {
  right: 8px;
  bottom: 4px;
}

.card-b .el-icon {
  background: linear-gradient(135deg, #7c3aed, #a78bfa);
}

.portal-section {
  margin-top: 22px;
}

.section-head {
  display: flex;
  justify-content: space-between;
  align-items: end;
  margin-bottom: 16px;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}

.feature-card {
  padding: 22px;
  border-radius: 24px;
  background: rgba(255,255,255,0.78);
  border: 1px solid rgba(148,163,184,0.12);
  box-shadow: 0 16px 30px rgba(15,23,42,0.06);
  cursor: pointer;
}

.feature-icon {
  width: 52px;
  height: 52px;
  border-radius: 18px;
  display: grid;
  place-items: center;
  color: #fff;
  font-size: 24px;
  margin-bottom: 16px;
  box-shadow: 0 14px 28px rgba(37, 99, 235, 0.16);
}

.feature-title {
  font-size: 18px;
  font-weight: 800;
  color: #0f172a;
}

.feature-desc {
  margin-top: 8px;
  color: #64748b;
  line-height: 1.7;
}

.feature-one .feature-icon { background: linear-gradient(135deg, #2563eb, #60a5fa); }
.feature-two .feature-icon { background: linear-gradient(135deg, #0ea5e9, #38bdf8); }
.feature-three .feature-icon { background: linear-gradient(135deg, #8b5cf6, #a78bfa); }
.feature-four .feature-icon { background: linear-gradient(135deg, #14b8a6, #5eead4); }

.split-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}

.soft-card {
  border: none;
  border-radius: 26px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 18px;
  font-weight: 800;
  color: #0f172a;
}

.card-subtitle {
  margin-top: 4px;
  color: #64748b;
  font-size: 13px;
}

.notice-list {
  display: grid;
  gap: 12px;
}

.notice-item {
  appearance: none;
  width: 100%;
  border: none;
  text-align: left;
  cursor: pointer;
  padding: 16px;
  border-radius: 18px;
  background: linear-gradient(180deg, #f8fbff, #eef4ff);
  transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
}
.notice-item.pinned {
  background: linear-gradient(180deg, #fff7ed, #fef3c7);
  border: 1px solid rgba(249, 115, 22, 0.12);
}

.notice-item:hover,
.notice-item:focus-visible {
  background: linear-gradient(180deg, #f4f8ff, #e8f0ff);
  box-shadow: 0 14px 28px rgba(37, 99, 235, 0.08);
  outline: none;
  transform: translateY(-2px);
}
.notice-item.pinned:hover,
.notice-item.pinned:focus-visible {
  background: linear-gradient(180deg, #fff1df, #fde7b1);
}

.notice-top {
  display: flex;
  align-items: center;
  gap: 10px;
}

.notice-dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  box-shadow: 0 0 0 6px rgba(37,99,235,0.08);
}

.notice-title {
  flex: 1;
  font-weight: 800;
  color: #0f172a;
}

.notice-title-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
  flex: 1;
}

.notice-content {
  margin-top: 10px;
  color: #64748b;
  line-height: 1.7;
}

.notice-more {
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
  flex-wrap: wrap;
  gap: 10px;
}

.chart-box {
  width: 100%;
  height: 320px;
}

.floating-card {
  animation: floatY 6s ease-in-out infinite;
}

.floating-card.card-b {
  animation-delay: 0.8s;
}

@keyframes floatY {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

@media (max-width: 1200px) {
  .feature-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .split-layout,
  .hero-content {
    grid-template-columns: 1fr;
  }

  .hero-visual {
    min-height: 300px;
  }
}

@media (max-width: 768px) {
  .art-hero {
    padding: 18px;
  }

  .hero-copy h1 {
    font-size: 30px;
  }

  .feature-grid {
    grid-template-columns: 1fr;
  }

  .hero-actions {
    flex-direction: column;
  }

  .glass-panel,
  .mini-card {
    position: static;
    width: 100%;
    margin-top: 14px;
  }

  .hero-visual {
    min-height: auto;
    display: grid;
    gap: 12px;
  }

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
}
</style>
