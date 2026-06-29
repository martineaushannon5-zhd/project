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
    redirect: '/login'
  },
  {
    path: '/portal',
    component: () => import('../views/layout/StudentLayout.vue'),
    redirect: '/portal/home',
    children: [
      {
        path: 'home',
        name: 'PortalHome',
        component: () => import('../views/portal/Home.vue')
      },
      {
        path: 'booking',
        name: 'PortalBooking',
        component: () => import('../views/booking/Booking.vue')
      },
      {
        path: 'notices',
        name: 'PortalNotices',
        component: () => import('../views/portal/PortalNotices.vue')
      },
      {
        path: 'my-reservations',
        name: 'PortalMyReservations',
        component: () => import('../views/booking/MyReservations.vue')
      },
      {
        path: 'feedback',
        name: 'PortalFeedback',
        component: () => import('../views/user/User.vue')
      },
      {
        path: 'user',
        name: 'PortalUser',
        component: () => import('../views/portal/Profile.vue')
      },
      {
        path: 'author',
        name: 'PortalAuthor',
        component: () => import('../views/portal/Author.vue')
      }
    ]
  },
  {
    path: '/admin',
    component: () => import('../views/layout/Layout.vue'),
    redirect: '/admin/home',
    children: [
      {
        path: 'home',
        name: 'AdminHome',
        component: () => import('../views/dashboard/Dashboard.vue')
      },
      {
        path: 'booking',
        name: 'AdminBooking',
        component: () => import('../views/booking/Booking.vue')
      },
      {
        path: 'my-reservations',
        name: 'AdminMyReservations',
        component: () => import('../views/booking/MyReservations.vue')
      },
      {
        path: 'user',
        name: 'AdminUser',
        component: () => import('../views/user/User.vue')
      },
      {
        path: 'notices',
        name: 'AdminNoticeManagement',
        component: () => import('../views/portal/PortalNotices.vue')
      },
      {
        path: 'feedback',
        name: 'AdminFeedback',
        component: () => import('../views/user/AdminFeedback.vue')
      },
      {
        path: 'rooms',
        name: 'RoomManagement',
        component: () => import('../views/room/RoomManagement.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
