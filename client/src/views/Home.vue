<template>
  <el-container class="min-h-screen">
    <!-- 侧边栏 -->
    <el-aside width="250px" class="bg-gray-800 text-white shadow-xl transition-all duration-300">
      <div class="h-16 flex items-center justify-center text-xl font-bold border-b border-gray-700 tracking-wider">
        自习室管理系统
      </div>
      <el-menu
        active-text-color="#409eff"
        background-color="transparent"
        class="border-none"
        default-active="1"
        text-color="#fff"
      >
        <el-menu-item index="1">
          <el-icon><DataLine /></el-icon>
          <span>数据看板</span>
        </el-menu-item>
        <el-menu-item index="2">
          <el-icon><Coordinate /></el-icon>
          <span>座位预约</span>
        </el-menu-item>
        <el-menu-item index="3">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主内容区 -->
    <el-container>
      <el-header class="bg-white shadow-sm flex items-center justify-between px-6 z-10">
        <div class="text-gray-600 font-medium">欢迎回来，{{ user?.real_name || user?.username || '管理员' }}</div>
        <el-button type="danger" plain @click="logout" size="small">退出登录</el-button>
      </el-header>

      <el-main class="bg-gray-50 p-6">
        <!-- 统计卡片 -->
        <el-row :gutter="20" class="mb-6">
          <el-col :span="8">
            <el-card shadow="hover" class="rounded-xl border-none">
              <div class="flex items-center justify-between">
                <div>
                  <div class="text-gray-400 text-sm mb-1">今日总预约数</div>
                  <div class="text-3xl font-bold text-gray-800">128</div>
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
                  <div class="text-3xl font-bold text-green-500">45</div>
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
                  <div class="text-3xl font-bold text-orange-500">15</div>
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
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'

const router = useRouter()
const chartRef = ref(null)
const user = ref(JSON.parse(localStorage.getItem('user') || '{}'))

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
        data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
        axisLine: { lineStyle: { color: '#999' } }
      },
      yAxis: {
        type: 'value',
        axisLine: { show: false },
        splitLine: { lineStyle: { type: 'dashed', color: '#eee' } }
      },
      series: [
        {
          data: [82, 93, 90, 104, 129, 133, 142],
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
  initChart()
})

const logout = () => {
  localStorage.removeItem('user')
  router.push('/login')
}
</script>