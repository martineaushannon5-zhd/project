<template>
  <div class="dashboard-page">
    <section class="dashboard-hero portal-fade-up">
      <div class="hero-orb hero-orb-a"></div>
      <div class="hero-orb hero-orb-b"></div>
      <div class="hero-main">
        <div class="hero-copy">
          <div class="hero-badge">运营后台 · 数据总览</div>
          <h2 class="hero-title">让后台首页更像一个高级产品，而不是一块生硬的报表墙</h2>
          <p class="hero-desc">
            把预约趋势、空间热度、座位利用率和运营重点整合到同一个首页，减少无效块级占位，让管理员一打开后台就能抓住重点。
          </p>
          <div class="hero-pills">
            <div class="hero-pill live-pill">
              <span class="hero-pill-dot"></span>
              系统稳定运行
            </div>
            <div class="hero-pill">{{ heroInsight }}</div>
            <div class="hero-pill">当前占用 {{ usagePercent }}%</div>
          </div>
          <div class="hero-action-row">
            <el-button type="primary" size="large" class="hero-primary-btn" @click="go('/admin/rooms')">
              管理自习室
            </el-button>
            <el-button size="large" class="hero-secondary-btn" @click="go('/admin/user')">
              查看用户
            </el-button>
            <el-button size="large" text @click="go('/admin/booking')">进入预约管理</el-button>
          </div>
        </div>

        <div class="hero-side">
          <div class="focus-card">
            <div class="focus-top">
              <div>
                <div class="focus-label">核心运行指数</div>
                <div class="focus-value">{{ usagePercent }}%</div>
              </div>
              <div class="focus-badge">{{ stats.active_now }} 人在馆</div>
            </div>
            <div class="focus-progress">
              <span :style="{ width: `${usagePercent}%` }"></span>
            </div>
            <div class="focus-grid">
              <div class="focus-metric">
                <span>已占用座位</span>
                <strong>{{ occupiedSeats }}</strong>
              </div>
              <div class="focus-metric">
                <span>空闲座位</span>
                <strong>{{ stats.free_seats }}</strong>
              </div>
              <div class="focus-metric">
                <span>今日完成</span>
                <strong>{{ stats.completed_today }}</strong>
              </div>
              <div class="focus-metric">
                <span>自习室数量</span>
                <strong>{{ stats.total_rooms }}</strong>
              </div>
            </div>
          </div>

          <div class="hero-mini-grid">
            <div class="hero-mini-card">
              <span>预约峰值日</span>
              <strong>{{ peakTrend.label }}</strong>
              <em>{{ peakTrend.value }} 次预约</em>
            </div>
            <div class="hero-mini-card lavender">
              <span>热门自习室</span>
              <strong>{{ topRoom.name }}</strong>
              <em>{{ topRoom.value }} 次预约</em>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="overview-grid">
      <article
        v-for="item in overviewCards"
        :key="item.label"
        class="overview-card portal-hover"
        :class="item.className"
      >
        <div class="overview-top">
          <span class="overview-eyebrow">{{ item.eyebrow }}</span>
          <span class="overview-chip">{{ item.chip }}</span>
        </div>
        <div class="overview-value">{{ item.value }}</div>
        <div class="overview-label">{{ item.label }}</div>
        <div class="overview-progress">
          <span :style="{ width: `${item.percent}%` }"></span>
        </div>
        <div class="overview-tip">{{ item.tip }}</div>
      </article>
    </section>

    <section class="dashboard-grid dashboard-grid-main">
      <el-card shadow="hover" class="panel-card portal-hover trend-panel">
        <template #header>
          <div class="panel-header">
            <div>
              <div class="panel-title">近七日预约趋势</div>
              <div class="panel-subtitle">把高峰波动和日常节奏拉平展示，方便快速判断最近运营状态。</div>
            </div>
            <div class="panel-chip">峰值 {{ peakTrend.value }}</div>
          </div>
        </template>
        <div ref="trendChartRef" class="chart-box"></div>
      </el-card>

      <el-card shadow="hover" class="panel-card portal-hover insights-panel">
        <template #header>
          <div class="panel-header">
            <div>
              <div class="panel-title">运营观察</div>
              <div class="panel-subtitle">把数字转换成可读结论，让首页更有管理价值。</div>
            </div>
          </div>
        </template>

        <div class="insight-list">
          <div class="insight-item">
            <span>峰值预约日</span>
            <strong>{{ peakTrend.label }}</strong>
            <em>{{ peakTrend.value }} 次预约，适合重点关注高峰资源分配。</em>
          </div>
          <div class="insight-item">
            <span>平均预约水平</span>
            <strong>{{ averageReservations }} 次 / 天</strong>
            <em>用于判断近期学习空间的整体活跃度。</em>
          </div>
          <div class="insight-item">
            <span>完成率</span>
            <strong>{{ completionRate }}%</strong>
            <em>今日完成与今日预约的比值，可用于衡量履约表现。</em>
          </div>
        </div>

        <div class="ops-metrics">
          <div class="ops-line">
            <div class="ops-line-top">
              <span>座位利用率</span>
              <strong>{{ usagePercent }}%</strong>
            </div>
            <div class="ops-line-track"><span :style="{ width: `${usagePercent}%` }"></span></div>
          </div>
          <div class="ops-line">
            <div class="ops-line-top">
              <span>空闲余量</span>
              <strong>{{ freeSeatPercent }}%</strong>
            </div>
            <div class="ops-line-track soft"><span :style="{ width: `${freeSeatPercent}%` }"></span></div>
          </div>
        </div>

        <div class="strategy-banner">
          <div class="strategy-label">今日建议</div>
          <div class="strategy-text">{{ strategyText }}</div>
        </div>
      </el-card>
    </section>

    <section class="dashboard-grid dashboard-grid-bottom">
      <el-card shadow="hover" class="panel-card portal-hover">
        <template #header>
          <div class="panel-header">
            <div>
              <div class="panel-title">座位结构</div>
              <div class="panel-subtitle">已占用与空闲比例，适合快速查看当前承载情况。</div>
            </div>
            <div class="panel-chip green-chip">空闲 {{ stats.free_seats }}</div>
          </div>
        </template>
        <div ref="pieChartRef" class="chart-box compact-chart"></div>
      </el-card>

      <el-card shadow="hover" class="panel-card portal-hover">
        <template #header>
          <div class="panel-header">
            <div>
              <div class="panel-title">自习室热度排行</div>
              <div class="panel-subtitle">横向对比各空间热度，便于调整座位配置与引导策略。</div>
            </div>
          </div>
        </template>
        <div ref="barChartRef" class="chart-box compact-chart"></div>
      </el-card>

      <el-card shadow="hover" class="panel-card portal-hover digest-card">
        <template #header>
          <div class="panel-header">
            <div>
              <div class="panel-title">首页摘要</div>
              <div class="panel-subtitle">用更精致、更紧凑的方式展示关键系统信息。</div>
            </div>
          </div>
        </template>

        <div class="digest-grid">
          <div class="digest-item">
            <span>总座位数</span>
            <strong>{{ stats.total_seats }}</strong>
          </div>
          <div class="digest-item">
            <span>总自习室数</span>
            <strong>{{ stats.total_rooms }}</strong>
          </div>
          <div class="digest-item">
            <span>当前使用中</span>
            <strong>{{ stats.active_now }}</strong>
          </div>
          <div class="digest-item">
            <span>今日预约数</span>
            <strong>{{ stats.today_reservations }}</strong>
          </div>
        </div>

        <div class="digest-note">
          这个首页现在更偏现代运营后台风格，减少了大面积生硬横幅，强化了首屏美观度、信息层级和管理感。
        </div>
      </el-card>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'
