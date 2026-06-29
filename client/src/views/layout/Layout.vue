<template>
  <el-container class="admin-shell min-h-screen">
    <el-aside class="admin-side" :width="isCollapsed ? '88px' : '260px'">
      <div class="brand-box">
        <div class="brand-copy" v-if="!isCollapsed">
          <div class="brand-kicker">Admin Control</div>
          <div class="brand-title">自习室管理系统</div>
          <div class="brand-subtitle">后台运营中心</div>
        </div>
        <div class="brand-wave" v-if="!isCollapsed">
          <span></span><span></span><span></span>
        </div>
        <div v-else class="brand-mini">SR</div>
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
.brand-box { display:flex; justify-content:space-between; align-items:flex-start; gap:12px; padding:16px; border-radius:18px; background:linear-gradient(135deg,#eff6ff,#eef2ff); margin-bottom:18px; }
.brand-kicker { display:inline-flex; padding:4px 10px; border-radius:999px; background:rgba(37,99,235,.12); color:#2563eb; font-size:12px; font-weight:700; margin-bottom:10px; }
.brand-title { font-weight:900; color:#1e293b; font-size:18px; }
.brand-subtitle { font-size:12px; color:#64748b; }
.brand-mini { width:44px; height:44px; border-radius:14px; display:grid; place-items:center; background:linear-gradient(135deg,#2563eb,#7c3aed); color:#fff; font-weight:900; }
.brand-wave { display:flex; gap:4px; align-items:flex-end; height:28px; padding-top:4px; }
.brand-wave span { width:4px; border-radius:999px; background:linear-gradient(180deg,#60a5fa,#8b5cf6); animation: wave 1.2s ease-in-out infinite; }
.brand-wave span:nth-child(1){height:10px}.brand-wave span:nth-child(2){height:18px;animation-delay:.15s}.brand-wave span:nth-child(3){height:14px;animation-delay:.3s}
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
@keyframes wave { 0%,100%{transform:scaleY(.75);opacity:.6} 50%{transform:scaleY(1.3);opacity:1} }
@keyframes pulseDot { 0%,100%{transform:scale(1)} 50%{transform:scale(1.12)} }
@media (max-width: 1100px){ .top-bar{padding:0 16px}.main-content{padding:16px}.top-subtitle{display:none} }
</style>
