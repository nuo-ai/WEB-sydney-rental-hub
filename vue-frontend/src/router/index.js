import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/property/:id',
      name: 'propertyDetail',
      component: () => import('../views/PropertyDetail.vue'),
    },
    {
      path: '/favorites',
      name: 'favorites',
      component: () => import('../views/Favorites.vue'),
    },
    {
      path: '/map',
      name: 'map',
      component: () => import('../views/Map.vue'),
    },
    {
      path: '/chat',
      name: 'chat',
      component: () => import('../views/Chat.vue'),
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/Profile.vue'),
    },
  ],
})

export default router
