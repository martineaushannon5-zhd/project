<template>
  <div class="booking-page" :class="isAdminView ? 'ops-console-mode' : 'portal-mode'">
    <!-- ============================================== -->
    <!-- ADMIN: EXTREME OPS CONSOLE MODE                -->
    <!-- ============================================== -->
    <template v-if="isAdminView">
      <div class="ops-header">
        <div class="ops-header-left">
          <div class="ops-logo">
            <span class="pulse-ring"></span>
            <strong>SPACE_OPS</strong>
            <em>// ORCHESTRATION CONSOLE</em>
          </div>
          <div class="ops-title">
            <h1>实时空间编排引擎</h1>
            <p>监控房间负载、干预异常座位、调度电源资源，全景掌控自习室物理空间。</p>
          </div>
        </div>
        <div class="ops-header-right">
          <div class="ops-metric">
            <span>全局负载率</span>
            <strong :class="{'text-danger': selectedRoomUsage > 80}">{{ selectedRoomUsage }}<small>%</small></strong>
          </div>
          <div class="ops-metric">
            <span>健康节点</span>
            <strong>{{ freeSeatsCount }}<small> / {{ totalSeats }}</small></strong>
          </div>
        </div>
      </div>

      <div class="ops-layout">
        <!-- 左侧面板：房间切换与预警 -->
        <aside class="ops-sidebar">
          <div class="ops-panel">
            <div class="ops-panel-head">
              <el-icon><OfficeBuilding /></el-icon>
              <span>节点群列 (Rooms)</span>
            </div>
            <div class="ops-room-list">
              <button
                v-for="room in rooms"
                :key="room.id"
                class="ops-room-btn"
                :class="{ active: selectedRoom === room.id }"
                @click="selectRoom(room.id)"
              >
                <div class="ops-room-info">
                  <span class="room-name">
                    <i class="status-dot" :class="roomStats[room.id]?.color || 'green'"></i>
                    {{ room.name }}
                  </span>
                  <span class="room-status" :class="roomStats[room.id]?.color || 'green'">
                    {{ roomStats[room.id]?.usage === 100 && roomStats[room.id]?.total > 0 ? '满座' : (roomStats[room.id]?.usage > 0 ? '占用中' : '空闲') }}
                  </span>
                </div>
                <div class="ops-room-bar">
                  <div class="bar-fill" :class="roomStats[room.id]?.color || 'green'" :style="{ width: `${roomStats[room.id]?.usage || 0}%` }"></div>
                </div>
              </button>
            </div>
          </div>

          <div class="ops-panel alert-panel" v-if="maintenanceSeatsCount > 0">
            <div class="ops-panel-head warning">
              <el-icon><Warning /></el-icon>
              <span>干预预警 (Alerts)</span>
            </div>
            <div class="alert-content">
              当前有 <strong>{{ maintenanceSeatsCount }}</strong> 个节点处于维护离线状态，可能会导致高峰期资源熔断，请尽快安排检修。
            </div>
          </div>
        </aside>

        <!-- 右侧面板：物理区域编排平面图 -->
        <main class="ops-main" v-loading="seatLoading">
          <div class="ops-toolbar">
            <div class="ops-filters">
              <button class="ops-filter-btn" :class="{ active: statusFilter === 'all' }" @click="statusFilter = 'all'">全景扫描</button>
              <button class="ops-filter-btn" :class="{ active: statusFilter === 'free' }" @click="statusFilter = 'free'">可用追踪</button>
              <button class="ops-filter-btn" :class="{ active: statusFilter === 'busy' }" @click="statusFilter = 'busy'">离线节点</button>
              <button class="ops-filter-btn power" :class="{ active: statusFilter === 'power' }" @click="statusFilter = 'power'">
                <el-icon><Lightning /></el-icon>能源位
              </button>
            </div>
            <div class="ops-legend">
              <span><i class="dot free"></i> 空闲</span>
              <span><i class="dot busy"></i> 维护/占用</span>
              <span><i class="dot power"></i> 电源</span>
            </div>
          </div>

          <div class="ops-room-details-card" v-if="selectedRoomData">
            <div class="details-header">
              <h2>{{ selectedRoomData.name }} <span class="room-status-badge" :class="roomStats[selectedRoomData.id]?.color || 'green'">{{ roomStats[selectedRoomData.id]?.usage === 100 && roomStats[selectedRoomData.id]?.total > 0 ? '满座' : (roomStats[selectedRoomData.id]?.usage > 0 ? '占用中' : '空闲') }}</span></h2>
              <span class="details-desc">{{ selectedRoomData.description || '当前物理空间编排区域的详细参数及运行状况' }}</span>
            </div>
            <div class="details-stats">
              <div class="stat-box">
                <span class="stat-label">总节点容量</span>
                <span class="stat-value">{{ totalSeats }}</span>
              </div>
              <div class="stat-box">
                <span class="stat-label">健康可用节点</span>
                <span class="stat-value text-green">{{ freeSeatsCount }}</span>
              </div>
              <div class="stat-box">
                <span class="stat-label">维护离线节点</span>
                <span class="stat-value text-red">{{ maintenanceSeatsCount }}</span>
              </div>
              <div class="stat-box">
                <span class="stat-label">高能电源覆盖</span>
                <span class="stat-value text-yellow">{{ powerSeatsCount }}</span>
              </div>
              <div class="stat-box">
                <span class="stat-label">实时空间负载</span>
                <span class="stat-value" :class="{'text-red': selectedRoomUsage === 100 && totalSeats > 0, 'text-yellow': selectedRoomUsage > 0 && selectedRoomUsage < 100}">{{ selectedRoomUsage }}%</span>
              </div>
            </div>
          </div>

          <div class="ops-floor-plan">
            <template v-if="filteredSeats.length">
              <!-- 按逻辑区域划分座位，模拟真实物理空间 -->
              <div v-for="(zone, zIndex) in physicalZones" :key="zIndex" class="ops-zone">
                <div class="ops-zone-label">
                  <span>ZONE {{ ['A','B','C','D'][zIndex] }}</span>
                  <em>{{ zone.name }}</em>
                </div>
                <div class="ops-seat-matrix">
                  <div
                    v-for="seat in zone.seats"
                    :key="seat.id"
                    class="ops-node"
                    :class="[
                      seat.status === 1 ? 'is-free' : 'is-busy',
                      seat.has_power ? 'has-power' : ''
                    ]"
                    @click="openBookingDialog(seat)"
                  >
                    <div class="node-ring"></div>
                    <div class="node-core">
                      <span class="node-id">{{ seat.seat_number }}</span>
                      <el-icon class="node-power-icon" v-if="seat.has_power"><Lightning /></el-icon>
                    </div>
                    <!-- 模拟热力条/状态槽 -->
                    <div class="node-timeline">
                      <span class="timeline-slot" :class="{ filled: seat.status !== 1 }"></span>
                      <span class="timeline-slot"></span>
                      <span class="timeline-slot"></span>
                    </div>
                  </div>
                </div>
              </div>
            </template>
            <div v-else class="ops-empty">
              <div class="radar-scan"></div>
              <p>雷达扫描：未发现符合条件的节点</p>
            </div>
          </div>
        </main>
      </div>
    </template>

    <!-- ============================================== -->
    <!-- PORTAL: STUDENT LIGHTWEIGHT MODE               -->
    <!-- ============================================== -->
    <template v-else>
      <section class="booking-hero portal-fade-up">
        <div class="hero-orb hero-orb-a"></div>
        <div class="hero-orb hero-orb-b"></div>
        <div class="hero-shell">
          <div class="hero-copy">
            <div class="hero-badge">Seat Booking</div>
            <h2>让选位更清晰、更安静、更高效</h2>
            <p>学生端保留轻量、直观的选位体验，用更舒服的卡片结构快速完成预约。</p>

            <div class="hero-pills">
              <div class="hero-pill accent">{{ roomInsight }}</div>
              <div class="hero-pill">当前房间 {{ selectedRoomData?.name || '未选择' }}</div>
              <div class="hero-pill">{{ freeSeatsCount }} 个可用座位</div>
            </div>

            <div class="hero-actions">
              <el-button type="primary" size="large" class="hero-primary-btn" @click="go('/portal/my-reservations')">
                我的预约
              </el-button>
              <el-button size="large" class="hero-secondary-btn" @click="go('/portal/notices')">
                查看公告
              </el-button>
            </div>
          </div>

          <div class="hero-side">
            <div class="hero-focus-card">
              <div class="hero-focus-top">
                <div>
                  <span class="hero-focus-label">本房间概览</span>
                  <strong class="hero-focus-value">{{ selectedRoomUsage }}%</strong>
                </div>
                <div class="hero-focus-badge">{{ selectedRoomName }}</div>
              </div>
              <div class="hero-progress">
                <span :style="{ width: `${selectedRoomUsage}%` }"></span>
              </div>
              <div class="hero-focus-grid">
                <div class="hero-focus-item">
                  <span>总座位</span>
                  <strong>{{ totalSeats }}</strong>
                </div>
                <div class="hero-focus-item">
                  <span>可预约</span>
                  <strong>{{ freeSeatsCount }}</strong>
                </div>
                <div class="hero-focus-item">
                  <span>维护中</span>
                  <strong>{{ maintenanceSeatsCount }}</strong>
                </div>
                <div class="hero-focus-item">
                  <span>电源位</span>
                  <strong>{{ powerSeatsCount }}</strong>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <el-card shadow="hover" class="control-card portal-hover">
        <div class="control-head">
          <div>
            <div class="section-title">选择自习室</div>
            <div class="section-subtitle">先选自习室，再挑选适合的座位进行预约。</div>
          </div>
          <el-select v-model="selectedRoom" placeholder="请选择自习室" size="large" class="room-select" @change="fetchSeats">
            <el-option v-for="room in rooms" :key="room.id" :label="room.name" :value="room.id" />
          </el-select>
        </div>

        <div class="room-chip-row" v-if="rooms.length">
          <button
            v-for="room in rooms"
            :key="room.id"
            type="button"
            class="room-chip"
            :class="{ active: selectedRoom === room.id }"
            @click="selectRoom(room.id)"
          >
            <el-icon><OfficeBuilding /></el-icon>
            <span>{{ room.name }}</span>
          </button>
        </div>
      </el-card>

      <el-card shadow="hover" class="seat-panel portal-hover" v-if="selectedRoom">
        <template #header>
          <div class="seat-panel-head">
            <div>
              <div class="section-title">座位分布</div>
              <div class="section-subtitle">卡片式座位矩阵，快速识别空闲和电源信息。</div>
            </div>
            <div class="seat-legend">
              <span class="legend-item"><i class="dot free"></i>可预约</span>
              <span class="legend-item"><i class="dot busy"></i>维护中</span>
              <span class="legend-item"><i class="dot power"></i>电源位</span>
            </div>
          </div>
        </template>

        <div class="filter-row">
          <button
            v-for="item in filterOptions"
            :key="item.key"
            type="button"
            class="filter-pill"
            :class="{ active: statusFilter === item.key }"
            @click="statusFilter = item.key"
          >
            <span>{{ item.label }}</span>
            <strong>{{ item.count }}</strong>
          </button>
        </div>

        <div class="seat-layout" v-loading="seatLoading">
          <div class="seat-content">
            <div v-if="filteredSeats.length" class="seat-grid">
              <button
                v-for="seat in filteredSeats"
                :key="seat.id"
                type="button"
                class="seat-item portal-hover"
                :class="seatCardClass(seat)"
                @click="openBookingDialog(seat)"
              >
                <div class="seat-top">
                  <div class="seat-number">Seat {{ seat.seat_number }}</div>
                  <div class="seat-chip" :class="seat.status === 1 ? 'chip-free' : 'chip-busy'">
                    {{ seat.status === 1 ? '可预约' : '维护中' }}
                  </div>
                </div>
                <div class="seat-center">
                  <div class="seat-visual">
                    <div class="seat-backrest"></div>
                    <div class="seat-cushion"></div>
                  </div>
                </div>
                <div class="seat-meta-row">
                  <div class="seat-meta-pill">
                    <el-icon v-if="seat.has_power"><Lightning /></el-icon>
                    <span>{{ seat.has_power ? '电源位' : '普通位' }}</span>
                  </div>
                  <div class="seat-meta-pill muted">
                    <span>{{ seat.status === 1 ? '点击可预约' : '暂不可用' }}</span>
                  </div>
                </div>
              </button>
            </div>
            <el-empty v-else description="当前筛选条件下没有可展示的座位" />
          </div>
        </div>
      </el-card>
    </template>

    <!-- 统一的预约弹窗 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="520px" destroy-on-close :class="{'ops-dialog': isAdminView}">
      <div class="booking-dialog-body">
        <div class="dialog-seat-banner" :class="{'ops-banner': isAdminView}">
          <div>
            <span class="dialog-seat-label">{{ isAdminView ? '干预目标节点' : '当前座位' }}</span>
            <strong class="dialog-seat-number">Seat {{ currentSeat?.seat_number || '-' }}</strong>
          </div>
          <div class="dialog-seat-tags">
            <el-tag size="small" :type="currentSeat?.status === 1 ? 'success' : 'danger'" :effect="isAdminView ? 'dark' : 'light'">
              {{ currentSeat?.status === 1 ? (isAdminView ? '状态: ONLINE' : '可预约') : (isAdminView ? '状态: OFFLINE' : '维护中') }}
            </el-tag>
            <el-tag size="small" type="warning" v-if="currentSeat?.has_power" :effect="isAdminView ? 'dark' : 'light'">电源覆盖</el-tag>
          </div>
        </div>

        <el-form :model="bookingForm" label-width="80px" class="booking-form">
          <el-form-item label="归属空间">
            <el-input :value="selectedRoomName" disabled />
          </el-form-item>
          <el-form-item label="预约日期">
            <el-date-picker
              v-model="bookingForm.date"
              type="date"
              placeholder="选择日期"
              class="w-full"
              :disabled-date="disablePastDates"
              value-format="YYYY-MM-DD"
            />
          </el-form-item>
          <el-form-item label="时间段">
            <el-time-picker
              v-model="bookingForm.timeRange"
              is-range
              range-separator="至"
              start-placeholder="开始时间"
              end-placeholder="结束时间"
              format="HH:mm:ss"
              value-format="HH:mm:ss"
              class="w-full"
            />
          </el-form-item>
        </el-form>
        <div v-if="!isAdminView" class="booking-tip">
          同一时间段仅允许保留一条有效预约，系统会自动拦截重复预约和时间冲突。
        </div>
      </div>
      <template #footer>
        <el-button @click="dialogVisible = false">{{ isAdminView ? '取消干预' : '取消' }}</el-button>
        <el-button type="primary" @click="submitBooking" :loading="loading">{{ submitButtonText }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import request from '../../utils/request'
import { Lightning, OfficeBuilding, Warning } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

interface RoomItem {
  id: number
  name: string
  description?: string
}

interface SeatItem {
  id: number
  seat_number: string | number
  status: number
  has_power?: boolean
}

interface ReservationItem {
  id: number
  user_id: number
  seat_id: number
  date: string
  start_time: string
  end_time: string
  status: string
}

type SeatFilterKey = 'all' | 'free' | 'busy' | 'power'

const route = useRoute()
const router = useRouter()
const rooms = ref<RoomItem[]>([])
const roomStats = ref<Record<number, { total: number, busy: number, usage: number, color: string }>>({})
const selectedRoom = ref<number | null>(null)
const seats = ref<SeatItem[]>([])
const user = ref<any>(JSON.parse(localStorage.getItem('user') || '{}'))
const userReservations = ref<ReservationItem[]>([])
const dialogVisible = ref(false)
const currentSeat = ref<SeatItem | null>(null)
const loading = ref(false)
const seatLoading = ref(false)
const statusFilter = ref<SeatFilterKey>('all')
const bookingForm = reactive({ date: '', timeRange: [] as string[] })

const isAdminView = computed(() => route.path.startsWith('/admin'))
const selectedRoomData = computed(() => rooms.value.find((room) => room.id === selectedRoom.value) || null)
const selectedRoomName = computed(() => selectedRoomData.value?.name || '未选择自习室')
const totalSeats = computed(() => seats.value.length)
const freeSeatsCount = computed(() => seats.value.filter((seat) => seat.status === 1).length)
const maintenanceSeatsCount = computed(() => seats.value.filter((seat) => seat.status !== 1).length)
const powerSeatsCount = computed(() => seats.value.filter((seat) => Boolean(seat.has_power)).length)
const selectedRoomUsage = computed(() => {
  if (!totalSeats.value) return 0
  return Math.round(((totalSeats.value - freeSeatsCount.value) / totalSeats.value) * 100)
})
const activeReservations = computed(() =>
  userReservations.value.filter((item) => item.status === 'pending' || item.status === 'active')
)

const roomInsight = computed(() => {
  if (!selectedRoom.value || !totalSeats.value) return '先选择一个自习室开始查看'
  if (selectedRoomUsage.value >= 85) return '当前房间利用率较高，建议关注高峰时段'
  if (selectedRoomUsage.value >= 50) return '当前房间使用情况平稳，适合继续正常开放'
  return '当前房间余量充足，适合引导更多预约'
})

// const activeFilterLabel = computed(() => {
//   const map: Record<SeatFilterKey, string> = {
//     all: '全部座位',
//     free: '仅看可预约',
//     busy: '仅看维护中',
//     power: '仅看电源位'
//   }
//   return map[statusFilter.value]
// })

const filterOptions = computed(() => [
  { key: 'all' as SeatFilterKey, label: '全部', count: seats.value.length },
  { key: 'free' as SeatFilterKey, label: '可预约', count: freeSeatsCount.value },
  { key: 'busy' as SeatFilterKey, label: '维护中', count: maintenanceSeatsCount.value },
  { key: 'power' as SeatFilterKey, label: '电源位', count: powerSeatsCount.value }
])

const filteredSeats = computed(() => {
  switch (statusFilter.value) {
    case 'free':
      return seats.value.filter((seat) => seat.status === 1)
    case 'busy':
      return seats.value.filter((seat) => seat.status !== 1)
    case 'power':
      return seats.value.filter((seat) => Boolean(seat.has_power))
    default:
      return seats.value
  }
})

// 将座位切分为 4 个虚拟物理区域，用于 Admin 极端控制台视图展示
const physicalZones = computed(() => {
  const all = filteredSeats.value
  if (!all.length) return []
  const chunkSize = Math.ceil(all.length / 4)
  const zoneNames = ['前排静音区 (Quiet Zone)', '中庭开放区 (Open Area)', '靠窗景观区 (Window Side)', '电源特区 (Power Grid)']
  const zones = []
  for (let i = 0; i < 4; i++) {
    const chunk = all.slice(i * chunkSize, (i + 1) * chunkSize)
    if (chunk.length) {
      zones.push({ name: zoneNames[i], seats: chunk })
    }
  }
  return zones
})

const dialogTitle = computed(() => isAdminView.value ? '节点调度干预' : '确认预约')
const submitButtonText = computed(() => isAdminView.value ? '执行调度指令' : '确认预约')
const formatLocalDate = (date: Date) => {
  const year = date.getFullYear()
  const month = `${date.getMonth() + 1}`.padStart(2, '0')
  const day = `${date.getDate()}`.padStart(2, '0')
  return `${year}-${month}-${day}`
}
const todayString = () => formatLocalDate(new Date())
const disablePastDates = (time: Date) => formatLocalDate(time) < todayString()
const hasTimeOverlap = (startA: string, endA: string, startB: string, endB: string) => startA < endB && endA > startB

const go = (path: string) => router.push(path)

const fetchUserReservations = async () => {
  if (!user.value.id) {
    userReservations.value = []
    return
  }
  try {
    userReservations.value = await request.get(`/api/seats/reservations/user/${user.value.id}`)
  } catch (error) {
    console.error('Failed to fetch user reservations')
  }
}

const fetchRooms = async () => {
  try {
    rooms.value = await request.get('/api/seats/rooms')
    
    // Fetch seats for all rooms to calculate status
    const statsPromises = rooms.value.map(async (room) => {
      try {
        const roomSeats: SeatItem[] = (await request.get(`/api/seats/rooms/${room.id}/seats`)) as any
        const total = roomSeats.length
        const busy = roomSeats.filter((s: SeatItem) => s.status !== 1).length
        const usage = total === 0 ? 0 : Math.round((busy / total) * 100)
        
        let color = 'green'
        if (usage === 100 && total > 0) color = 'red'
        else if (usage > 0) color = 'yellow'
        
        roomStats.value[room.id] = { total, busy, usage, color }
      } catch (e) {
        console.error(`Failed to fetch seats for room ${room.id}`)
      }
    })
    
    await Promise.all(statsPromises)

    if (!selectedRoom.value && rooms.value.length) {
      selectedRoom.value = rooms.value[0].id
      await fetchSeats()
    }
  } catch (error) {
    ElMessage.error('获取自习室列表失败')
  }
}

const fetchSeats = async () => {
  if (!selectedRoom.value) return
  seatLoading.value = true
  try {
    seats.value = await request.get(`/api/seats/rooms/${selectedRoom.value}/seats`)
  } catch (error) {
    ElMessage.error('获取座位信息失败')
  } finally {
    seatLoading.value = false
  }
}

const selectRoom = async (roomId: number) => {
  selectedRoom.value = roomId
  await fetchSeats()
}

const openBookingDialog = (seat: SeatItem) => {
  if (seat.status !== 1 && !isAdminView.value) {
    ElMessage.warning('该座位当前不可预约')
    return
  }
  currentSeat.value = seat
  dialogVisible.value = true
  bookingForm.date = todayString()
  bookingForm.timeRange = ['08:00:00', '12:00:00']
}

const submitBooking = async () => {
  if (!currentSeat.value) return
  if (!bookingForm.date || !bookingForm.timeRange || bookingForm.timeRange.length !== 2) {
    ElMessage.warning('请完整填写预约时间')
    return
  }
  if (bookingForm.date < todayString()) {
    ElMessage.warning('不能预约过去的日期')
    return
  }
  if (bookingForm.timeRange[0] >= bookingForm.timeRange[1]) {
    ElMessage.warning('结束时间必须晚于开始时间')
    return
  }
  const conflictingReservation = activeReservations.value.find((item) =>
    item.date === bookingForm.date &&
    hasTimeOverlap(item.start_time, item.end_time, bookingForm.timeRange[0], bookingForm.timeRange[1])
  )
  if (conflictingReservation) {
    const isSameSeatAndRange =
      conflictingReservation.seat_id === currentSeat.value.id &&
      conflictingReservation.start_time === bookingForm.timeRange[0] &&
      conflictingReservation.end_time === bookingForm.timeRange[1]
    ElMessage.warning(
      isSameSeatAndRange
        ? '你已经预约过该座位的这个时间段，请勿重复提交'
        : '该时间段你已有其他预约，请更换时间后再试'
    )
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
    ElMessage.success(isAdminView.value ? '调度指令已执行' : '预约成功！')
    dialogVisible.value = false
    await Promise.all([fetchSeats(), fetchUserReservations()])
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '操作失败')
  } finally {
    loading.value = false
  }
}

