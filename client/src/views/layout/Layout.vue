<template>
  <el-container class="min-h-screen">
    <!-- 侧边栏 -->
    <el-aside width="250px" class="bg-gray-800 text-white shadow-xl transition-all duration-300">
      <div class="h-16 flex items-center justify-center text-xl font-bold border-b border-gray-700 tracking-wider">
        自习室管理系统
      </div>
      <el-menu
        :default-active="activeMenu"
        active-text-color="#409eff"
        background-color="transparent"
        class="border-none"
        text-color="#fff"
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
        <el-menu-item index="/user" v-if="user?.role === 'admin'">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主内容区 -->
    <el-container>
      <el-header class="bg-white shadow-sm flex items-center justify-between px-6 z-10">
        <div class="text-gray-600 font-medium">欢迎回来，{{ user?.real_name || user?.username || '管理员' }}</div>
        <el-button type="danger" plain @click="logout" size="small">退出登录</el-button>
      </el-header>

      <el-main class="bg-gray-50 p-6">
        <!-- 路由出口 -->
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
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
import { DataLine, Coordinate, User, Document } from '@element-plus/icons-vue'

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
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
