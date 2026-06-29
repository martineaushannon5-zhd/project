<template>
  <div class="room-page">
    <el-card class="hero-card portal-hover" shadow="hover">
      <div class="hero-main">
        <div>
          <div class="hero-badge">空间配置 · 自习室管理</div>
          <h2 class="hero-title">自习室管理中心</h2>
          <p class="hero-desc">统一维护自习室基础信息、批量生成座位，并查看座位概况。</p>
        </div>
        <div class="hero-actions">
          <el-button type="primary" :icon="Plus" @click="openDialog()">新增自习室</el-button>
          <el-button :icon="Refresh" @click="fetchRooms">刷新数据</el-button>
        </div>
      </div>
    </el-card>

    <el-card class="section-card portal-hover" shadow="hover">
      <template #header>
        <div class="section-header">
          <div>
            <div class="section-title">自习室列表</div>
            <div class="section-subtitle">点击行内操作可编辑、生成座位或查看座位详情。</div>
          </div>
        </div>
      </template>

      <el-table :data="rooms" v-loading="loading" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="自习室名称" min-width="180" />
        <el-table-column prop="description" label="描述" min-width="220" />
        <el-table-column prop="created_at" label="创建时间" min-width="180" />
        <el-table-column label="操作" width="360" fixed="right">
          <template #default="{ row }">
            <div class="row-actions">
              <el-button link type="primary" @click="openDialog(row)">编辑</el-button>
              <el-button link type="success" @click="openBatchDialog(row)">批量生成座位</el-button>
              <el-button link type="warning" @click="viewSeats(row)">座位概况</el-button>
              <el-button link type="danger" @click="removeRoom(row)">删除</el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <div class="bottom-grid">
      <el-card class="section-card portal-hover" shadow="hover">
        <template #header>
          <div class="section-header">
            <div>
              <div class="section-title">批量生成座位</div>
              <div class="section-subtitle">适合一次性为新自习室快速铺设座位。</div>
            </div>
          </div>
        </template>

        <el-form :model="batchForm" label-position="top" class="form-grid">
          <el-form-item label="座位前缀">
            <el-input v-model="batchForm.prefix" placeholder="如 A / B / C" />
          </el-form-item>
          <el-form-item label="生成数量">
            <el-input-number v-model="batchForm.count" :min="1" :max="200" class="w-full" />
          </el-form-item>
          <el-form-item label="电源配置">
            <el-switch v-model="batchForm.has_power" active-text="有电源" inactive-text="无电源" />
          </el-form-item>
        </el-form>
        <div class="footer-actions">
          <el-button type="primary" @click="submitBatch" :loading="batchSaving">生成座位</el-button>
        </div>
      </el-card>

      <el-card class="section-card portal-hover" shadow="hover">
        <template #header>
          <div class="section-header">
            <div>
              <div class="section-title">座位概况</div>
              <div class="section-subtitle">查看当前选中自习室的座位状态。</div>
            </div>
          </div>
        </template>
        <el-descriptions :column="1" border class="mb-4">
          <el-descriptions-item label="自习室">{{ currentRoom?.name || '未选择' }}</el-descriptions-item>
          <el-descriptions-item label="描述">{{ currentRoom?.description || '暂无' }}</el-descriptions-item>
        </el-descriptions>
        <el-table :data="seatList" border>
          <el-table-column prop="seat_number" label="座位号" />
          <el-table-column prop="status" label="状态">
            <template #default="{ row }">
              <el-tag :type="row.status === 1 ? 'success' : 'danger'">
                {{ row.status === 1 ? '正常' : '维护中' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="has_power" label="电源">
            <template #default="{ row }">
              <el-tag :type="row.has_power ? 'primary' : 'info'">
                {{ row.has_power ? '有' : '无' }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="520px" destroy-on-close>
      <el-form :model="form" label-position="top">
        <el-form-item label="名称">
          <el-input v-model="form.name" placeholder="请输入自习室名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="4" placeholder="请输入自习室描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm" :loading="saving">保存</el-button>
      </template>
    </el-dialog>

    <el-drawer v-model="seatDrawerVisible" title="座位概况" size="40%">
      <el-table :data="seatList" border>
        <el-table-column prop="seat_number" label="座位号" />
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'danger'">
              {{ row.status === 1 ? '正常' : '维护中' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="has_power" label="电源">
          <template #default="{ row }">
            <el-tag :type="row.has_power ? 'primary' : 'info'">
              {{ row.has_power ? '有' : '无' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import request from '../../utils/request'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Refresh } from '@element-plus/icons-vue'

const rooms = ref<any[]>([])
const loading = ref(false)
const saving = ref(false)
const batchSaving = ref(false)
const dialogVisible = ref(false)
const batchDialogVisible = ref(false)
const seatDrawerVisible = ref(false)
const currentRoom = ref<any>(null)
const seatList = ref<any[]>([])
const dialogTitle = ref('新增自习室')
const form = reactive({ id: null as number | null, name: '', description: '' })
const batchForm = reactive({ prefix: 'A', count: 30, has_power: true })

const fetchRooms = async () => {
  loading.value = true
  try {
    rooms.value = await request.get('/api/seats/rooms')
  } catch (error) {
    ElMessage.error('获取自习室失败')
  } finally {
    loading.value = false
  }
}

const openDialog = (row?: any) => {
  if (row) {
    dialogTitle.value = '编辑自习室'
    form.id = row.id
    form.name = row.name
    form.description = row.description || ''
  } else {
    dialogTitle.value = '新增自习室'
    form.id = null
    form.name = ''
    form.description = ''
  }
  dialogVisible.value = true
}

const submitForm = async () => {
  if (!form.name.trim()) {
    ElMessage.warning('请输入自习室名称')
    return
  }
  saving.value = true
  try {
    if (form.id) {
      await request.put(`/api/seats/rooms/${form.id}`, { name: form.name, description: form.description })
    } else {
      await request.post('/api/seats/rooms', { name: form.name, description: form.description })
    }
    ElMessage.success('保存成功')
    dialogVisible.value = false
    fetchRooms()
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

const openBatchDialog = (row: any) => {
  currentRoom.value = row
  batchDialogVisible.value = true
  batchForm.prefix = 'A'
  batchForm.count = 30
  batchForm.has_power = true
}

const submitBatch = async () => {
  if (!currentRoom.value) {
    ElMessage.warning('请先选择一个自习室')
    return
  }
  batchSaving.value = true
  try {
    await request.post(`/api/seats/rooms/${currentRoom.value.id}/seats/batch`, null, { params: batchForm })
    ElMessage.success('座位生成成功')
    batchDialogVisible.value = false
    fetchRooms()
    viewSeats(currentRoom.value)
  } catch (error) {
    ElMessage.error('座位生成失败')
  } finally {
    batchSaving.value = false
  }
}

const removeRoom = async (row: any) => {
  await ElMessageBox.confirm(`确认删除自习室「${row.name}」吗？`, '提示', { type: 'warning' })
  await request.delete(`/api/seats/rooms/${row.id}`)
  ElMessage.success('删除成功')
  fetchRooms()
}

const viewSeats = async (row: any) => {
  currentRoom.value = row
  try {
    seatList.value = await request.get(`/api/seats/rooms/${row.id}/seats`)
    seatDrawerVisible.value = true
  } catch (error) {
    ElMessage.error('获取座位概况失败')
  }
}

onMounted(fetchRooms)
</script>

<style scoped>
.room-page { display: flex; flex-direction: column; gap: 20px; }
.hero-card { border: none; border-radius: 28px; padding: 24px; background: linear-gradient(135deg, #2563eb, #7c3aed); color: #fff; }
.hero-main { display: flex; justify-content: space-between; gap: 20px; align-items: center; }
.hero-badge { display: inline-flex; padding: 6px 12px; border-radius: 999px; background: rgba(255,255,255,.16); margin-bottom: 12px; }
.hero-title { margin: 0; font-size: 28px; font-weight: 900; }
.hero-desc { margin: 10px 0 0; opacity: .92; }
.hero-actions { display: flex; gap: 10px; flex-wrap: wrap; }
.section-card { border: none; border-radius: 24px; }
.section-header { display: flex; justify-content: space-between; align-items: center; gap: 16px; }
.section-title { font-size: 18px; font-weight: 800; color: #0f172a; }
.section-subtitle { margin-top: 4px; color: #64748b; font-size: 12px; }
.row-actions { display: flex; gap: 10px; flex-wrap: wrap; }
.bottom-grid { display: grid; grid-template-columns: 0.9fr 1.1fr; gap: 20px; }
.form-grid { display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 14px; }
.footer-actions { display: flex; justify-content: flex-end; margin-top: 14px; }
@media (max-width: 1100px) { .bottom-grid, .form-grid { grid-template-columns: 1fr; } .hero-main { flex-direction: column; align-items: flex-start; } }
</style>
