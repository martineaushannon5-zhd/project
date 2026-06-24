<template>
  <el-container class="layout-shell min-h-screen">
    <el-aside class="side-panel" width="260px">
      <div class="brand-box">
        <div class="brand-copy">
          <div class="brand-kicker">Study Room Admin</div>
          <div class="brand-title">自习室管理系统</div>
          <div class="brand-subtitle">后台运营中心</div>
        </div>
        <div class="brand-wave">
          <span></span>
          <span></span>
          <span></span>
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
        <el-menu-item index="/dashboard">
          <el-icon><DataLine /></el-icon>
          <span>数据看板</span>
        </el-menu-item>
        <el-menu-item index="/booking">
          <el-icon><Coordinate /></el-icon>
          <span>座位预约</span>
        </el-menu-item>
        <el-menu-item index="/my-reservations" v-if="user?.role === 'student'">
          <el-icon><Document /></el-icon>
          <span>我的预约</span>
        </el-menu-item>
        <el-menu-item index="/rooms" v-if="user?.role === 'admin'">
          <el-icon><OfficeBuilding /></el-icon>
          <span>自习室管理</span>
        </el-menu-item>
        <el-menu-item index="/user" v-if="user?.role === 'admin'">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="top-bar">
        <div class="top-copy">
          <div class="top-title">欢迎回来，{{ user?.real_name || user?.username || '管理员' }}</div>
          <div class="top-subtitle">今天也要保持高效管理</div>
        </div>
        <div class="top-actions">
          <div class="status-pill">
            <span class="status-dot"></span>
            系统运行正常
          </div>
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
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { DataLine, Coordinate, User, Document, OfficeBuilding } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const user = ref(JSON.parse(localStorage.getItem('user') || '{}'))

const activeMenu = computed(() => route.path)

const logout = () => {
  localStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
.layout-shell {
  position: relative;
  overflow: hidden;
  background: transparent;
}

.layout-shell::before,
.layout-shell::after {
  content: '';
  position: fixed;
  border-radius: 999px;
  pointer-events: none;
  filter: blur(10px);
  opacity: 0.55;
  z-index: 0;
}

.layout-shell::before {
  width: 180px;
  height: 180px;
  left: -60px;
  top: 120px;
  background: radial-gradient(circle, rgba(59,130,246,0.22), rgba(59,130,246,0));
  animation: floatBlob 9s ease-in-out infinite;
}

.layout-shell::after {
  width: 220px;
  height: 220px;
  right: -70px;
  top: 280px;
  background: radial-gradient(circle, rgba(124,58,237,0.16), rgba(124,58,237,0));
  animation: floatBlob 12s ease-in-out infinite reverse;
}

.side-panel {
  position: relative;
  z-index: 1;
  padding: 18px 14px;
  background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(241,245,249,0.98));
  border-right: 1px solid rgba(148, 163, 184, 0.18);
  box-shadow: 12px 0 30px rgba(15, 23, 42, 0.04);
}

.brand-box {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  border-radius: 18px;
  background: linear-gradient(135deg, #eff6ff, #eef2ff);
  margin-bottom: 18px;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.7);
}

.brand-copy {
  min-width: 0;
}

.brand-kicker {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(37, 99, 235, 0.12);
  color: #2563eb;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.5px;
  margin-bottom: 10px;
}

.brand-title {
  font-weight: 900;
  color: #1e293b;
  font-size: 18px;
  line-height: 1.2;
}

.brand-subtitle {
  font-size: 12px;
  color: #64748b;
  margin-top: 4px;
}

.brand-wave {
  display: flex;
  gap: 4px;
  align-items: flex-end;
  height: 28px;
  padding-top: 4px;
}

.brand-wave span {
  width: 4px;
  border-radius: 999px;
  background: linear-gradient(180deg, #60a5fa, #8b5cf6);
  animation: wave 1.2s ease-in-out infinite;
}

.brand-wave span:nth-child(1) { height: 10px; animation-delay: 0s; }
.brand-wave span:nth-child(2) { height: 18px; animation-delay: 0.15s; }
.brand-wave span:nth-child(3) { height: 14px; animation-delay: 0.3s; }

.side-menu {
  border: none;
}

.side-menu :deep(.el-menu-item) {
  margin: 6px 0;
  border-radius: 14px;
  transition: all 0.22s ease;
}

.side-menu :deep(.el-menu-item:hover) {
  transform: translateX(8px);
  background: rgba(37, 99, 235, 0.08);
}

.side-menu :deep(.el-menu-item.is-active) {
  background: linear-gradient(90deg, rgba(37,99,235,0.14), rgba(124,58,237,0.08));
  box-shadow: 0 10px 24px rgba(37, 99, 235, 0.10);
}

.top-bar {
  position: relative;
  z-index: 1;
  height: 76px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 28px;
  background: rgba(255,255,255,0.78);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(148, 163, 184, 0.16);
}

.top-copy {
  position: relative;
}

.top-copy::after {
  content: '';
  display: block;
  width: 120px;
  height: 3px;
  margin-top: 10px;
  border-radius: 999px;
  background: linear-gradient(90deg, #2563eb, #7c3aed);
}

.top-title {
  font-size: 18px;
  font-weight: 800;
  color: #0f172a;
}

.top-subtitle {
  margin-top: 4px;
  font-size: 12px;
  color: #64748b;
}

.top-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(16, 185, 129, 0.10);
  color: #059669;
  font-size: 12px;
  font-weight: 600;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: #10b981;
  box-shadow: 0 0 0 6px rgba(16,185,129,0.15);
  animation: pulseDot 1.6s ease-in-out infinite;
}

.main-content {
  position: relative;
  z-index: 1;
  padding: 24px;
}

@keyframes floatBlob {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(18px) scale(1.06); }
}

@keyframes wave {
  0%, 100% { transform: scaleY(0.75); opacity: 0.6; }
  50% { transform: scaleY(1.3); opacity: 1; }
}

@keyframes pulseDot {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.12); }
}
</style>