import request from '../../utils/request'
import { ElMessage } from 'element-plus'

interface RoomDistributionItem {
  name: string
  value: number
}

interface StatsData {
  today_reservations: number
  active_now: number
  completed_today: number
  free_seats: number
  total_rooms: number
  total_seats: number
  seat_usage_rate: number
  trend_labels: string[]
  trend_data: number[]
  room_distribution: RoomDistributionItem[]
}

const router = useRouter()
const trendChartRef = ref<HTMLDivElement | null>(null)
const pieChartRef = ref<HTMLDivElement | null>(null)
const barChartRef = ref<HTMLDivElement | null>(null)

const stats = ref<StatsData>({
  today_reservations: 0,
  active_now: 0,
  completed_today: 0,
  free_seats: 0,
  total_rooms: 0,
  total_seats: 0,
  seat_usage_rate: 0,
  trend_labels: [],
  trend_data: [],
  room_distribution: []
})

const clampPercent = (value: number) => Math.max(0, Math.min(100, Math.round(value || 0)))

const usagePercent = computed(() => clampPercent(stats.value.seat_usage_rate))
const occupiedSeats = computed(() => Math.max(stats.value.total_seats - stats.value.free_seats, 0))
const freeSeatPercent = computed(() => {
  if (!stats.value.total_seats) return 0
  return clampPercent((stats.value.free_seats / stats.value.total_seats) * 100)
})
const completionRate = computed(() => {
  if (!stats.value.today_reservations) return 0
  return clampPercent((stats.value.completed_today / stats.value.today_reservations) * 100)
})
const averageReservations = computed(() => {
  if (!stats.value.trend_data.length) return 0
  const total = stats.value.trend_data.reduce((sum, item) => sum + Number(item || 0), 0)
  return Math.round(total / stats.value.trend_data.length)
})
const peakTrend = computed(() => {
  if (!stats.value.trend_data.length) {
    return { label: '暂无数据', value: 0 }
  }
  const maxValue = Math.max(...stats.value.trend_data)
  const index = stats.value.trend_data.findIndex((item) => item === maxValue)
  return {
    label: stats.value.trend_labels[index] || '未知日期',
    value: maxValue
  }
})
const topRoom = computed(() => {
  if (!stats.value.room_distribution.length) {
    return { name: '暂无数据', value: 0 }
  }
  return [...stats.value.room_distribution].sort((a, b) => b.value - a.value)[0]
})
const heroInsight = computed(() => {
  if (usagePercent.value >= 85) return '当前利用率偏高，建议重点关注高峰分流'
  if (usagePercent.value >= 60) return '整体运行平稳，当前处于较健康的利用区间'
  return '当前负载较轻，可引导更多用户进行预约'
})
const strategyText = computed(() => {
  if (topRoom.value.value === 0) return '当前还没有足够的运营数据，建议先积累预约记录后再做资源调度。'
  if (usagePercent.value >= 85) return `热门空间集中在 ${topRoom.value.name}，建议优先检查高峰时段的座位周转与分流。`
  if (freeSeatPercent.value >= 45) return `当前空闲余量较充足，可结合 ${topRoom.value.name} 的热度做更精准的资源引导。`
  return `整体资源分配较均衡，建议持续关注 ${peakTrend.value.label} 的预约峰值表现。`
})
const overviewCards = computed(() => [
  {
    eyebrow: '今日活跃',
    chip: `${peakTrend.value.label}`,
    label: '今日预约数',
    value: stats.value.today_reservations,
    percent: clampPercent((stats.value.today_reservations / Math.max(peakTrend.value.value || 1, 1)) * 100),
    tip: '反映今天整体预约热度与活跃程度',
    className: 'overview-blue'
  },
  {
    eyebrow: '馆内状态',
    chip: `${usagePercent.value}%`,
    label: '当前使用中',
    value: stats.value.active_now,
    percent: clampPercent((stats.value.active_now / Math.max(stats.value.total_seats || 1, 1)) * 100),
    tip: '正在使用中的座位规模',
    className: 'overview-green'
  },
  {
    eyebrow: '资源余量',
    chip: `${freeSeatPercent.value}%`,
    label: '空闲座位',
    value: stats.value.free_seats,
    percent: freeSeatPercent.value,
    tip: '仍可分配给新预约用户的座位数量',
    className: 'overview-orange'
  },
  {
    eyebrow: '空间配置',
    chip: `${topRoom.value.name}`,
    label: '自习室数量',
    value: stats.value.total_rooms,
    percent: clampPercent((stats.value.total_rooms / Math.max(stats.value.total_rooms || 1, 1)) * 100),
    tip: '后台已纳入管理的学习空间数量',
    className: 'overview-purple'
  }
])

