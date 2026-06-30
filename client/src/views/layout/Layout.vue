<template>
  <el-container class="admin-shell min-h-screen">
    <el-aside class="admin-side" :width="isCollapsed ? '88px' : '260px'">
      <div class="brand-box">
        <div :class="isCollapsed ? 'brand-mini' : 'brand-icon'">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" style="width: 24px; height: 24px;">
            <path d="M11.25 4.533A9.707 9.707 0 0 0 6 3a9.735 9.735 0 0 0-3.25.555.75.75 0 0 0-.5.707v14.25a.75.75 0 0 0 1 .707A8.237 8.237 0 0 1 6 18.75c1.995 0 3.823.707 5.25 1.886V4.533ZM12.75 20.636A8.214 8.214 0 0 1 18 18.75c.966 0 1.89.166 2.75.47a.75.75 0 0 0 1-.708V4.262a.75.75 0 0 0-.5-.707A9.735 9.735 0 0 0 18 3a9.707 9.707 0 0 0-5.25 1.533v16.103Z" />
          </svg>
        </div>
        <div class="brand-copy" v-if="!isCollapsed">
          <div class="brand-title">自习室管理系统</div>
          <div class="brand-subtitle">后台运营中心</div>
        </div>
      </div>

      <el-menu
        :default-active="activeMenu"
        active-text-color="#2563eb"
        background-color="transparent"
        class="side-menu"
        text-color="#1f2937"
        router
      >
        <el-menu-item index="/admin/home">
          <el-icon><DataLine /></el-icon>
          <span v-if="!isCollapsed">数据看板</span>
        </el-menu-item>
        <el-menu-item index="/admin/booking">
          <el-icon><Coordinate /></el-icon>
          <span v-if="!isCollapsed">座位预约</span>
        </el-menu-item>
        <el-menu-item index="/admin/rooms">
          <el-icon><OfficeBuilding /></el-icon>
          <span v-if="!isCollapsed">自习室管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/user">
          <el-icon><User /></el-icon>
          <span v-if="!isCollapsed">用户管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/notices">
          <el-icon><Bell /></el-icon>
          <span v-if="!isCollapsed">公告管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/feedback">
          <el-icon><ChatDotRound /></el-icon>
          <span v-if="!isCollapsed">反馈处理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="top-bar">
        <div class="top-left">
          <el-button class="collapse-btn" text @click="isCollapsed = !isCollapsed">
            <el-icon><Fold v-if="!isCollapsed" /><Expand v-else /></el-icon>
          </el-button>
          <div class="top-copy">
            <div class="top-title">欢迎回来，{{ user?.real_name || user?.username || '管理员' }}</div>
            <div class="top-subtitle">今天也要保持高效管理</div>
          </div>
        </div>
        <div class="top-actions">
          <div class="status-pill"><span class="status-dot"></span>系统运行正常</div>
          <el-button type="primary" plain @click="logout">退出登录</el-button>
        </div>
      </el-header>

      <el-main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="page-fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { DataLine, Coordinate, User, OfficeBuilding, Bell, ChatDotRound, Fold, Expand } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const user = ref(JSON.parse(localStorage.getItem('user') || '{}'))
const activeMenu = computed(() => route.path)
const isCollapsed = ref(false)

const updateResponsive = () => {
  isCollapsed.value = window.innerWidth < 1100
}

onMounted(() => {
  updateResponsive()
  window.addEventListener('resize', updateResponsive)
})

onBeforeUnmount(() => window.removeEventListener('resize', updateResponsive))

const logout = () => {
  localStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
.admin-shell { background: transparent; }
.admin-side {
  position: relative; z-index: 1; padding: 18px 14px;
  background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(241,245,249,0.98));
  border-right: 1px solid rgba(148, 163, 184, 0.18); box-shadow: 12px 0 30px rgba(15, 23, 42, 0.04);
}
.brand-box { display:flex; align-items:center; gap:14px; padding:18px 16px; border-radius:18px; background:linear-gradient(135deg,#eff6ff,#eef2ff); margin-bottom:24px; }
.brand-copy { display:flex; flex-direction:column; gap:4px; }
.brand-title { font-weight:900; color:#0f172a; font-size:18px; letter-spacing:-0.5px; }
.brand-subtitle { font-size:13px; color:#64748b; font-weight:500; }
.brand-icon, .brand-mini { width:48px; height:48px; border-radius:16px; display:grid; place-items:center; background:linear-gradient(135deg,#2563eb,#7c3aed); color:#fff; box-shadow:0 12px 24px rgba(37,99,235,.22); flex-shrink:0; }
.side-menu { border:none; }
.side-menu :deep(.el-menu-item) { margin:6px 0; border-radius:14px; transition:all .22s ease; }
.side-menu :deep(.el-menu-item:hover){ transform:translateX(8px); background:rgba(37,99,235,.08); }
.side-menu :deep(.el-menu-item.is-active){ color:#fff; background:linear-gradient(90deg,#2563eb,#7c3aed); box-shadow:0 10px 24px rgba(37,99,235,.10); }
.top-bar { position:relative; z-index:1; height:76px; display:flex; align-items:center; justify-content:space-between; padding:0 28px; background:rgba(255,255,255,.78); backdrop-filter:blur(12px); border-bottom:1px solid rgba(148,163,184,.16); }
.top-left{display:flex;align-items:center;gap:12px}
.collapse-btn{border-radius:12px}
.top-copy::after{content:'';display:block;width:120px;height:3px;margin-top:10px;border-radius:999px;background:linear-gradient(90deg,#2563eb,#7c3aed)}
.top-title { font-size:18px; font-weight:800; color:#0f172a; }
.top-subtitle { margin-top:4px; font-size:12px; color:#64748b; }
.top-actions { display:flex; align-items:center; gap:12px; }
.status-pill { display:inline-flex; align-items:center; gap:8px; padding:8px 12px; border-radius:999px; background:rgba(16,185,129,.10); color:#059669; font-size:12px; font-weight:600; }
.status-dot { width:8px; height:8px; border-radius:999px; background:#10b981; box-shadow:0 0 0 6px rgba(16,185,129,.15); animation:pulseDot 1.6s ease-in-out infinite; }
.main-content { position:relative; z-index:1; padding:24px; }
@keyframes pulseDot { 0%,100%{transform:scale(1)} 50%{transform:scale(1.12)} }
@media (max-width: 1100px){ .top-bar{padding:0 16px}.main-content{padding:16px}.top-subtitle{display:none} }
</style>
