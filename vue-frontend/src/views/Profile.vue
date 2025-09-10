<template>
  <div class="profile-page">
    <!-- 顶部导航 -->
    <header class="page-header">
      <div class="container">
        <button class="btn btn-icon" @click="$router.back()">
          <i class="fas fa-arrow-left"></i>
        </button>
        <h1 class="page-title">个人中心</h1>
        <button class="btn btn-icon" @click="showSettings = true">
          <i class="fas fa-cog"></i>
        </button>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="page-content">
      <div class="container">
        <!-- 用户信息卡片 -->
        <section class="user-section">
          <div class="card user-card">
            <div class="card-body">
              <div class="user-avatar">
                <div class="avatar-placeholder">
                  <i class="fas fa-user"></i>
                </div>
                <button class="btn btn-sm btn-primary">更换头像</button>
              </div>
              <div class="user-info">
                <h2 class="user-name">{{ userInfo.name || '游客用户' }}</h2>
                <p class="user-email">{{ userInfo.email || '未登录' }}</p>
                <div class="user-stats">
                  <div class="stat-item">
                    <span class="stat-value">{{ favoriteCount }}</span>
                    <span class="stat-label">收藏</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-value">{{ historyCount }}</span>
                    <span class="stat-label">浏览</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-value">{{ savedSearchCount }}</span>
                    <span class="stat-label">订阅</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- 快捷操作 -->
        <section class="quick-actions">
          <div class="section-header">
            <h3 class="section-title">快捷操作</h3>
          </div>
          <div class="action-grid">
            <button class="action-card" @click="activeTab = 'favorites'">
              <i class="fas fa-heart action-icon"></i>
              <span class="action-label">我的收藏</span>
              <span class="badge" v-if="favoriteCount">{{ favoriteCount }}</span>
            </button>
            <button class="action-card" @click="activeTab = 'history'">
              <i class="fas fa-history action-icon"></i>
              <span class="action-label">浏览历史</span>
              <span class="badge" v-if="newHistoryCount">{{ newHistoryCount }}</span>
            </button>
            <button class="action-card" @click="activeTab = 'searches'">
              <i class="fas fa-bell action-icon"></i>
              <span class="action-label">搜索订阅</span>
              <span class="badge badge-dot" v-if="hasNewProperties"></span>
            </button>
            <button class="action-card" @click="activeTab = 'settings'">
              <i class="fas fa-cog action-icon"></i>
              <span class="action-label">账号设置</span>
            </button>
          </div>
        </section>

        <!-- 标签页内容 -->
        <section class="content-section">
          <!-- 标签导航 -->
          <div class="tabs">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              :class="['tab', { active: activeTab === tab.id }]"
              @click="activeTab = tab.id"
            >
              <i :class="tab.icon"></i>
              <span>{{ tab.label }}</span>
            </button>
          </div>

          <!-- 标签内容 -->
          <div class="tab-content">
            <!-- 我的收藏 -->
            <div v-if="activeTab === 'favorites'" class="favorites-content">
              <div v-if="favorites.length === 0" class="empty-state">
                <i class="fas fa-heart empty-icon"></i>
                <h4 class="empty-title">暂无收藏</h4>
                <p class="empty-text">点击房源卡片上的心形图标即可收藏</p>
                <button class="btn btn-primary" @click="$router.push('/')">去看看房源</button>
              </div>
              <div v-else class="property-grid">
                <div v-for="item in favorites" :key="item.id" class="card property-card-mini">
                  <img :src="item.image" :alt="item.address" class="property-image-mini" />
                  <div class="card-body">
                    <div class="price price-sm">
                      <span class="price-symbol">$</span>
                      <span class="price-value">{{ item.rent_pw }}</span>
                      <span class="price-unit">/周</span>
                    </div>
                    <div class="address">
                      <div class="address-primary">{{ item.address }}</div>
                      <div class="address-secondary">{{ item.suburb }}</div>
                    </div>
                    <div class="specs">
                      <span class="spec-item">
                        <i class="fas fa-bed spec-icon"></i>
                        <span class="spec-value">{{ item.bedrooms }}</span>
                      </span>
                      <span class="spec-item">
                        <i class="fas fa-bath spec-icon"></i>
                        <span class="spec-value">{{ item.bathrooms }}</span>
                      </span>
                      <span class="spec-item">
                        <i class="fas fa-car spec-icon"></i>
                        <span class="spec-value">{{ item.car_spaces }}</span>
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 浏览历史 -->
            <div v-if="activeTab === 'history'" class="history-content">
              <div class="history-list">
                <div v-for="item in browsingHistory" :key="item.id" class="history-item">
                  <div class="history-date">{{ formatDate(item.viewedAt) }}</div>
                  <div class="card history-card">
                    <div class="card-body">
                      <div class="history-property">
                        <img :src="item.image" :alt="item.address" class="history-image" />
                        <div class="history-info">
                          <h4 class="history-address">{{ item.address }}</h4>
                          <p class="history-suburb">{{ item.suburb }}, NSW</p>
                          <div class="price price-sm">
                            <span class="price-symbol">$</span>
                            <span class="price-value">{{ item.rent_pw }}</span>
                            <span class="price-unit">/周</span>
                          </div>
                        </div>
                        <button class="btn btn-sm btn-outline">查看详情</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 搜索订阅 -->
            <div v-if="activeTab === 'searches'" class="searches-content">
              <div class="search-list">
                <div v-for="search in savedSearches" :key="search.id" class="card search-card">
                  <div class="card-body">
                    <div class="search-header">
                      <h4 class="search-name">{{ search.name }}</h4>
                      <div class="search-actions">
                        <button class="btn btn-icon btn-sm">
                          <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-icon btn-sm">
                          <i class="fas fa-trash"></i>
                        </button>
                      </div>
                    </div>
                    <div class="search-filters">
                      <span class="tag">{{ search.suburb }}</span>
                      <span class="tag">${{ search.minPrice }}-${{ search.maxPrice }}/周</span>
                      <span class="tag">{{ search.bedrooms }}卧室</span>
                    </div>
                    <div class="search-status">
                      <span class="status-dot"></span>
                      <span>{{ search.newCount }} 套新房源</span>
                      <span class="search-frequency">每日通知</span>
                    </div>
                  </div>
                </div>
              </div>
              <button class="btn btn-primary btn-block">
                <i class="fas fa-plus"></i>
                创建新的搜索订阅
              </button>
            </div>

            <!-- 账号设置 -->
            <div v-if="activeTab === 'settings'" class="settings-content">
              <div class="settings-group">
                <h4 class="settings-title">通知设置</h4>
                <div class="setting-item">
                  <div class="setting-info">
                    <span class="setting-label">邮件通知</span>
                    <span class="setting-hint">接收新房源和价格变动通知</span>
                  </div>
                  <label class="switch">
                    <input type="checkbox" v-model="settings.emailNotifications" />
                    <span class="switch-slider"></span>
                  </label>
                </div>
                <div class="setting-item">
                  <div class="setting-info">
                    <span class="setting-label">推送通知</span>
                    <span class="setting-hint">浏览器推送通知</span>
                  </div>
                  <label class="switch">
                    <input type="checkbox" v-model="settings.pushNotifications" />
                    <span class="switch-slider"></span>
                  </label>
                </div>
              </div>

              <div class="settings-group">
                <h4 class="settings-title">隐私设置</h4>
                <div class="setting-item">
                  <div class="setting-info">
                    <span class="setting-label">浏览历史</span>
                    <span class="setting-hint">保存最近浏览的房源</span>
                  </div>
                  <label class="switch">
                    <input type="checkbox" v-model="settings.saveHistory" />
                    <span class="switch-slider"></span>
                  </label>
                </div>
              </div>

              <div class="settings-actions">
                <button class="btn btn-secondary">清除缓存</button>
                <button class="btn btn-secondary">导出数据</button>
                <button class="btn btn-text" style="color: var(--status-error)">退出登录</button>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<script setup>
