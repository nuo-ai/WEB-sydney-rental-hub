<template>
  <!-- 移动端底部导航 -->
  <nav v-if="isMobile" class="bottom-nav">
    <div class="nav-container">
      <router-link
        v-for="item in navItems"
        :key="item.name"
        :to="item.path"
        class="nav-item"
        :class="{ 'active': isActive(item.path) }"
      >
        <i :class="item.icon"></i>
        <span class="chinese-text">{{ item.label }}</span>
      </router-link>
    </div>
  </nav>

  <!-- 桌面端顶部导航 -->
  <nav v-else class="top-nav" :class="{ 'nav-hidden': isNavHidden }">
    <div class="top-nav-content">
      <!-- 左侧 Logo 和主导航 -->
      <div class="nav-left">
        <router-link to="/" class="logo">
          <div class="logo-icon">
            <i class="fa-solid fa-home"></i>
          </div>
          <span class="chinese-text">JUWO 桔屋找房</span>
        </router-link>

        <div class="main-nav">
          <router-link
            v-for="item in mainNavItems"
            :key="item.name"
            :to="item.path"
            class="main-nav-item"
            :class="{ 'active': isActive(item.path) }"
          >
            <i :class="item.icon"></i>
            <span class="chinese-text">{{ item.label }}</span>
          </router-link>
        </div>
      </div>

      <!-- 右侧用户导航 -->
      <div class="nav-right">
        <router-link
          v-for="item in userNavItems"
          :key="item.name"
          :to="item.path"
          class="user-nav-item"
          :class="{ 'active': isActive(item.path) }"
        >
          <i :class="item.icon"></i>
          <span class="chinese-text">{{ item.label }}</span>
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
defineOptions({ name: 'MainNavigation' })
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute } from 'vue-router'

// 定义导航栏显示状态的props
const props = defineProps({
  isHidden: {
    type: Boolean,
    default: false
  }
})

// 路由
const route = useRoute()

// 导航项配置
const navItems = [
  {
    name: 'home',
    path: '/',
    icon: 'fa-solid fa-magnifying-glass',
    label: '搜索'
  },
  {
    name: 'favorites',
    path: '/favorites',
    icon: 'fa-regular fa-heart',
    label: '收藏'
  },
  {
    name: 'chat',
    path: '/chat',
    icon: 'fa-solid fa-comments',
    label: 'AI助手'
  },
  {
    name: 'map',
    path: '/map',
    icon: 'fa-regular fa-map',
    label: '地图'
  },
  {
    name: 'profile',
    path: '/profile',
    icon: 'fa-regular fa-user',
    label: '我的'
  }
]

const mainNavItems = [
  {
    name: 'home',
    path: '/',
    icon: 'fa-solid fa-magnifying-glass',
    label: '搜索'
  },
  {
    name: 'favorites',
    path: '/favorites',
    icon: 'fa-regular fa-heart',
    label: '收藏'
  },
  {
    name: 'map',
    path: '/map',
    icon: 'fa-regular fa-map',
    label: '地图'
  }
]

const userNavItems = [
  {
    name: 'chat',
    path: '/chat',
    icon: 'fa-solid fa-comments',
    label: 'AI助手'
  },
  {
    name: 'profile',
    path: '/profile',
    icon: 'fa-regular fa-user',
    label: '我的'
  }
]

// 计算属性
const windowWidth = ref(window.innerWidth)

const isMobile = computed(() => {
  return windowWidth.value <= 768
})

const isNavHidden = computed(() => {
  return props.isHidden
})

const isActive = (path) => {
  return route.path === path
}

const handleResize = () => {
  windowWidth.value = window.innerWidth
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
/* 移动端底部导航 */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  border-top: 1px solid var(--color-border-default);
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.06);
  z-index: 100;
  height: 70px;
}

.nav-container {
  display: flex;
  justify-content: space-around;
  align-items: center;
  height: 100%;
  padding: 0 8px;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 8px 6px;
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: all 0.2s ease;
  border-radius: 8px;
  min-width: 60px;
}

.nav-item:hover,
.nav-item.active {
  color: var(--juwo-primary);
  background: var(--juwo-primary-50);
}

.nav-item i {
  font-size: 20px;
}

.nav-item span {
  font-size: 12px;
  font-weight: 500;
}

/* 桌面端顶部导航 */
.top-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: white;
  border-bottom: 1px solid var(--color-border-default);
  height: 64px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  z-index: 60;
  transform: translateY(0);
  transition: transform 0.25s ease-in-out;
  /* 硬件加速优化 - 避免transform冲突 */
  will-change: transform;
  backface-visibility: hidden;
}

.top-nav.nav-hidden {
  transform: translateY(-100%);
}

.top-nav-content {
  max-width: 1200px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
}

/* 左侧导航 */
.nav-left {
  display: flex;
  align-items: center;
  gap: 32px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text-primary);
  text-decoration: none;
  transition: all 0.2s ease;
}

.logo:hover {
  color: var(--juwo-primary);
}

.logo-icon {
  width: 32px;
  height: 32px;
  background: var(--juwo-primary);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 16px;
  transition: all 0.2s ease;
}

.logo:hover .logo-icon {
  background: var(--juwo-primary-light);
  transform: scale(1.05);
}

.main-nav {
  display: flex;
  align-items: center;
  gap: 24px;
}

.main-nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  color: var(--color-text-secondary);
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.2s ease;
  font-weight: 500;
}

.main-nav-item:hover,
.main-nav-item.active {
  color: var(--juwo-primary);
  background: var(--juwo-primary-50);
}

.main-nav-item i {
  font-size: 16px;
}

/* 右侧导航 */
.nav-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  color: var(--color-text-secondary);
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.2s ease;
  font-weight: 500;
}

.user-nav-item:hover,
.user-nav-item.active {
  color: var(--juwo-primary);
  background: var(--juwo-primary-50);
}

.user-nav-item i {
  font-size: 16px;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .top-nav {
    display: none;
  }
}

@media (min-width: 769px) {
  .bottom-nav {
    display: none;
  }
}

@media (max-width: 1023px) {
  .top-nav-content {
    padding: 0 20px;
  }

  .nav-left {
    gap: 20px;
  }

  .main-nav {
    gap: 16px;
  }

  .nav-right {
    gap: 12px;
  }
}
</style>
