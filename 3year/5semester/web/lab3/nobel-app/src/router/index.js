import { createRouter, createWebHistory } from 'vue-router'
import PrizesView from '../views/PrizesView.vue'
import LaureatesView from '../views/LaureatesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'prizes',
      component: PrizesView
    },
    {
      path: '/laureates',
      name: 'laureates',
      component: LaureatesView
    },
  ]
})

export default router