<template>
  <!-- 移动端底部导航 -->
  <nav v-if="isMobile && !disableBottomNav" class="bottom-nav">
    <div class="nav-container">
      <router-link
        v-for="item in navItems"
        :key="item.name"
        :to="item.path"
        class="nav-item"
        :class="{ active: isActive(item.path) }"
      >
        <component :is="item.iconComp" class="nav-icon" aria-hidden="true" />
        <span class="chinese-text">{{ item.label }}</span>
      </router-link>
    </div>
  </nav>

  <!-- 桌面端顶部导航 -->
  <nav v-else class="top-nav" :class="{ 'nav-hidden': isNavHidden }">
    <div class="top-nav-content">
      <!-- 左侧 Logo 和主导航 -->
      <div class="nav-left">
        <router-link to="/" class="logo juwo">
          <span class="brand-text">Juwo</span>
        </router-link>

        <div class="main-nav">
          <router-link
            v-for="item in mainNavItems"
            :key="item.name"
            :to="item.path"
            class="main-nav-item"
            :class="{ active: isActive(item.path) }"
          >
            <component :is="item.iconComp" class="nav-icon" aria-hidden="true" />
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
          :class="{ active: isActive(item.path) }"
        >
          <component :is="item.iconComp" class="nav-icon" aria-hidden="true" />
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
import { Search, Heart, MessageSquare, Map, User } from 'lucide-vue-next'

// 定义导航栏显示状态的props
const props = defineProps({
  isHidden: {
    type: Boolean,
    default: false,
  },
  // 中文注释：网站默认关闭底部导航；如需启用（如小程序场景），传入 :disableBottomNav="false"
  disableBottomNav: {
    type: Boolean,
    default: true,
  },
})

// 路由
const route = useRoute()

// 导航项配置
const navItems = [
  {
    name: 'home',
    path: '/',
    icon: 'fa-solid fa-magnifying-glass',
    iconComp: Search,
    label: '搜索',
  },
  {
    name: 'favorites',
    path: '/favorites',
    icon: 'fa-regular fa-heart',
    iconComp: Heart,
    label: '收藏',
  },
  {
    name: 'chat',
    path: '/chat',
    icon: 'fa-solid fa-comments',
    iconComp: MessageSquare,
    label: 'AI助手',
  },
  {
    name: 'map',
    path: '/map',
    icon: 'fa-regular fa-map',
    iconComp: Map,
    label: '地图',
  },
  {
    name: 'profile',
    path: '/profile',
    icon: 'fa-regular fa-user',
    iconComp: User,
    label: '我的',
  },
]

const mainNavItems = [
  {
    name: 'home',
    path: '/',
    icon: 'fa-solid fa-magnifying-glass',
    iconComp: Search,
    label: '搜索',
  },
  {
    name: 'favorites',
    path: '/favorites',
    icon: 'fa-regular fa-heart',
    iconComp: Heart,
    label: '收藏',
  },
  {
    name: 'map',
    path: '/map',
    icon: 'fa-regular fa-map',
    iconComp: Map,
    label: '地图',
  },
]

const userNavItems = [
  {
    name: 'chat',
    path: '/chat',
    icon: 'fa-solid fa-comments',
    iconComp: MessageSquare,
    label: 'AI助手',
  },
  {
    name: 'profile',
    path: '/profile',
    icon: 'fa-regular fa-user',
    iconComp: User,
    label: '我的',
  },
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
  /* 中文注释：移动端底部导航变量化，读取 page tokens，确保高度=56px+安全区 */
  --nav-height: calc(var(--nav-h-mob, 56px) + var(--nav-safe-area-bottom, 0px));
  --nav-padding-x: var(--nav-px-mob, 16px);
  --nav-icon-size: var(--nav-icon, 16px);
  --nav-item-gap: 4px;

  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  border-top: 1px solid var(--color-border-default);
  box-shadow: var(--nav-shadow, none);
  z-index: 100;
  height: var(--nav-height);
  padding-bottom: var(--nav-safe-area-bottom, 0px);
}

.nav-container {
  display: flex;
  justify-content: space-around;
  align-items: center;
  height: 100%;
  padding: 0 var(--nav-padding-x);
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--nav-item-gap, 4px);
  padding: 8px 6px;
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: all 0.2s ease;
  border-radius: 2px;
  min-width: 60px;
}

.nav-item:hover,
.nav-item.active {
  color: var(--color-text-primary);
  background: var(--bg-hover);
}

.nav-item .nav-icon {
  width: var(--nav-icon-size);
  height: var(--nav-icon-size);
}

.nav-item span {
  font-size: 12px;
  font-weight: 500;
}

/* 桌面端顶部导航 */
.top-nav {
  /* 中文注释：桌面端顶部导航变量化，读取 page tokens */
  --nav-height: var(--nav-h-desk, 64px);
  --nav-padding-x: var(--nav-px-desk, 32px);
  --nav-gap: var(--nav-gap, 24px);
  --nav-icon-size: var(--nav-icon, 16px);

  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: white;
  border-bottom: 1px solid var(--color-border-default);
  height: var(--nav-height);
  box-shadow: var(--nav-shadow, none);
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
  padding: 0 var(--nav-padding-x);
}

/* 左侧导航 */
.nav-left {
  display: flex;
  align-items: center;
  gap: var(--nav-gap);
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



.brand-text {
  color: var(--color-text-primary); /* PC 顶部 JUWO 文本：黑色 */
  font-weight: 700;                 /* 加粗 */
}

.main-nav {
  display: flex;
  align-items: center;
  gap: var(--nav-gap);
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
  position: relative; /* 中文注释：为活动态下划线提供定位锚点 */
}

.main-nav-item:hover,
.main-nav-item.active {
  color: var(--color-text-primary);
  background: var(--bg-hover);
}

/* 当前路由活动态：2px 下划线（前端表现：清晰的当前页指示） */
.main-nav-item.active::after {
  content: '';
  position: absolute;
  left: 12px;  /* 与左右内边距 16 结合，视觉收口 */
  right: 12px;
  bottom: 6px;
  height: var(--nav-active-underline, 2px);
  background: var(--juwo-primary);
  border-radius: 1px;
}

.main-nav-item .nav-icon {
  width: var(--nav-icon-size);
  height: var(--nav-icon-size);
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
  border-radius: 2px;
  transition: all 0.2s ease;
  font-weight: 500;
}

.user-nav-item:hover,
.user-nav-item.active {
  color: var(--color-text-primary);
  background: var(--bg-hover);
}

.user-nav-item .nav-icon {
  width: var(--nav-icon-size);
  height: var(--nav-icon-size);
}

/* 响应式适配 */
@media (width <= 768px) {
  .top-nav {
    display: none;
  }
}

@media (width >= 769px) {
  .bottom-nav {
    display: none;
  }
}

/* 导航点击后不显示外框（去除浅灰外框），悬停可用品牌橙，点击无 outline */
.main-nav-item:focus,
.main-nav-item:focus-visible,
.nav-item:focus,
.nav-item:focus-visible,
.user-nav-item:focus,
.user-nav-item:focus-visible,
.logo:focus,
.logo:focus-visible {
  outline: none !important;
  box-shadow: none !important;
}

@media (width <= 1023px) {
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
