import { createRouter, createWebHistory } from 'vue-router'
import Prizes from '../views/Prizes.vue'
import Laureates from '../views/Laureates.vue'

const routes = [
  { path: '/', redirect: '/prizes' },
  { path: '/prizes', component: Prizes },
  { path: '/laureates', component: Laureates }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
