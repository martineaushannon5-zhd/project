<template>
  <div class="portal-shell">
    <el-card class="portal-card portal-hover">
      <template #header>
        <div class="card-header-row">
          <div>
            <div class="portal-section-title">自习室预约</div>
            <div class="portal-section-subtitle">选择自习室、查看座位、完成预约。</div>
          </div>
          <el-button type="primary" @click="$router.push('/portal/my-reservations')">查看我的预约</el-button>
        </div>
      </template>

      <div class="booking-portal">
        <div class="booking-side">
          <div class="booking-hero">
            <div class="booking-title">选择自习室</div>
            <div class="booking-desc">卡片式浏览更适合学生端，清晰查看每个自习室的座位信息。</div>
          </div>
          <el-select v-model="selectedRoom" placeholder="请选择自习室" size="large" class="w-full mt-4" @change="fetchSeats">
            <el-option v-for="room in rooms" :key="room.id" :label="room.name" :value="room.id" />
          </el-select>

          <div class="room-tags" v-if="rooms.length">
            <span v-for="room in rooms" :key="room.id" class="room-tag" @click="selectedRoom = room.id; fetchSeats()">{{ room.name }}</span>
          </div>
        </div>

        <div class="booking-main">
          <el-empty v-if="!selectedRoom" description="请选择一个自习室开始预约" />
          <div v-else class="seat-board">
            <div v-for="seat in seats" :key="seat.id" class="seat-card portal-hover" :class="seat.status === 1 ? 'free' : 'busy'" @click="openBookingDialog(seat)">
              <div class="seat-number">{{ seat.seat_number }}</div>
              <div class="seat-meta">
                <span>{{ seat.has_power ? '有电源' : '无电源' }}</span>
                <span>{{ seat.status === 1 ? '可预约' : '维护中' }}</span>
              </div>
            </div>
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
import { ElMessage } from 'element-plus'

const rooms = ref<any[]>([])
const selectedRoom = ref<number | null>(null)
const seats = ref<any[]>([])
const user = ref(JSON.parse(localStorage.getItem('user') || '{}'))
const dialogVisible = ref(false)
const currentSeat = ref<any>(null)
const loading = ref(false)

const bookingForm = reactive({ date: '', timeRange: [] as string[] })

const fetchRooms = async () => {
  rooms.value = await request.get('/api/seats/rooms')
}

const fetchSeats = async () => {
  if (!selectedRoom.value) return
  seats.value = await request.get(`/api/seats/rooms/${selectedRoom.value}/seats`)
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
    await request.post('/api/seats/reservations', {
      user_id: user.value.id,
      seat_id: currentSeat.value.id,
      date: bookingForm.date,
      start_time: bookingForm.timeRange[0],
      end_time: bookingForm.timeRange[1]
    })
    ElMessage.success('预约成功！')
    dialogVisible.value = false
    fetchSeats()
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '预约失败')
  } finally {
    loading.value = false
  }
}

onMounted(fetchRooms)
</script>
