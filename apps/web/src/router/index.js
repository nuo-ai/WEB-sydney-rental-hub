import { createRouter, createWebHistory } from 'vue-router'
// import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
    },
    {
      path: '/details/:id',
      name: 'PropertyDetail',
      component: () => import('../views/PropertyDetail.vue'),
      props: true,
    },
    {
      path: '/details-new/:id',
      name: 'PropertyDetailNew',
      component: () => import('../views/PropertyDetailNew.vue'),
      props: true,
    },
    {
      path: '/property-detail-v3/:id',
      name: 'PropertyDetailV3',
      component: () => import('../views/PropertyDetailV3.vue'),
      props: true,
      meta: { layout: 'shadcn' },
    },
    {
      path: '/favorites',
      name: 'favorites',
      component: () => import('../views/Favorites.vue'),
    },
    {
      path: '/chat',
      name: 'chat',
      component: () => import('../views/ChatView.vue'),
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/Profile.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/compare',
      name: 'compare',
      component: () => import('../views/CompareView.vue'),
    },
    {
      path: '/commute',
      name: 'CommuteTimes',
      component: () => import('../views/CommuteTimes.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/globals-demo',
      name: 'GlobalsDemo',
      component: () => import('../views/GlobalsDemo.vue'),
    },
    {
      path: '/cards-demo',
      name: 'CardsDemo',
      component: () => import('../views/CardsDemo.vue'),
    },
  ],
})

/*
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const publicPages = ['/login']
  const authRequired = !publicPages.includes(to.path)

  if (authRequired && !authStore.isAuthenticated) {
    return next('/login')
  }

  next()
})
*/

export default router
