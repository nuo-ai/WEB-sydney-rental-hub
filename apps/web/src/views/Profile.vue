<template>
  <div class="page profile-page">
    <!-- 1. 页面头部: 完全遵循样板和视觉标准 -->
    <header class="page__header header-with-back">
      <!-- 返回上一页（无历史则回首页） -->
      <BaseIconButton aria-label="返回上一页" @click="goBack">
        <ArrowLeft />
      </BaseIconButton>

      <h1 class="typo-h1 page-title">{{ pageTitle }}</h1>
    </header>

    <!-- 页面操作区：回到首页、退出登录 -->
    <section class="page__toolbar account-toolbar" aria-label="页面操作">
      <div class="account-toolbar__actions">
        <router-link to="/" class="account-toolbar__link">
          <BaseButton variant="ghost" aria-label="回到首页">回到首页</BaseButton>
        </router-link>
        <BaseButton variant="secondary" @click="handleLogout">退出登录</BaseButton>
      </div>
    </section>

    <!-- 2. 页面内容区 -->
    <main class="page__content">

      <!-- 3. 第一个区块：我的收藏 -->
      <section class="page-section">
        <div class="section-header">
          <h2 class="typo-h2">我的收藏（共 {{ favoritesCount }}）</h2>
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
            @click="goToPropertyDetail"
          />
        </div>
        <div v-else class="empty-state">
          <p class="typo-body">您还没有收藏任何房源。</p>
        </div>
      </section>

      <!-- 4. 第二个区块：最近浏览 -->
      <section class="page-section">
        <div class="section-header">
          <h2 class="typo-h2">最近浏览（共 {{ historyCount }}）</h2>
        </div>

        <!-- 动态内容：历史记录列表或空状态 -->
        <div v-if="historyProperties.length > 0" class="property-grid">
          <!-- 复用 PropertyCard 组件，并只显示最近3条 -->
          <PropertyCard
            v-for="property in recentHistory"
            :key="property.listing_id"
            :property="property"
            @click="goToPropertyDetail"
          />
        </div>
        <div v-else class="empty-state">
          <p class="typo-body">暂无浏览记录。</p>
        </div>
      </section>

      <!-- 5. 第三个区块：我的筛选 -->
      <section class="page-section">
        <div class="section-header">
          <h2 class="typo-h2">我的筛选（共 {{ savedSearchesCount }}）</h2>
        </div>
        <SavedSearchesManager @updated="handleSavedSearchesUpdated" />
      </section>

    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ArrowLeft } from 'lucide-vue-next'
// 假设你的 store 文件和基础组件路径如下
import { usePropertiesStore } from '@/stores/properties'
import PropertyCard from '@/components/PropertyCard.vue'
import BaseButton from '@/components/base/BaseButton.vue' // 确保路径正确
import BaseIconButton from '@/components/base/BaseIconButton.vue'
import SavedSearchesManager from '@/components/SavedSearchesManager.vue'
import { useFilterWizard } from '@/composables/useFilterWizard'

defineOptions({ name: 'ProfileView' })

const pageTitle = ref('我的中心')

const router = useRouter()
const authStore = useAuthStore()
const { getSavedSearches } = useFilterWizard()

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

// 中文注释：概览页只回显总数（避免越权到管理页）
// 为什么：Profile 仅承担"收藏概览 + 入口"，完整管理在 /favorites。
// 前端表现：标题显示"（共 N）/（共 M）"，下方仅渲染最近 3 条。
const favoritesCount = computed(() => favoriteProperties.value.length)
const historyCount = computed(() => historyProperties.value.length)

// 已保存搜索计数
const savedSearches = ref([])
const savedSearchesCount = computed(() => savedSearches.value.length)

// 7. 实现业务逻辑：只取最近的3条记录
const recentFavorites = computed(() => favoriteProperties.value.slice(0, 3))
const recentHistory = computed(() => historyProperties.value.slice(0, 3))

const goToPropertyDetail = (property) => {
  if (!property || !property.listing_id) return
  router.push({ name: 'PropertyDetail', params: { id: property.listing_id } })
}

const refreshSavedSearches = () => {
  try {
    savedSearches.value = getSavedSearches()
  } catch (error) {
    console.error('获取已保存搜索计数失败:', error)
    savedSearches.value = []
  }
}

const handleSavedSearchesUpdated = (list) => {
  if (Array.isArray(list)) {
    savedSearches.value = list
    return
  }
  refreshSavedSearches()
}

onMounted(() => {
  refreshSavedSearches()
  propertiesStore.fetchFavoriteProperties().catch((error) => {
    console.error('获取收藏房源失败:', error)
  })
})

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

.empty-state,
.placeholder-state {
  padding: var(--space-xl) var(--space-4);
  background-color: var(--color-bg-card);
  border: 1px dashed var(--color-border-default);
  border-radius: var(--radius-md);
  text-align: center;
}

.text-secondary {
  color: var(--color-text-secondary);
}

.header-with-back {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.header-with-back .page-title {
  margin: 0;
}

.account-toolbar {
  display: flex;
  justify-content: flex-end;
}

.account-toolbar__actions {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.account-toolbar__link {
  display: inline-flex;
  text-decoration: none;
}
</style>
