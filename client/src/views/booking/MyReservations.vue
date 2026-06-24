<template>
  <div class="portal-shell">
    <el-card shadow="hover" class="portal-card portal-hover reservation-card">
      <template #header>
        <div class="card-header">
          <div class="title-box">
            <div class="portal-section-title">我的预约记录</div>
            <div class="portal-section-subtitle">可在此取消未使用预约，并完成签到操作。</div>
          </div>
          <el-button :icon="Refresh" @click="fetchReservations">刷新</el-button>
        </div>
      </template>

      <el-table :data="reservations" style="width: 100%" v-loading="loading" border>
        <el-table-column prop="id" label="预约ID" width="90" />
        <el-table-column prop="date" label="预约日期" width="120" />
        <el-table-column label="时间段" min-width="180">
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
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button link type="warning" @click="checkin(row)" :disabled="row.status !== 'pending'">签到</el-button>
            <el-button link type="danger" @click="cancel(row)" :disabled="row.status !== 'pending'">取消</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import request from '../../utils/request'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'

const reservations = ref<any[]>([])
const loading = ref(false)
const user = ref(JSON.parse(localStorage.getItem('user') || '{}'))

const fetchReservations = async () => {
  if (!user.value.id) return
  loading.value = true
  try {
    reservations.value = await request.get(`/api/seats/reservations/user/${user.value.id}`)
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

const cancel = async (row: any) => {
  await ElMessageBox.confirm('确认取消该预约吗？', '提示', { type: 'warning' })
  try {
    await request.post(`/api/seats/reservations/${row.id}/cancel`, null, { params: { user_id: user.value.id } })
    ElMessage.success('取消成功')
    fetchReservations()
  } catch (error) {
    ElMessage.error('取消失败')
  }
}

const checkin = async (row: any) => {
  try {
    await request.post(`/api/seats/reservations/${row.id}/checkin`, null, { params: { user_id: user.value.id } })
    ElMessage.success('签到成功')
    fetchReservations()
  } catch (error) {
    ElMessage.error('签到失败')
  }
}

onMounted(fetchReservations)
</script>

<style scoped>
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}
</style>
