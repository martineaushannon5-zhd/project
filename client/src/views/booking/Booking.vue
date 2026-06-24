<template>
  <div class="booking-container">
    <el-card shadow="never" class="rounded-xl border-none mb-6">
      <template #header>
        <div class="font-bold text-gray-700">自习室选择</div>
      </template>
      <el-select v-model="selectedRoom" placeholder="请选择自习室" size="large" class="w-64" @change="fetchSeats">
        <el-option v-for="room in rooms" :key="room.id" :label="room.name" :value="room.id" />
      </el-select>
    </el-card>

    <el-card shadow="never" class="rounded-xl border-none" v-if="selectedRoom">
      <template #header>
        <div class="font-bold text-gray-700">座位分布 (绿色: 空闲, 红色: 使用中)</div>
      </template>
      
      <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        <div 
          v-for="seat in seats" 
          :key="seat.id"
          @click="openBookingDialog(seat)"
          class="p-4 rounded-lg border-2 cursor-pointer transition-all duration-200 text-center hover:shadow-md"
          :class="seat.status === 1 ? 'border-green-400 bg-green-50 hover:bg-green-100 text-green-700' : 'border-red-400 bg-red-50 cursor-not-allowed text-red-700 opacity-60'"
        >
          <div class="font-bold text-lg mb-1">{{ seat.seat_number }}</div>
          <div class="text-xs flex items-center justify-center gap-1">
            <el-icon v-if="seat.has_power"><Lightning /></el-icon>
            <span v-if="seat.has_power">有电源</span>
            <span v-else>无电源</span>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 预约弹窗 -->
    <el-dialog v-model="dialogVisible" title="确认预约" width="400px" destroy-on-close>
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
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitBooking" :loading="loading">确认预约</el-button>
        </span>
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
    const res: any = await request.get('/api/seats/rooms')
    rooms.value = res
  } catch (error) {
    ElMessage.error('获取自习室失败')
  }
}

const fetchSeats = async () => {
  if (!selectedRoom.value) return
  try {
    const res: any = await request.get(`/api/seats/rooms/${selectedRoom.value}/seats`)
    seats.value = res
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
  // 设置默认时间为今天
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
    fetchSeats() // 刷新座位状态
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