defineOptions({ name: 'ProfileView' })
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useFavoritesStore } from '@/stores/favorites'

const authStore = useAuthStore()
const favoritesStore = useFavoritesStore()

// 用户信息
const userInfo = computed(() => authStore.user || {})

// 标签页
const activeTab = ref('favorites')
const tabs = [
  { id: 'favorites', label: '我的收藏', icon: 'fas fa-heart' },
  { id: 'history', label: '浏览历史', icon: 'fas fa-history' },
  { id: 'searches', label: '搜索订阅', icon: 'fas fa-bell' },
  { id: 'settings', label: '账号设置', icon: 'fas fa-cog' },
]

// 统计数据
const favoriteCount = computed(() => favoritesStore.favoritesList.length)
const historyCount = ref(12)
const savedSearchCount = ref(3)
const newHistoryCount = ref(5)
const hasNewProperties = ref(true)

// 收藏列表（模拟数据）
const favorites = computed(() => {
  // 实际应该从 store 获取
  return [
    {
      id: 1,
      image: '/api/placeholder/300/200',
      address: '123 George Street',
      suburb: 'Sydney CBD',
      rent_pw: 750,
      bedrooms: 2,
      bathrooms: 1,
      car_spaces: 1,
    },
    {
      id: 2,
      image: '/api/placeholder/300/200',
      address: '456 Harris Street',
      suburb: 'Ultimo',
      rent_pw: 680,
      bedrooms: 1,
      bathrooms: 1,
      car_spaces: 0,
    },
  ]
})

