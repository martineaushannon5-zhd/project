<template>
  <div class="dashboard-page">
    <div class="hero-card mb-6">
      <div>
        <div class="hero-badge">自习室后台数据看板</div>
        <h2 class="hero-title">预约趋势、座位占用、资源概览</h2>
        <p class="hero-desc">用于展示自习室预约系统的核心运营数据，帮助管理员快速掌握系统运行状态。</p>
      </div>
      <div class="hero-stats">
        <div class="hero-stat">
          <span>今日预约</span>
          <strong>{{ stats.today_reservations }}</strong>
        </div>
        <div class="hero-stat">
          <span>当前使用中</span>
          <strong>{{ stats.active_now }}</strong>
        </div>
        <div class="hero-stat">
          <span>占用率</span>
          <strong>{{ stats.seat_usage_rate }}%</strong>
        </div>
      </div>
    </div>

    <el-row :gutter="20" class="mb-6">
      <el-col :xs="12" :sm="12" :md="6">
        <el-card shadow="hover" class="stat-card stat-blue">
          <div class="stat-label">今日预约数</div>
          <div class="stat-value">{{ stats.today_reservations }}</div>
          <div class="stat-tip">反映当天的预约热度</div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="12" :md="6">
        <el-card shadow="hover" class="stat-card stat-green">
          <div class="stat-label">当前使用中</div>
          <div class="stat-value">{{ stats.active_now }}</div>
          <div class="stat-tip">当前正在使用的座位数</div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="12" :md="6">
        <el-card shadow="hover" class="stat-card stat-orange">
          <div class="stat-label">空闲座位</div>
          <div class="stat-value">{{ stats.free_seats }}</div>
          <div class="stat-tip">剩余可预约的座位数量</div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="12" :md="6">
        <el-card shadow="hover" class="stat-card stat-purple">
          <div class="stat-label">自习室数量</div>
          <div class="stat-value">{{ stats.total_rooms }}</div>
          <div class="stat-tip">系统中已配置的自习室</div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :xs="24" :lg="16" class="mb-6">
        <el-card shadow="hover" class="panel-card">
          <template #header>
            <div class="panel-title">近七日预约趋势</div>
          </template>
          <div ref="trendChartRef" class="chart-box"></div>
        </el-card>
      </el-col>
      <el-col :xs="24" :lg="8" class="mb-6">
        <el-card shadow="hover" class="panel-card h-full">
          <template #header>
            <div class="panel-title">座位占用率</div>
          </template>
          <div ref="pieChartRef" class="chart-box compact-chart"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :xs="24" :lg="12" class="mb-6">
        <el-card shadow="hover" class="panel-card h-full">
          <template #header>
            <div class="panel-title">自习室预约分布</div>
          </template>
          <div ref="barChartRef" class="chart-box compact-chart"></div>
        </el-card>
      </el-col>
      <el-col :xs="24" :lg="12" class="mb-6">
        <el-card shadow="hover" class="panel-card h-full info-card">
          <template #header>
            <div class="panel-title">系统说明</div>
          </template>
          <el-alert title="当前看板为毕设展示核心页面" type="info" show-icon :closable="false" class="mb-4" />
          <div class="info-grid">
            <div>
              <span>总座位数</span>
              <strong>{{ stats.total_seats }}</strong>
            </div>
            <div>
              <span>今日完成预约</span>
              <strong>{{ stats.completed_today }}</strong>
            </div>
            <div>
              <span>座位占用率</span>
              <strong>{{ stats.seat_usage_rate }}%</strong>
            </div>
            <div>
              <span>数据来源</span>
              <strong>后端实时统计</strong>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import * as echarts from 'echarts'
import request from '../../utils/request'
import { ElMessage } from 'element-plus'

const trendChartRef = ref<HTMLDivElement | null>(null)
const pieChartRef = ref<HTMLDivElement | null>(null)
const barChartRef = ref<HTMLDivElement | null>(null)

const stats = ref({
  today_reservations: 0,
  active_now: 0,
  completed_today: 0,
  free_seats: 0,
  total_rooms: 0,
  total_seats: 0,
  seat_usage_rate: 0,
  trend_labels: [],
  trend_data: [],
  room_distribution: [] as { name: string; value: number }[]
})

let trendChart: echarts.ECharts | null = null
let pieChart: echarts.ECharts | null = null
let barChart: echarts.ECharts | null = null

const fetchStats = async () => {
  try {
    const res: any = await request.get('/api/seats/stats')
    stats.value = res
    await nextTick()
    initCharts()
  } catch (error) {
    ElMessage.error('获取统计数据失败')
  }
}