let trendChart: echarts.ECharts | null = null
let pieChart: echarts.ECharts | null = null
let barChart: echarts.ECharts | null = null

const go = (path: string) => router.push(path)

const fetchStats = async () => {
  try {
    stats.value = await request.get('/api/seats/stats') as StatsData
    await nextTick()
    initCharts()
  } catch (error) {
    ElMessage.error('获取统计数据失败')
  }
}

const initTrendChart = () => {
  if (!trendChartRef.value) return
  trendChart?.dispose()
  trendChart = echarts.init(trendChartRef.value)
  trendChart.setOption({
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(15,23,42,0.92)',
      borderWidth: 0,
      textStyle: { color: '#fff' }
    },
    grid: { left: 28, right: 20, top: 28, bottom: 24, containLabel: true },
    xAxis: {
      type: 'category',
      data: stats.value.trend_labels,
      boundaryGap: false,
      axisLine: { lineStyle: { color: '#dbe3f0' } },
      axisTick: { show: false },
      axisLabel: { color: '#64748b' }
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#64748b' },
      splitLine: { lineStyle: { type: 'dashed', color: '#e5edf7' } }
    },
    series: [{
      data: stats.value.trend_data,
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 8,
      lineStyle: {
        width: 4,
        color: '#2563eb',
        shadowBlur: 10,
        shadowColor: 'rgba(37,99,235,0.22)'
      },
      itemStyle: {
        color: '#ffffff',
        borderColor: '#2563eb',
        borderWidth: 3
      },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(37,99,235,0.28)' },
          { offset: 1, color: 'rgba(37,99,235,0.02)' }
        ])
      }
    }]
  })
}