// 浏览历史（模拟数据）
const browsingHistory = ref([
  {
    id: 1,
    viewedAt: new Date('2025-01-30T10:00:00'),
    image: '/api/placeholder/100/80',
    address: '789 Broadway',
    suburb: 'Glebe',
    rent_pw: 820,
  },
  {
    id: 2,
    viewedAt: new Date('2025-01-29T15:30:00'),
    image: '/api/placeholder/100/80',
    address: '321 King Street',
    suburb: 'Newtown',
    rent_pw: 590,
  },
])

// 搜索订阅（模拟数据）
const savedSearches = ref([
  {
    id: 1,
    name: 'CBD 两室公寓',
    suburb: 'Sydney CBD',
    minPrice: 600,
    maxPrice: 800,
    bedrooms: 2,
    newCount: 3,
  },
  {
    id: 2,
    name: 'Newtown 单间',
    suburb: 'Newtown',
    minPrice: 400,
    maxPrice: 500,
    bedrooms: 1,
    newCount: 0,
  },
])

// 设置
const settings = ref({
  emailNotifications: true,
  pushNotifications: false,
  saveHistory: true,
})

// 格式化日期
const formatDate = (date) => {
  const now = new Date()
  const diff = now - date
  const hours = Math.floor(diff / (1000 * 60 * 60))

  if (hours < 1) return '刚刚'
  if (hours < 24) return `${hours}小时前`
  if (hours < 48) return '昨天'

  return date.toLocaleDateString('zh-CN')
}
</script>

<style scoped>
/* 使用设计系统的样式 */
.profile-page {
  min-height: 100vh;
  background: var(--bg-page);
}

/* 页面头部 */
.page-header {
  background: var(--bg-card);
  border-bottom: 1px solid var(--border-light);
  position: sticky;
  top: 0;
  z-index: var(--z-sticky);
}

.page-header .container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: var(--height-navbar);
  padding: 0 var(--space-4);
}

.page-title {
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
}

/* 页面内容 */
.page-content {
  padding: var(--space-4) 0;
}

.container {
  max-width: var(--container-lg);
  margin: 0 auto;
  padding: 0 var(--space-4);
}

/* 用户卡片 */
.user-section {
  margin-bottom: var(--space-6);
}

.user-card .card-body {
  display: flex;
  gap: var(--gap-lg);
  padding: var(--space-6);
}

.user-avatar {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--gap-md);
}

.avatar-placeholder {
  width: 80px;
  height: 80px;
  background: var(--bg-hover);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--text-2xl);
  color: var(--text-tertiary);
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: var(--text-xl);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
  margin-bottom: var(--space-1);
}

.user-email {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  margin-bottom: var(--space-4);
}

.user-stats {
  display: flex;
  gap: var(--gap-xl);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: var(--text-2xl);
  font-weight: var(--font-bold);
  color: var(--text-primary);
}

.stat-label {
  font-size: var(--text-xs);
  color: var(--text-tertiary);
  text-transform: uppercase;
}

/* 快捷操作 */
.quick-actions {
  margin-bottom: var(--space-8);
}

.section-header {
  margin-bottom: var(--space-4);
}

.section-title {
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: var(--gap-md);
}

.action-card {
  position: relative;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--gap-sm);
  cursor: pointer;
  transition: var(--transition-all);
}

.action-card:hover {
  border-color: var(--brand-primary);
  box-shadow: var(--shadow-sm);
  transform: translateY(-2px);
}

.action-icon {
  font-size: var(--text-2xl);
  color: var(--brand-primary);
}

.action-label {
  font-size: var(--text-sm);
  color: var(--text-primary);
  font-weight: var(--font-medium);
}

