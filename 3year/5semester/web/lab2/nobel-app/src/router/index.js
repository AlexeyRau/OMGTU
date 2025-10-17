import Prizes from '@/views/Prizes.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/', 
      redirect: '/prizes'
    },
    {
      path: '/prizes', 
      name: 'prizes', 
      component: () => import('@/views/Prizes.vue')
    },
    {
      path: '/laureates', 
      name: 'laureats', 
      component: () => import('@/views/Laureates.vue')
    }
  ]
})

export default router