const initPieChart = () => {
  if (!pieChartRef.value) return
  pieChart?.dispose()
  pieChart = echarts.init(pieChartRef.value)
  pieChart.setOption({
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(15,23,42,0.92)',
      borderWidth: 0,
      textStyle: { color: '#fff' }
    },
    legend: {
      bottom: 0,
      left: 'center',
      itemWidth: 10,
      itemHeight: 10,
      textStyle: { color: '#64748b' }
    },
    graphic: [
      {
        type: 'text',
        left: 'center',
        top: '39%',
        style: {
          text: `${usagePercent.value}%`,
          textAlign: 'center',
          fill: '#0f172a',
          fontSize: 26,
          fontWeight: 700
        }
      },
      {
        type: 'text',
        left: 'center',
        top: '50%',
        style: {
          text: '座位利用率',
          textAlign: 'center',
          fill: '#64748b',
          fontSize: 12
        }
      }
    ],
    series: [{
      type: 'pie',
      radius: ['62%', '78%'],
      center: ['50%', '44%'],
      label: { show: false },
      data: [
        { value: occupiedSeats.value, name: '已占用' },
        { value: stats.value.free_seats, name: '空闲' }
      ],
      itemStyle: {
        borderRadius: 12,
        borderColor: '#fff',
        borderWidth: 4
      }
    }],
    color: ['#22c55e', '#dbeafe']
  })
}

const initBarChart = () => {
  if (!barChartRef.value) return
  barChart?.dispose()
  barChart = echarts.init(barChartRef.value)
  barChart.setOption({
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(15,23,42,0.92)',
      borderWidth: 0,
      textStyle: { color: '#fff' }
    },
    grid: { left: 12, right: 20, top: 14, bottom: 14, containLabel: true },
    xAxis: {
      type: 'value',
      axisLabel: { color: '#64748b' },
      splitLine: { lineStyle: { type: 'dashed', color: '#edf2f7' } }
    },
    yAxis: {
      type: 'category',
      data: stats.value.room_distribution.map((item) => item.name),
      axisTick: { show: false },
      axisLine: { show: false },
      axisLabel: { color: '#475569' }
    },
    series: [{
      data: stats.value.room_distribution.map((item) => item.value),
      type: 'bar',
      barWidth: 16,
      itemStyle: {
        borderRadius: [0, 10, 10, 0],
        color: new echarts.graphic.LinearGradient(1, 0, 0, 0, [
          { offset: 0, color: '#c4b5fd' },
          { offset: 1, color: '#7c3aed' }
        ])
      }
    }]
  })
}

const initCharts = () => {
  initTrendChart()
  initPieChart()
  initBarChart()
}

const resizeCharts = () => {
  trendChart?.resize()
  pieChart?.resize()
  barChart?.resize()
}

onMounted(() => {
  fetchStats()
  window.addEventListener('resize', resizeCharts)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', resizeCharts)
  trendChart?.dispose()
  pieChart?.dispose()
  barChart?.dispose()
})
</script>

<style scoped>
.dashboard-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.dashboard-hero {
  position: relative;
  overflow: hidden;
  padding: 28px;
  border-radius: 32px;
  background: linear-gradient(135deg, #f8fbff 0%, #f5f8ff 38%, #f6f3ff 100%);
  border: 1px solid rgba(148, 163, 184, 0.12);
  box-shadow: 0 26px 70px rgba(15, 23, 42, 0.08);
}

.hero-orb {
  position: absolute;
  border-radius: 999px;
  pointer-events: none;
  filter: blur(8px);
}

.hero-orb-a {
  width: 220px;
  height: 220px;
  right: -36px;
  top: -58px;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.22), rgba(59, 130, 246, 0));
}

.hero-orb-b {
  width: 240px;
  height: 240px;
  left: 36%;
  bottom: -130px;
  background: radial-gradient(circle, rgba(139, 92, 246, 0.16), rgba(139, 92, 246, 0));
}