/** 初始化趋势图 */
const initTrendChart = () => {
  if (!trendChartRef.value) return
  trendChart?.dispose()
  trendChart = echarts.init(trendChartRef.value)
  trendChart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: 40, right: 20, top: 30, bottom: 30 },
    xAxis: {
      type: 'category',
      data: stats.value.trend_labels,
      axisLine: { lineStyle: { color: '#dbe3f0' } },
      axisLabel: { color: '#6b7280' }
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#6b7280' },
      splitLine: { lineStyle: { type: 'dashed', color: '#edf2f7' } }
    },
    series: [
      {
        data: stats.value.trend_data,
        type: 'line',
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        lineStyle: { width: 4, color: '#3b82f6' },
        itemStyle: { color: '#3b82f6' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(59,130,246,0.35)' },
            { offset: 1, color: 'rgba(59,130,246,0.02)' }
          ])
        }
      }
    ]
  })
}

/** 初始化占用率图 */
const initPieChart = () => {
  if (!pieChartRef.value) return
  pieChart?.dispose()
  pieChart = echarts.init(pieChartRef.value)
  pieChart.setOption({
    tooltip: { trigger: 'item' },
    legend: { bottom: 0, left: 'center' },
    series: [
      {
        type: 'pie',
        radius: ['55%', '78%'],
        center: ['50%', '45%'],
        data: [
          { value: stats.value.total_seats - stats.value.free_seats, name: '已占用' },
          { value: stats.value.free_seats, name: '空闲' }
        ],
        label: { formatter: '{b}\n{d}%' },
        itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 }
      }
    ],
    color: ['#22c55e', '#cbd5e1']
  })
}

/** 初始化自习室分布图 */
const initBarChart = () => {
  if (!barChartRef.value) return
  barChart?.dispose()
  barChart = echarts.init(barChartRef.value)
  barChart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: 50, right: 20, top: 20, bottom: 30 },
    xAxis: {
      type: 'category',
      data: stats.value.room_distribution.map((item) => item.name),
      axisLabel: { color: '#6b7280', rotate: 15 }
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#6b7280' },
      splitLine: { lineStyle: { type: 'dashed', color: '#edf2f7' } }
    },
    series: [
      {
        data: stats.value.room_distribution.map((item) => item.value),
        type: 'bar',
        barWidth: '42%',
        itemStyle: {
          borderRadius: [10, 10, 0, 0],
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#8b5cf6' },
            { offset: 1, color: '#c4b5fd' }
          ])
        }
      }
    ]
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
  padding: 4px;
}

.hero-card {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  padding: 24px;
  border-radius: 18px;
  color: #fff;
  background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
  box-shadow: 0 18px 40px rgba(37, 99, 235, 0.18);
}

.hero-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.16);
  margin-bottom: 14px;
  font-size: 12px;
}

.hero-title {
  font-size: 28px;
  font-weight: 800;
  margin: 0 0 10px;
}

.hero-desc {
  margin: 0;
  max-width: 640px;
  opacity: 0.92;
}

.hero-stats {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
  min-width: 420px;
}

.hero-stat {
  padding: 16px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.14);
  backdrop-filter: blur(8px);
}

.hero-stat span,
.stat-label,
.stat-tip,
.info-grid span {
  display: block;
  font-size: 12px;
  opacity: 0.85;
}

.hero-stat strong,
.stat-value,
.info-grid strong {
  display: block;
  margin-top: 6px;
  font-size: 22px;
  font-weight: 800;
}

.stat-card {
  border: none;
  border-radius: 18px;
  color: #fff;
  min-height: 128px;
}

.stat-blue { background: linear-gradient(135deg, #3b82f6, #60a5fa); }
.stat-green { background: linear-gradient(135deg, #10b981, #34d399); }
.stat-orange { background: linear-gradient(135deg, #f59e0b, #fbbf24); }
.stat-purple { background: linear-gradient(135deg, #8b5cf6, #a78bfa); }

.panel-card {
  border: none;
  border-radius: 18px;
}

.panel-title {
  font-weight: 700;
  color: #1f2937;
}

.chart-box {
  width: 100%;
  height: 360px;
}

.compact-chart {
  height: 320px;
}

.info-card {
  background: linear-gradient(180deg, #ffffff, #f8fbff);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

@media (max-width: 992px) {
  .hero-card {
    flex-direction: column;
  }

  .hero-stats {
    min-width: 100%;
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .hero-stats,
  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>
