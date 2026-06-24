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
            <span>座位预约</span>
            <span>公告通知</span>
            <span>我的预约</span>
            <span>反馈留言</span>
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
          <div v-for="item in notices.slice(0, 4)" :key="item.id" class="notice-item">
            <div class="notice-top">
              <div class="notice-dot"></div>
              <div class="notice-title">{{ item.title }}</div>
              <el-tag size="small" :type="noticeTagType(item.level)">{{ item.level || 'info' }}</el-tag>
            </div>
            <div class="notice-content">{{ item.content }}</div>
          </div>
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
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import request from '../../utils/request'
import * as echarts from 'echarts'
import { Calendar, Bowl, EditPen, Tickets, Bell, ChatDotRound } from '@element-plus/icons-vue'

const router = useRouter()
const stats = ref<any>({
  today_reservations: 0,
  free_seats: 0,
  seat_usage_rate: 0,
  trend_labels: [],
  trend_data: []
})
const notices = ref<any[]>([])
const trendRef = ref<HTMLDivElement | null>(null)
let chart: echarts.ECharts | null = null

const go = (path: string) => router.push(path)

const noticeTagType = (level: string) => {
  const map: Record<string, any> = {
    success: 'success',
    warning: 'warning',
    info: 'info'
  }
  return map[level] || 'info'
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

.hero-tags span {
  padding: 9px 14px;
  border-radius: 999px;
  background: rgba(255,255,255,0.72);
  color: #334155;
  border: 1px solid rgba(148,163,184,0.16);
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
  padding: 16px;
  border-radius: 18px;
  background: linear-gradient(180deg, #f8fbff, #eef4ff);
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

.notice-content {
  margin-top: 10px;
  color: #64748b;
  line-height: 1.7;
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
}
</style>