.hero-main {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 24px;
  align-items: stretch;
}

.hero-badge {
  display: inline-flex;
  padding: 7px 12px;
  border-radius: 999px;
  background: rgba(37, 99, 235, 0.08);
  color: #1d4ed8;
  font-size: 12px;
  font-weight: 700;
}

.hero-title {
  margin: 18px 0 12px;
  font-size: 36px;
  line-height: 1.15;
  letter-spacing: -0.03em;
  color: #0f172a;
}

.hero-desc {
  margin: 0;
  max-width: 740px;
  color: #475569;
  font-size: 15px;
  line-height: 1.9;
}

.hero-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 22px;
}

.hero-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 9px 14px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.74);
  border: 1px solid rgba(148, 163, 184, 0.16);
  color: #334155;
  font-size: 13px;
}

.live-pill {
  background: rgba(16, 185, 129, 0.10);
  color: #047857;
  border-color: rgba(16, 185, 129, 0.14);
}

.hero-pill-dot {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: #10b981;
  box-shadow: 0 0 0 6px rgba(16, 185, 129, 0.12);
}

.hero-action-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 24px;
}

.hero-primary-btn,
.hero-secondary-btn {
  height: 46px;
  padding: 0 20px;
  border-radius: 999px;
}

.hero-side {
  display: grid;
  gap: 14px;
}

.focus-card {
  padding: 20px;
  border-radius: 26px;
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(12px);
  box-shadow: 0 20px 40px rgba(37, 99, 235, 0.08);
}

.focus-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.focus-label {
  font-size: 12px;
  color: #64748b;
}

.focus-value {
  margin-top: 8px;
  font-size: 38px;
  line-height: 1;
  font-weight: 900;
  color: #0f172a;
}

.focus-badge {
  padding: 8px 12px;
  border-radius: 999px;
  background: linear-gradient(135deg, #eff6ff, #eef2ff);
  color: #4338ca;
  font-size: 12px;
  font-weight: 700;
}

.focus-progress {
  margin-top: 18px;
  height: 10px;
  overflow: hidden;
  border-radius: 999px;
  background: #e2e8f0;
}

.focus-progress span {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, #2563eb, #8b5cf6);
}

.focus-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-top: 18px;
}

