<template>
  <div class="student-layout">
    <el-header class="student-header">
      <div class="student-brand" @click="goHome">
        <div class="brand-mark">SR</div>
        <div>
          <div class="brand-name">自习室门户</div>
          <div class="brand-sub">预约、公告、个人中心一站式服务</div>
        </div>
      </div>

      <div class="desktop-nav">
        <el-menu mode="horizontal" :default-active="activeMenu" class="portal-menu" router>
          <el-menu-item index="/portal/home">首页</el-menu-item>
          <el-menu-item index="/portal/booking">自习室预约</el-menu-item>
          <el-menu-item index="/portal/notices">公告通知</el-menu-item>
          <el-menu-item index="/portal/my-reservations">我的预约</el-menu-item>
          <el-menu-item index="/portal/feedback">意见反馈</el-menu-item>
          <el-menu-item index="/portal/user">个人中心</el-menu-item>
        </el-menu>
      </div>

      <div class="header-actions">
        <el-dropdown>
          <span class="user-pill">{{ user?.real_name || user?.username || '学生' }}</span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="goPage('/portal/my-reservations')">我的预约</el-dropdown-item>
              <el-dropdown-item @click="goPage('/portal/user')">个人中心</el-dropdown-item>
              <el-dropdown-item divided @click="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <el-button class="mobile-toggle" text @click="drawerVisible = true">菜单</el-button>
      </div>
    </el-header>

    <el-drawer v-model="drawerVisible" title="导航菜单" direction="rtl" size="260px">
      <el-menu :default-active="activeMenu" router class="mobile-menu">
        <el-menu-item index="/portal/home">首页</el-menu-item>
        <el-menu-item index="/portal/booking">自习室预约</el-menu-item>
        <el-menu-item index="/portal/notices">公告通知</el-menu-item>
        <el-menu-item index="/portal/my-reservations">我的预约</el-menu-item>
        <el-menu-item index="/portal/feedback">意见反馈</el-menu-item>
        <el-menu-item index="/portal/user">个人中心</el-menu-item>
      </el-menu>
    </el-drawer>

    <main class="student-main">
      <router-view v-slot="{ Component }">
        <transition name="page-fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <footer class="student-footer">
      <div>Python 自习室预约系统 · 学生门户</div>
      <div>便捷预约 · 公告通知 · 反馈留言</div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const user = ref(JSON.parse(localStorage.getItem('user') || '{}'))
const drawerVisible = ref(false)
const activeMenu = computed(() => route.path)

const goHome = () => router.push('/portal/home')
const goPage = (path: string) => {
  drawerVisible.value = false
  router.push(path)
}
const logout = () => {
  localStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
.student-layout {
  min-height: 100vh;
  background: linear-gradient(180deg, #f8fbff 0%, #eef4ff 100%);
}

.student-header {
  position: sticky;
  top: 0;
  z-index: 20;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  height: 78px;
  padding: 0 28px;
  background: rgba(255,255,255,0.78);
  backdrop-filter: blur(18px);
  border-bottom: 1px solid rgba(148, 163, 184, 0.14);
}

.student-brand {
  display: flex;
  align-items: center;
  gap: 14px;
  cursor: pointer;
}

.brand-mark {
  width: 44px;
  height: 44px;
  border-radius: 15px;
  display: grid;
  place-items: center;
  color: #fff;
  font-weight: 800;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  box-shadow: 0 12px 24px rgba(37, 99, 235, 0.22);
}

.brand-name {
  font-size: 18px;
  font-weight: 800;
  color: #0f172a;
}

.brand-sub {
  font-size: 12px;
  color: #64748b;
}

.portal-menu {
  border-bottom: none;
  background: transparent;
}

.portal-menu :deep(.el-menu-item) {
  height: 50px;
  line-height: 50px;
  border-radius: 999px;
  margin: 0 6px;
  padding: 0 18px;
  font-weight: 600;
  transition: all 0.22s ease;
}

.portal-menu :deep(.el-menu-item:hover) {
  transform: translateY(-2px);
  background: rgba(37, 99, 235, 0.08);
}

.portal-menu :deep(.el-menu-item.is-active) {
  color: #fff;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  box-shadow: 0 12px 24px rgba(37, 99, 235, 0.22);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-pill {
  display: inline-flex;
  align-items: center;
  padding: 10px 14px;
  border-radius: 999px;
  background: linear-gradient(135deg, rgba(37,99,235,0.12), rgba(124,58,237,0.10));
  color: #1d4ed8;
  font-weight: 700;
  cursor: pointer;
}

.mobile-toggle {
  display: none;
}

.student-main {
  max-width: 1280px;
  margin: 0 auto;
  padding: 28px 20px 44px;
}

.student-footer {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 18px 24px 28px;
  color: #64748b;
  font-size: 12px;
  max-width: 1280px;
  margin: 0 auto;
}

@media (max-width: 960px) {
  .desktop-nav {
    display: none;
  }

  .mobile-toggle {
    display: inline-flex;
  }

  .student-header {
    padding: 0 16px;
  }

  .student-main {
    padding: 20px 14px 32px;
  }

  .student-footer {
    flex-direction: column;
    text-align: center;
  }
}
</style>
