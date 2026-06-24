<template>
  <div>
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="mb-6">
      <el-col :span="8">
        <el-card shadow="hover" class="rounded-xl border-none">
          <div class="flex items-center justify-between">
            <div>
              <div class="text-gray-400 text-sm mb-1">今日总预约数</div>
              <div class="text-3xl font-bold text-gray-800">{{ stats.today_reservations }}</div>
            </div>
            <el-icon class="text-4xl text-blue-400"><DocumentChecked /></el-icon>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="rounded-xl border-none">
          <div class="flex items-center justify-between">
            <div>
              <div class="text-gray-400 text-sm mb-1">当前使用中</div>
              <div class="text-3xl font-bold text-green-500">{{ stats.active_now }}</div>
            </div>
            <el-icon class="text-4xl text-green-400"><Position /></el-icon>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="rounded-xl border-none">
          <div class="flex items-center justify-between">
            <div>
              <div class="text-gray-400 text-sm mb-1">空闲座位</div>
              <div class="text-3xl font-bold text-orange-500">{{ stats.free_seats }}</div>
            </div>
            <el-icon class="text-4xl text-orange-400"><CoffeeCup /></el-icon>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Echarts 图表区 -->
    <el-card shadow="hover" class="rounded-xl border-none">
      <template #header>
        <div class="font-bold text-gray-700">近七日预约趋势</div>
      </template>
      <div ref="chartRef" class="w-full h-80"></div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import { DocumentChecked, Position, CoffeeCup } from '@element-plus/icons-vue'
import request from '../../utils/request'
import { ElMessage } from 'element-plus'

const chartRef = ref(null)
const stats = ref({
  today_reservations: 0,
  active_now: 0,
  free_seats: 0,
  trend_data: [0, 0, 0, 0, 0, 0, 0]
})

const fetchStats = async () => {
  try {
    const res: any = await request.get('/api/seats/stats')
    if (res) {
      stats.value = res
      initChart()
    }
  } catch (error) {
    ElMessage.error('获取统计数据失败')
  }
}

// 初始化 ECharts
const initChart = () => {
  if (chartRef.value) {
    const myChart = echarts.init(chartRef.value)
    const option = {
      tooltip: {
        trigger: 'axis'
      },
      xAxis: {
        type: 'category',
        data: ['6天前', '5天前', '4天前', '3天前', '前天', '昨天', '今天'],
        axisLine: { lineStyle: { color: '#999' } }
      },
      yAxis: {
        type: 'value',
        axisLine: { show: false },
        splitLine: { lineStyle: { type: 'dashed', color: '#eee' } }
      },
      series: [
        {
          data: stats.value.trend_data,
          type: 'line',
          smooth: true,
          areaStyle: {
            opacity: 0.2,
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#409eff' },
              { offset: 1, color: '#ffffff' }
            ])
          },
          itemStyle: { color: '#409eff' },
          lineStyle: { width: 3 }
        }
      ]
    }
    myChart.setOption(option)
    window.addEventListener('resize', () => {
      myChart.resize()
    })
  }
}

onMounted(() => {
  fetchStats()
})
</script>
