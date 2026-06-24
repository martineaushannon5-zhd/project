<template>
  <div class="my-reservations-container">
    <el-card shadow="never" class="rounded-xl border-none">
      <template #header>
        <div class="font-bold text-gray-700">我的预约记录</div>
      </template>
      
      <el-table :data="reservations" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="预约ID" width="80" />
        <el-table-column prop="date" label="预约日期" width="120" />
        <el-table-column label="时间段">
          <template #default="{ row }">
            {{ row.start_time }} - {{ row.end_time }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import request from '../../utils/request'
import { ElMessage } from 'element-plus'

const reservations = ref([])
const loading = ref(false)
const user = ref(JSON.parse(localStorage.getItem('user') || '{}'))

const fetchReservations = async () => {
  if (!user.value.id) return
  loading.value = true
  try {
    const res: any = await request.get(`/api/seats/reservations/user/${user.value.id}`)
    reservations.value = res
  } catch (error) {
    ElMessage.error('获取预约记录失败')
  } finally {
    loading.value = false
  }
}

const getStatusType = (status: string) => {
  const map: Record<string, string> = {
    pending: 'warning',
    active: 'success',
    completed: 'info',
    cancelled: 'danger'
  }
  return map[status] || 'info'
}

const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    pending: '待使用',
    active: '使用中',
    completed: '已完成',
    cancelled: '已取消'
  }
  return map[status] || status
}

onMounted(() => {
  fetchReservations()
})
</script>