const seatCardClass = (seat: SeatItem) => ({
  'seat-free': seat.status === 1,
  'seat-busy': seat.status !== 1,
  'seat-power': Boolean(seat.has_power)
})

watch(selectedRoom, () => {
  statusFilter.value = 'all'
})

onMounted(fetchRooms)
onMounted(fetchUserReservations)
</script>

<style scoped>
.booking-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ========================================================= */
/* PORTAL MODE STYLES (STUDENT VIEW)                         */
/* ========================================================= */
.portal-mode .booking-hero {
  position: relative;
  overflow: hidden;
  padding: 28px;
  border-radius: 32px;
  border: 1px solid rgba(148, 163, 184, 0.12);
  box-shadow: 0 24px 64px rgba(15, 23, 42, 0.08);
  background: linear-gradient(135deg, #eef4ff 0%, #f8fbff 45%, #f4f9ff 100%);
}
.portal-mode .hero-orb {
  position: absolute;
  border-radius: 999px;
  pointer-events: none;
  filter: blur(8px);
}
.portal-mode .hero-orb-a {
  width: 220px;
  height: 220px;
  right: -50px;
  top: -40px;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.22), rgba(59, 130, 246, 0));
}
.portal-mode .hero-orb-b {
  width: 260px;
  height: 260px;
  left: 36%;
  bottom: -150px;
  background: radial-gradient(circle, rgba(168, 85, 247, 0.20), rgba(168, 85, 247, 0));
}
.portal-mode .hero-shell {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 24px;
  align-items: stretch;
}
.portal-mode .hero-badge {
  display: inline-flex;
  padding: 7px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  background: rgba(37, 99, 235, 0.08);
  color: #1d4ed8;
}
.portal-mode .hero-copy h2 {
  margin: 16px 0 12px;
  font-size: 36px;
  line-height: 1.15;
  letter-spacing: -0.03em;
  color: #0f172a;
}
.portal-mode .hero-copy p {
  margin: 0;
  max-width: 760px;
  font-size: 15px;
  line-height: 1.85;
  color: #475569;
}
.portal-mode .hero-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 22px;
}
.portal-mode .hero-pill {
  padding: 9px 14px;
  border-radius: 999px;
  font-size: 13px;
  background: rgba(255, 255, 255, 0.78);
  color: #334155;
  border: 1px solid rgba(148, 163, 184, 0.12);
}
.portal-mode .hero-pill.accent {
  font-weight: 700;
}
.portal-mode .hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 24px;
}
.portal-mode .hero-primary-btn,
.portal-mode .hero-secondary-btn {
  height: 46px;
  padding: 0 20px;
  border-radius: 999px;
}
.portal-mode .hero-side {
  display: grid;
  gap: 14px;
}
.portal-mode .hero-focus-card {
  padding: 20px;
  border-radius: 26px;
  backdrop-filter: blur(12px);
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(255, 255, 255, 0.86);
  box-shadow: 0 20px 40px rgba(37, 99, 235, 0.08);
}
.portal-mode .hero-focus-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}
.portal-mode .hero-focus-label {
  display: block;
  font-size: 12px;
  color: #64748b;
}
.portal-mode .hero-focus-value {
  display: block;
  margin-top: 8px;
  font-size: 38px;
  line-height: 1;
  color: #0f172a;
}
.portal-mode .hero-focus-badge {
  padding: 8px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  background: linear-gradient(135deg, #eff6ff, #eef2ff);
  color: #4338ca;
}
.portal-mode .hero-progress {
  margin-top: 18px;
  height: 10px;
  overflow: hidden;
  border-radius: 999px;
  background: #e2e8f0;
}
.portal-mode .hero-progress span {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, #22c55e, #60a5fa, #8b5cf6);
}
.portal-mode .hero-focus-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-top: 18px;
}
.portal-mode .hero-focus-item {
  padding: 14px 16px;
  border-radius: 18px;
  background: linear-gradient(180deg, #fbfdff, #f4f8ff);
}
.portal-mode .hero-focus-item span {
  display: block;
  color: #64748b;
}
.portal-mode .hero-focus-item strong {
  display: block;
  color: #0f172a;
}

.portal-mode .control-card,
.portal-mode .seat-panel {
  border: none;
  border-radius: 28px;
  box-shadow: 0 20px 48px rgba(15, 23, 42, 0.06);
}
.portal-mode .control-head,
.portal-mode .seat-panel-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}
.portal-mode .section-title {
  font-size: 18px;
  font-weight: 800;
  color: #0f172a;
}
.portal-mode .section-subtitle {
  margin-top: 4px;
  color: #64748b;
  font-size: 13px;
  line-height: 1.7;
}
.portal-mode .room-select {
  width: min(420px, 100%);
}
.portal-mode .room-chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 18px;
}
.portal-mode .room-chip {
  appearance: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-radius: 999px;
  border: 1px solid rgba(148, 163, 184, 0.16);
  background: #ffffff;
  color: #334155;
  cursor: pointer;
  transition: all 0.2s ease;
}
.portal-mode .room-chip:hover,
.portal-mode .room-chip.active {
  transform: translateY(-1px);
  color: #1d4ed8;
  border-color: rgba(37, 99, 235, 0.22);
  box-shadow: 0 10px 24px rgba(37, 99, 235, 0.08);
}
.portal-mode .seat-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
}
.portal-mode .legend-item {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #64748b;
  font-size: 12px;
}
.portal-mode .dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
}
.portal-mode .dot.free { background: #22c55e; }
.portal-mode .dot.busy { background: #ef4444; }
.portal-mode .dot.power { background: #f59e0b; }

.portal-mode .filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.portal-mode .filter-pill {
  appearance: none;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: 999px;
  border: 1px solid rgba(148, 163, 184, 0.16);
  background: #ffffff;
  color: #334155;
  cursor: pointer;
}
.portal-mode .filter-pill.active {
  color: #1d4ed8;
  border-color: rgba(37, 99, 235, 0.2);
  background: linear-gradient(135deg, #eff6ff, #f5f7ff);
}
.portal-mode .filter-pill strong {
  font-size: 12px;
}
.portal-mode .seat-layout {
  margin-top: 18px;
}
.portal-mode .seat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 16px;
}
.portal-mode .seat-item {
  appearance: none;
  width: 100%;
  padding: 18px;
  border-radius: 24px;
  border: 1px solid rgba(148, 163, 184, 0.14);
  background: linear-gradient(180deg, #ffffff, #f8fbff);
  cursor: pointer;
  text-align: left;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}
.portal-mode .seat-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 18px 34px rgba(15, 23, 42, 0.08);
}
.portal-mode .seat-free { border-color: rgba(34, 197, 94, 0.18); }
.portal-mode .seat-busy { opacity: 0.82; border-color: rgba(239, 68, 68, 0.14); }
.portal-mode .seat-power { box-shadow: inset 0 0 0 1px rgba(245, 158, 11, 0.14); }
.portal-mode .seat-top { display: flex; justify-content: space-between; align-items: center; gap: 12px; }
.portal-mode .seat-number { font-size: 17px; font-weight: 800; color: #0f172a; }
.portal-mode .seat-chip { padding: 6px 10px; border-radius: 999px; font-size: 12px; font-weight: 700; }
.portal-mode .chip-free { background: rgba(34, 197, 94, 0.12); color: #15803d; }
.portal-mode .chip-busy { background: rgba(239, 68, 68, 0.12); color: #dc2626; }
.portal-mode .seat-center { display: flex; justify-content: center; padding: 22px 0 18px; }
.portal-mode .seat-visual { position: relative; width: 74px; height: 64px; }
.portal-mode .seat-backrest { width: 54px; height: 18px; margin: 0 auto; border-radius: 14px 14px 8px 8px; background: linear-gradient(180deg, #cbd5e1, #94a3b8); }
.portal-mode .seat-cushion { position: absolute; left: 50%; bottom: 0; width: 74px; height: 38px; transform: translateX(-50%); border-radius: 20px; background: linear-gradient(180deg, #eff6ff, #dbeafe); box-shadow: inset 0 6px 14px rgba(255, 255, 255, 0.5); }
.portal-mode .seat-free .seat-cushion { background: linear-gradient(180deg, #dcfce7, #86efac); }
.portal-mode .seat-busy .seat-cushion { background: linear-gradient(180deg, #fee2e2, #fca5a5); }
.portal-mode .seat-meta-row { display: grid; gap: 8px; }
.portal-mode .seat-meta-pill { display: inline-flex; align-items: center; gap: 6px; padding: 8px 10px; border-radius: 12px; background: #f8fafc; color: #475569; font-size: 12px; }
.portal-mode .seat-meta-pill.muted { color: #64748b; }
.portal-mode .booking-dialog-body { display: grid; gap: 16px; }
.portal-mode .booking-tip { padding: 12px 14px; border-radius: 14px; background: rgba(37, 99, 235, 0.06); color: #475569; font-size: 13px; line-height: 1.6; }
.portal-mode .dialog-seat-banner { display: flex; justify-content: space-between; align-items: center; gap: 12px; padding: 18px; border-radius: 22px; background: linear-gradient(135deg, #eff6ff, #f5f3ff); }
.portal-mode .dialog-seat-label { display: block; color: #64748b; font-size: 12px; }
.portal-mode .dialog-seat-number { display: block; margin-top: 8px; color: #0f172a; font-size: 24px; }
.portal-mode .dialog-seat-tags { display: flex; flex-wrap: wrap; gap: 8px; }

/* ========================================================= */
/* ADMIN MODE STYLES (MODERN LIGHT SAAS CONSOLE)             */
/* ========================================================= */
.ops-console-mode {
  min-height: calc(100vh - 120px);
  background: #f8fafc; /* Light modern base */
  border-radius: 24px;
  color: #0f172a;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 20px 40px -10px rgba(0, 0, 0, 0.03);
  border: 1px solid #e2e8f0;
  font-family: 'Inter', system-ui, sans-serif;
}

.ops-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 32px;
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
}

.ops-header-left {
  display: flex;
  align-items: center;
  gap: 32px;
}

.ops-logo {
  display: flex;
  flex-direction: column;
  position: relative;
  padding-left: 20px;
}

.pulse-ring {
  position: absolute;
  left: 0;
  top: 6px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #3b82f6;
  box-shadow: 0 0 12px rgba(59, 130, 246, 0.6);
  animation: pulse 2s infinite;
}

.ops-logo strong {
  font-size: 16px;
  letter-spacing: 0.1em;
  color: #0f172a;
}

.ops-logo em {
  font-size: 10px;
  color: #64748b;
  font-style: normal;
  letter-spacing: 0.05em;
  margin-top: 2px;
}

.ops-title h1 {
  font-size: 20px;
  margin: 0 0 4px;
  color: #0f172a;
  font-weight: 700;
}

.ops-title p {
  margin: 0;
  font-size: 13px;
  color: #64748b;
}

.ops-header-right {
  display: flex;
  gap: 32px;
}

.ops-metric {
  text-align: right;
}

.ops-metric span {
  display: block;
  font-size: 11px;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 4px;
}

.ops-metric strong {
  font-size: 28px;
  line-height: 1;
  color: #0f172a;
  font-weight: 600;
}

.ops-metric strong.text-danger {
  color: #ef4444;
  text-shadow: none;
}

.ops-metric small {
  font-size: 14px;
  color: #64748b;
  margin-left: 4px;
}

.ops-layout {
  display: flex;
  flex: 1;
  min-height: 0;
}

.ops-sidebar {
  width: 280px;
  background: #ffffff;
  border-right: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  padding: 20px;
  gap: 24px;
  overflow-y: auto;
}

.ops-panel-head {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 16px;
  font-weight: 600;
}

.ops-panel-head.warning {
  color: #d97706;
}

.ops-room-list {
  display: grid;
  gap: 8px;
}

.ops-room-btn {
  appearance: none;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 12px 14px;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #334155;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
}

.ops-room-btn:hover {
  background: #f8fafc;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.ops-room-btn.active {
  background: #eff6ff;
  border-color: #bfdbfe;
  box-shadow: inset 3px 0 0 #3b82f6, 0 4px 6px -1px rgba(59, 130, 246, 0.1);
}

.ops-room-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.room-name {
  font-size: 14px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
  color: #0f172a;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}
.status-dot.red { background: #ef4444; box-shadow: 0 0 6px rgba(239, 68, 68, 0.4); }
.status-dot.yellow { background: #f59e0b; box-shadow: 0 0 6px rgba(245, 158, 11, 0.4); }
.status-dot.green { background: #10b981; box-shadow: 0 0 6px rgba(16, 185, 129, 0.4); }

.room-status {
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: bold;
}
.room-status.red { color: #b91c1c; background: #fee2e2; }
.room-status.yellow { color: #b45309; background: #fef3c7; }
.room-status.green { color: #047857; background: #d1fae5; }

.ops-room-bar {
  height: 4px;
  background: #e2e8f0;
  border-radius: 2px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  transition: width 0.5s ease;
}
.bar-fill.red { background: linear-gradient(90deg, #f87171, #ef4444); }
.bar-fill.yellow { background: linear-gradient(90deg, #fbbf24, #f59e0b); }
.bar-fill.green { background: linear-gradient(90deg, #34d399, #10b981); }

.alert-panel {
  background: #fffbeb;
  border: 1px solid #fde68a;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
}

.alert-content {
  font-size: 13px;
  line-height: 1.6;
  color: #b45309;
}

.alert-content strong {
  color: #92400e;
  font-size: 16px;
}

.ops-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #f8fafc;
  position: relative;
  overflow-y: auto;
}

.ops-main::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(#e2e8f0 1px, transparent 1px),
    linear-gradient(90deg, #e2e8f0 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none;
  opacity: 0.5;
}

.ops-toolbar {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 32px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid #e2e8f0;
}

.ops-filters {
  display: flex;
  gap: 8px;
  background: #f1f5f9;
  padding: 4px;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
}

.ops-filter-btn {
  appearance: none;
  background: transparent;
  border: none;
  color: #64748b;
  padding: 6px 16px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}

.ops-filter-btn:hover {
  color: #334155;
  background: #e2e8f0;
}

.ops-filter-btn.active {
  background: #ffffff;
  color: #0f172a;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.ops-filter-btn.power.active {
  color: #d97706;
}

.ops-room-details-card {
  margin: 24px 32px 0;
  padding: 24px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
  position: relative;
  z-index: 1;
}

.details-header {
  margin-bottom: 20px;
}

.details-header h2 {
  font-size: 20px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 8px 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.room-status-badge {
  font-size: 11px;
  padding: 4px 8px;
  border-radius: 6px;
  font-weight: bold;
}
.room-status-badge.red { color: #b91c1c; background: #fee2e2; border: 1px solid #fca5a5; }
.room-status-badge.yellow { color: #b45309; background: #fef3c7; border: 1px solid #fcd34d; }
.room-status-badge.green { color: #047857; background: #d1fae5; border: 1px solid #6ee7b7; }

.details-desc {
  font-size: 13px;
  color: #64748b;
}

.details-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 16px;
}

.stat-box {
  background: #f8fafc;
  border-radius: 12px;
  padding: 16px;
  border: 1px solid #f1f5f9;
}

.stat-label {
  display: block;
  font-size: 11px;
  color: #64748b;
  margin-bottom: 8px;
  text-transform: uppercase;
  font-weight: 600;
}

.stat-value {
  display: block;
  font-size: 24px;
  font-weight: 700;
  color: #0f172a;
}

.stat-value.text-green { color: #10b981; }
.stat-value.text-red { color: #ef4444; }
.stat-value.text-yellow { color: #f59e0b; }

.ops-legend {
  display: flex;
  gap: 16px;
}

.ops-legend span {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #64748b;
  font-weight: 500;
}

.ops-legend .dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.ops-legend .dot.free { background: #10b981; }
.ops-legend .dot.busy { background: #ef4444; }
.ops-legend .dot.power { background: #f59e0b; }

.ops-floor-plan {
  padding: 32px;
  position: relative;
  z-index: 1;
  display: grid;
  gap: 40px;
}

.ops-zone {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
  position: relative;
}

.ops-zone::before {
  content: '';
  position: absolute;
  top: 0; left: 0; width: 30px; height: 30px;
  border-top: 3px solid #cbd5e1;
  border-left: 3px solid #cbd5e1;
  border-top-left-radius: 16px;
}

.ops-zone-label {
  display: flex;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 24px;
}

.ops-zone-label span {
  font-size: 18px;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: 0.05em;
}

.ops-zone-label em {
  font-size: 12px;
  color: #64748b;
  font-style: normal;
  text-transform: uppercase;
}

.ops-seat-matrix {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 20px;
}

.ops-node {
  position: relative;
  height: 90px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.ops-node:hover {
  transform: translateY(-4px) scale(1.02);
  border-color: #cbd5e1;
  z-index: 2;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.node-ring {
  position: absolute;
  inset: -1px;
  border-radius: inherit;
  opacity: 0;
  transition: opacity 0.3s;
}

.ops-node.is-free .node-ring {
  box-shadow: inset 0 0 0 2px rgba(16, 185, 129, 0.4);
}

.ops-node.is-busy .node-ring {
  box-shadow: inset 0 0 0 2px rgba(239, 68, 68, 0.4);
}

.ops-node:hover .node-ring {
  opacity: 1;
}

.node-core {
  display: flex;
  align-items: center;
  gap: 6px;
  z-index: 1;
}

.node-id {
  font-size: 20px;
  font-family: monospace;
  font-weight: 700;
}

.ops-node.is-free .node-id { color: #059669; }
.ops-node.is-busy .node-id { color: #dc2626; opacity: 0.8; }

.node-power-icon {
  color: #d97706;
  font-size: 14px;
}

.node-timeline {
  position: absolute;
  bottom: 8px;
  left: 12px;
  right: 12px;
  display: flex;
  gap: 2px;
  height: 4px;
}

.timeline-slot {
  flex: 1;
  background: #e2e8f0;
  border-radius: 2px;
}

.timeline-slot.filled {
  background: #f87171;
}

.ops-node.is-free .timeline-slot {
  background: #6ee7b7;
}

.ops-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: #64748b;
}

.radar-scan {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: 2px solid rgba(59, 130, 246, 0.2);
  position: relative;
  margin-bottom: 16px;
  overflow: hidden;
}

.radar-scan::after {
  content: '';
  position: absolute;
  top: 50%; left: 50%;
  width: 50%; height: 50%;
  background: conic-gradient(transparent, rgba(59, 130, 246, 0.4));
  transform-origin: 0 0;
  animation: radar 2s linear infinite;
}

@keyframes radar {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.4); }
  70% { box-shadow: 0 0 0 10px rgba(59, 130, 246, 0); }
  100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
}

/* ========================================================= */
/* SHARED MEDIA QUERIES                                      */
/* ========================================================= */
@media (max-width: 960px) {
  .ops-layout { flex-direction: column; }
  .ops-sidebar { width: 100%; border-right: none; border-bottom: 1px solid #e2e8f0; max-height: 300px; }
  .ops-header { flex-direction: column; align-items: flex-start; gap: 20px; }
}

/* Admin Dialog Overrides - Light Theme */
.ops-dialog :deep(.el-dialog) {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}
.ops-dialog :deep(.el-dialog__title) { color: #0f172a; font-weight: 700; }
.ops-dialog :deep(.el-form-item__label) { color: #475569; font-weight: 500; }
.ops-dialog :deep(.el-input__wrapper),
.ops-dialog :deep(.el-input.is-disabled .el-input__wrapper) {
  background: #f8fafc;
  box-shadow: 0 0 0 1px #e2e8f0 inset;
}
.ops-dialog :deep(.el-input__inner) { color: #0f172a; }
.ops-banner {
  background: #eff6ff !important;
  border: 1px solid #bfdbfe;
}
.ops-banner .dialog-seat-label { color: #3b82f6 !important; font-weight: 600; }
.ops-banner .dialog-seat-number { color: #1d4ed8 !important; }
</style>
