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
