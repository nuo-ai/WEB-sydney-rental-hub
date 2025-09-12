<template>
  <div class="page profile-page">
    <!-- 1. 页面头部: 完全遵循样板和视觉标准 -->
    <header class="page__header header-with-actions">
      <!-- 返回上一页（无历史则回首页） -->
      <button class="icon-btn back-btn" @click="goBack" aria-label="返回上一页">
        <ArrowLeft class="icon" />
      </button>

      <h1 class="typo-h1 page-title">{{ pageTitle }}</h1>

      <!-- 回到首页 -->
      <router-link to="/">
        <BaseButton variant="ghost" aria-label="回到首页">回到首页</BaseButton>
      </router-link>
    </header>

    <!-- 账号操作：退出登录（次要按钮样式） -->
    <section class="page-section account-actions">
      <BaseButton variant="secondary" @click="handleLogout">退出登录</BaseButton>
    </section>

    <!-- 2. 页面内容区 -->
    <main class="page__content">

      <!-- 3. 第一个区块：我的收藏 -->
      <section class="page-section">
        <div class="section-header">
          <h2 class="typo-h2">我的收藏</h2>
          <!-- 只有在有收藏项时才显示“查看全部”按钮 -->
          <router-link to="/favorites" v-if="favoriteProperties.length > 0">
            <BaseButton variant="ghost">查看全部</BaseButton>
          </router-link>
        </div>

        <!-- 动态内容：收藏列表或空状态 -->
        <div v-if="favoriteProperties.length > 0" class="property-grid">
          <!-- 复用 PropertyCard 组件，并只显示最近3条 -->
          <PropertyCard
            v-for="property in recentFavorites"
            :key="property.listing_id"
            :property="property"
          />
        </div>
        <div v-else class="empty-state">
          <p class="typo-body">您还没有收藏任何房源。</p>
        </div>
      </section>

      <!-- 4. 第二个区块：最近浏览 -->
      <section class="page-section">
        <div class="section-header">
          <h2 class="typo-h2">最近浏览</h2>
        </div>

        <!-- 动态内容：历史记录列表或空状态 -->
        <div v-if="historyProperties.length > 0" class="property-grid">
           <!-- 复用 PropertyCard 组件，并只显示最近3条 -->
          <PropertyCard
            v-for="property in recentHistory"
            :key="property.listing_id"
            :property="property"
          />
        </div>
        <div v-else class="empty-state">
          <p class="typo-body">暂无浏览记录。</p>
        </div>
      </section>

      <!-- 5. 第三个区块：我的筛选 (占位) -->
      <section class="page-section">
        <div class="section-header">
          <h2 class="typo-h2">我的筛选</h2>
        </div>
        <div class="placeholder-state">
          <p class="typo-body text-secondary">此功能即将推出，敬请期待。</p>
        </div>
      </section>

    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ArrowLeft } from 'lucide-vue-next'
// 假设你的 store 文件和基础组件路径如下
import { usePropertiesStore } from '@/stores/properties'
import PropertyCard from '@/components/PropertyCard.vue'
import BaseButton from '@/components/base/BaseButton.vue' // 确保路径正确

defineOptions({ name: 'ProfileView' })

const pageTitle = ref('我的中心')

const router = useRouter()
const authStore = useAuthStore()

// 返回上一页（无历史则回首页）
const goBack = () => {
  try {
    if (window.history.length > 1) router.back()
    else router.push('/')
  } catch {
    router.push('/')
  }
}

// 退出登录并回到首页
const handleLogout = () => {
  try {
    authStore.logout()
  } finally {
    router.push('/')
  }
}

// 6. 从 Pinia Store 获取状态
const propertiesStore = usePropertiesStore()
const favoriteProperties = computed(() => propertiesStore.favoriteProperties || [])
const historyProperties = computed(() => propertiesStore.historyProperties || [])

// 7. 实现业务逻辑：只取最近的3条记录
const recentFavorites = computed(() => favoriteProperties.value.slice(0, 3))
const recentHistory = computed(() => historyProperties.value.slice(0, 3))

</script>

<style scoped>
/* 页面级样式，严格使用设计令牌和规范 */
.profile-page {
  /* 页面级容器默认就有左右 padding 和底部的防遮挡 padding,
     这些由 .page 的全局样式或页面令牌提供，这里无需重复添加 */
}

.page-section {
  /* 使用页面级 design token 控制 section 间的垂直间距 */
  margin-bottom: var(--page-section-gap-lg, 32px);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--page-section-gap, 24px);
}

.property-grid {
  display: grid;
  /* 移动端默认单列，桌面端多列 */
  grid-template-columns: 1fr;
  gap: var(--page-section-gap, 24px);
}

/* 桌面端布局 */
@media (min-width: 768px) {
  .property-grid {
    /* 平板和桌面显示多列 */
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (min-width: 1200px) {
  .property-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.empty-state, .placeholder-state {
  padding: var(--space-8) var(--space-4);
  background-color: var(--color-bg-card);
  border: 1px dashed var(--color-border-default);
  border-radius: var(--radius-md);
  text-align: center;
}

.text-secondary {
  color: var(--color-text-secondary);
}

.header-with-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.header-with-actions .page-title {
  flex: 1;
  text-align: center;
  margin: 0;
}

/* 统一图标按钮样式（令牌化） */
.icon-btn {
  background: transparent;
  border: 1px solid var(--color-border-default);
  color: var(--color-text-secondary);
  width: 36px;
  height: 36px;
  border-radius: 18px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  cursor: pointer;
  transition: background-color .2s ease, color .2s ease, transform .1s ease;
}

.icon-btn:hover {
  background: var(--bg-hover);
  color: var(--color-text-primary);
}

.icon-btn:active {
  transform: translateY(1px);
}

.icon-btn .icon {
  width: 18px;
  height: 18px;
}

/* 账号操作区与标题之间的节奏 */
.account-actions {
  padding-top: 0;
  margin-top: 8px;
  margin-bottom: var(--page-section-gap, 24px);
}

/* 适配移动端：保证左右控件可点区域充足 */
@media (width <= 767px) {
  .icon-btn {
    width: 40px;
    height: 40px;
    border-radius: 20px;
  }
}
</style>
