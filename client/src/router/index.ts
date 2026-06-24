import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/',
    name: 'Layout',
    component: () => import('../views/layout/Layout.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../views/dashboard/Dashboard.vue')
      },
      {
        path: 'booking',
        name: 'Booking',
        component: () => import('../views/booking/Booking.vue')
      },
      {
        path: 'my-reservations',
        name: 'MyReservations',
        component: () => import('../views/booking/MyReservations.vue')
      },
      {
        path: 'user',
        name: 'User',
        component: () => import('../views/user/User.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router