.action-card .badge {
  position: absolute;
  top: var(--space-2);
  right: var(--space-2);
}

/* 标签页 */
.tabs {
  display: flex;
  gap: var(--gap-sm);
  border-bottom: 1px solid var(--border-light);
  margin-bottom: var(--space-4);
  overflow-x: auto;
}

.tab {
  padding: var(--space-3) var(--space-4);
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  color: var(--text-secondary);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  cursor: pointer;
  transition: var(--transition-colors);
  display: flex;
  align-items: center;
  gap: var(--gap-xs);
  white-space: nowrap;
}

.tab:hover {
  color: var(--text-primary);
}

.tab.active {
  color: var(--brand-primary);
  border-bottom-color: var(--brand-primary);
}

/* 标签内容 */
.tab-content {
  min-height: 400px;
}

/* 空状态 */
.empty-state {
  padding: var(--space-12) var(--space-4);
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--gap-md);
}

.empty-icon {
  font-size: 64px;
  color: var(--text-tertiary);
  opacity: 0.5;
}

.empty-title {
  font-size: var(--text-xl);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
}

.empty-text {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  max-width: 300px;
}

/* 房源网格 */
.property-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--gap-lg);
}

.property-card-mini {
  cursor: pointer;
  transition: var(--transition-all);
}

.property-card-mini:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.property-image-mini {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

/* 历史列表 */
.history-list {
  display: flex;
  flex-direction: column;
  gap: var(--gap-md);
}

.history-date {
  font-size: var(--text-sm);
  color: var(--text-tertiary);
  font-weight: var(--font-medium);
  margin-bottom: var(--space-2);
}

.history-property {
  display: flex;
  gap: var(--gap-md);
  align-items: center;
}

.history-image {
  width: 100px;
  height: 80px;
  object-fit: cover;
  border-radius: var(--radius-sm);
}

.history-info {
  flex: 1;
}

.history-address {
  font-size: var(--text-base);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
  margin-bottom: var(--space-1);
}

.history-suburb {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  margin-bottom: var(--space-2);
}

/* 搜索订阅 */
.search-list {
  display: flex;
  flex-direction: column;
  gap: var(--gap-md);
  margin-bottom: var(--space-4);
}

.search-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-3);
}

.search-name {
  font-size: var(--text-base);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
}

.search-actions {
  display: flex;
  gap: var(--gap-xs);
}

.search-filters {
  display: flex;
  flex-wrap: wrap;
  gap: var(--gap-xs);
  margin-bottom: var(--space-3);
}

.search-status {
  display: flex;
  align-items: center;
  gap: var(--gap-sm);
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.search-frequency {
  margin-left: auto;
  color: var(--text-tertiary);
}

/* 设置 */
.settings-content {
  max-width: 600px;
}

.settings-group {
  margin-bottom: var(--space-8);
}

.settings-title {
  font-size: var(--text-base);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
  margin-bottom: var(--space-4);
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-3) 0;
  border-bottom: 1px solid var(--border-light);
}

.setting-info {
  display: flex;
  flex-direction: column;
  gap: var(--gap-xs);
}

.setting-label {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--text-primary);
}

.setting-hint {
  font-size: var(--text-xs);
  color: var(--text-tertiary);
}

/* 开关 */
.switch {
  position: relative;
  display: inline-block;
  width: 48px;
  height: 24px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.switch-slider {
  position: absolute;
  cursor: pointer;
  inset: 0;
  background-color: var(--bg-hover);
  transition: var(--transition-colors);
  border-radius: var(--radius-full);
}

.switch-slider::before {
  position: absolute;
  content: '';
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: var(--transition-transform);
  border-radius: var(--radius-full);
}

.switch input:checked + .switch-slider {
  background-color: var(--brand-primary);
}

.switch input:checked + .switch-slider::before {
  transform: translateX(24px);
}

.settings-actions {
  display: flex;
  flex-direction: column;
  gap: var(--gap-md);
  padding-top: var(--space-6);
}

/* 工具类 */
.btn-block {
  width: 100%;
}

/* 响应式 */
@media (width <= 768px) {
  .user-card .card-body {
    flex-direction: column;
    text-align: center;
  }

  .user-stats {
    justify-content: center;
  }

  .action-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .property-grid {
    grid-template-columns: 1fr;
  }

  .history-property {
    flex-direction: column;
    text-align: center;
  }

  .history-image {
    width: 100%;
    height: 200px;
  }
}
</style>
