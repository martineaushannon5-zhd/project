<template>
  <div class="booking-page portal-shell">
    <el-card shadow="hover" class="portal-card portal-hover mb-6">
      <template #header>
        <div class="section-head">
          <div>
            <div class="portal-section-title">自习室预约</div>
            <div class="portal-section-subtitle">选择自习室后查看座位，轻松完成预约。</div>
          </div>
        </div>
      </template>
      <el-select v-model="selectedRoom" placeholder="请选择自习室" size="large" class="room-select" @change="fetchSeats">
        <el-option v-for="room in rooms" :key="room.id" :label="room.name" :value="room.id" />
      </el-select>
    </el-card>

    <el-card shadow="hover" class="portal-card portal-hover" v-if="selectedRoom">
      <template #header>
        <div class="section-head">
          <div>
            <div class="portal-section-title">座位分布</div>
            <div class="portal-section-subtitle">绿色表示空闲，红色表示使用中。</div>
          </div>
        </div>
      </template>

      <div class="seat-grid">
        <div 
          v-for="seat in seats" 
          :key="seat.id"
          @click="openBookingDialog(seat)"
          class="seat-item portal-hover"
          :class="seat.status === 1 ? 'seat-free' : 'seat-busy'"
        >
          <div class="seat-number">{{ seat.seat_number }}</div>
          <div class="seat-meta">
            <el-icon v-if="seat.has_power"><Lightning /></el-icon>
            <span>{{ seat.has_power ? '有电源' : '无电源' }}</span>
          </div>
        </div>
      </div>
    </el-card>

    <el-dialog v-model="dialogVisible" title="确认预约" width="420px" destroy-on-close>
      <el-form :model="bookingForm" label-width="80px">
        <el-form-item label="座位号">
          <el-input :value="currentSeat?.seat_number" disabled />
        </el-form-item>
        <el-form-item label="预约日期">
          <el-date-picker v-model="bookingForm.date" type="date" placeholder="选择日期" class="w-full" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="时间段">
          <el-time-picker v-model="bookingForm.timeRange" is-range range-separator="至" start-placeholder="开始时间" end-placeholder="结束时间" format="HH:mm:ss" value-format="HH:mm:ss" class="w-full" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitBooking" :loading="loading">确认预约</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import request from '../../utils/request'
import { Lightning } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const rooms = ref<any[]>([])
const selectedRoom = ref<number | null>(null)
const seats = ref<any[]>([])
const user = ref(JSON.parse(localStorage.getItem('user') || '{}'))

const dialogVisible = ref(false)
const currentSeat = ref<any>(null)
const loading = ref(false)

const bookingForm = reactive({
  date: '',
  timeRange: [] as string[]
})

const fetchRooms = async () => {
  try {
    rooms.value = await request.get('/api/seats/rooms')
  } catch (error) {
    ElMessage.error('获取自习室失败')
  }
}

const fetchSeats = async () => {
  if (!selectedRoom.value) return
  try {
    seats.value = await request.get(`/api/seats/rooms/${selectedRoom.value}/seats`)
  } catch (error) {
    ElMessage.error('获取座位失败')
  }
}

const openBookingDialog = (seat: any) => {
  if (seat.status !== 1) {
    ElMessage.warning('该座位当前不可预约')
    return
  }
  currentSeat.value = seat
  dialogVisible.value = true
  const today = new Date().toISOString().split('T')[0]
  bookingForm.date = today
  bookingForm.timeRange = ['08:00:00', '12:00:00']
}

const submitBooking = async () => {
  if (!bookingForm.date || !bookingForm.timeRange || bookingForm.timeRange.length !== 2) {
    ElMessage.warning('请完整填写预约时间')
    return
  }
  
  loading.value = true
  try {
    const payload = {
      user_id: user.value.id,
      seat_id: currentSeat.value.id,
      date: bookingForm.date,
      start_time: bookingForm.timeRange[0],
      end_time: bookingForm.timeRange[1]
    }
    await request.post('/api/seats/reservations', payload)
    ElMessage.success('预约成功！')
    dialogVisible.value = false
    fetchSeats()
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '预约失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchRooms()
})
</script>

<style scoped>
.section-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.room-select {
  width: 320px;
}

.seat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 14px;
}

.seat-item {
  padding: 18px 14px;
  border-radius: 18px;
  border: 1px solid transparent;
  cursor: pointer;
  text-align: center;
  background: #f8fbff;
}

.seat-free {
  border-color: rgba(34,197,94,0.25);
}

.seat-busy {
  opacity: 0.65;
  border-color: rgba(239,68,68,0.18);
}

.seat-number {
  font-size: 18px;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 8px;
}

.seat-meta {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #64748b;
  font-size: 12px;
}
</style>