.focus-metric {
  padding: 14px 16px;
  border-radius: 18px;
  background: linear-gradient(180deg, #fbfdff, #f4f8ff);
}

.focus-metric span {
  display: block;
  color: #64748b;
  font-size: 12px;
}

.focus-metric strong {
  display: block;
  margin-top: 8px;
  color: #0f172a;
  font-size: 18px;
}

.hero-mini-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.hero-mini-card {
  padding: 18px;
  border-radius: 22px;
  background: linear-gradient(135deg, #ffffff, #f8fbff);
  border: 1px solid rgba(148, 163, 184, 0.12);
  box-shadow: 0 16px 28px rgba(15, 23, 42, 0.05);
}

.hero-mini-card.lavender {
  background: linear-gradient(135deg, #faf7ff, #f4f1ff);
}

.hero-mini-card span,
.hero-mini-card em {
  display: block;
}

.hero-mini-card span {
  color: #64748b;
  font-size: 12px;
}

.hero-mini-card strong {
  display: block;
  margin-top: 10px;
  color: #0f172a;
  font-size: 20px;
  line-height: 1.3;
}

.hero-mini-card em {
  margin-top: 8px;
  color: #64748b;
  font-style: normal;
  font-size: 12px;
}

.overview-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}

.overview-card {
  padding: 20px;
  border-radius: 24px;
  color: #fff;
  box-shadow: 0 18px 36px rgba(15, 23, 42, 0.08);
}

.overview-blue {
  background: linear-gradient(135deg, #2563eb, #60a5fa);
}

.overview-green {
  background: linear-gradient(135deg, #059669, #34d399);
}

.overview-orange {
  background: linear-gradient(135deg, #ea580c, #fb923c);
}

.overview-purple {
  background: linear-gradient(135deg, #7c3aed, #a78bfa);
}

.overview-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.overview-eyebrow,
.overview-chip,
.overview-tip {
  opacity: 0.9;
}

.overview-eyebrow,
.overview-chip {
  font-size: 12px;
}

.overview-chip {
  padding: 4px 8px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.16);
}

.overview-value {
  margin-top: 18px;
  font-size: 34px;
  font-weight: 900;
  line-height: 1;
}

.overview-label {
  margin-top: 8px;
  font-size: 16px;
  font-weight: 700;
}

.overview-progress {
  margin-top: 16px;
  height: 8px;
  overflow: hidden;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.18);
}

.overview-progress span {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: rgba(255, 255, 255, 0.95);
}

.overview-tip {
  margin-top: 12px;
  font-size: 12px;
}

.dashboard-grid {
  display: grid;
  gap: 18px;
}

.dashboard-grid-main {
  grid-template-columns: 1.35fr 0.85fr;
}

.dashboard-grid-bottom {
  grid-template-columns: 0.92fr 1.08fr 0.86fr;
}

.panel-card {
  border: none;
  border-radius: 28px;
  box-shadow: 0 20px 48px rgba(15, 23, 42, 0.06);
}

.trend-panel :deep(.el-card__body),
.insights-panel :deep(.el-card__body),
.digest-card :deep(.el-card__body) {
  padding-top: 8px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}

.panel-title {
  font-size: 18px;
  font-weight: 800;
  color: #0f172a;
}

.panel-subtitle {
  margin-top: 4px;
  color: #64748b;
  font-size: 12px;
  line-height: 1.7;
}

.panel-chip {
  padding: 8px 12px;
  border-radius: 999px;
  background: #eff6ff;
  color: #1d4ed8;
  font-size: 12px;
  font-weight: 700;
}

.green-chip {
  background: rgba(16, 185, 129, 0.10);
  color: #047857;
}

.chart-box {
  width: 100%;
  height: 360px;
}

.compact-chart {
  height: 320px;
}

.insight-list {
  display: grid;
  gap: 12px;
}

.insight-item {
  padding: 16px 18px;
  border-radius: 20px;
  background: linear-gradient(180deg, #f8fbff, #f3f7ff);
}

.insight-item span,
.insight-item em {
  display: block;
}

.insight-item span {
  color: #64748b;
  font-size: 12px;
}

.insight-item strong {
  display: block;
  margin-top: 8px;
  color: #0f172a;
  font-size: 18px;
}

.insight-item em {
  margin-top: 8px;
  color: #64748b;
  font-style: normal;
  line-height: 1.7;
  font-size: 12px;
}

.ops-metrics {
  display: grid;
  gap: 14px;
  margin-top: 18px;
}

.ops-line-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  color: #475569;
  font-size: 13px;
}

.ops-line-top strong {
  color: #0f172a;
  font-size: 14px;
}

.ops-line-track {
  height: 10px;
  overflow: hidden;
  border-radius: 999px;
  background: #e2e8f0;
}

.ops-line-track span {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, #2563eb, #8b5cf6);
}

.ops-line-track.soft span {
  background: linear-gradient(90deg, #22c55e, #86efac);
}

.strategy-banner {
  margin-top: 18px;
  padding: 18px;
  border-radius: 22px;
  background: linear-gradient(135deg, #eff6ff, #f5f3ff);
}

.strategy-label {
  color: #4338ca;
  font-size: 12px;
  font-weight: 700;
}

.strategy-text {
  margin-top: 10px;
  color: #334155;
  line-height: 1.8;
}

.digest-card {
  background: linear-gradient(180deg, #ffffff, #f8fbff);
}

.digest-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.digest-item {
  padding: 16px;
  border-radius: 18px;
  background: #ffffff;
  border: 1px solid rgba(148, 163, 184, 0.12);
}

.digest-item span {
  display: block;
  color: #64748b;
  font-size: 12px;
}

.digest-item strong {
  display: block;
  margin-top: 8px;
  color: #0f172a;
  font-size: 24px;
  font-weight: 800;
}

.digest-note {
  margin-top: 16px;
  padding: 16px 18px;
  border-radius: 20px;
  background: linear-gradient(135deg, #0f172a, #1e293b);
  color: rgba(255, 255, 255, 0.86);
  line-height: 1.8;
  font-size: 13px;
}

@media (max-width: 1280px) {
  .hero-main,
  .dashboard-grid-main,
  .dashboard-grid-bottom,
  .overview-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 960px) {
  .hero-main,
  .dashboard-grid-main,
  .dashboard-grid-bottom,
  .overview-grid,
  .hero-mini-grid {
    grid-template-columns: 1fr;
  }

  .hero-title {
    font-size: 30px;
  }
}

@media (max-width: 640px) {
  .dashboard-hero {
    padding: 18px;
  }

  .focus-grid,
  .digest-grid {
    grid-template-columns: 1fr;
  }

  .hero-action-row {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
