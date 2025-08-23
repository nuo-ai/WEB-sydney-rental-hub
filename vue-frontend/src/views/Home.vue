<template>
  <div class="home-container">
    <!-- 主页内容 -->
    <main class="main-content">
      <!-- 移动端Logo区域 -->
      <div class="mobile-logo-section">
        <div class="container">
          <div class="mobile-logo">
            <i class="fa-solid fa-house logo-icon"></i>
            <span class="logo-text">JUWO 桔屋找房</span>
          </div>
        </div>
      </div>

      <!-- 搜索和筛选区域 - Domain风格全屏容器 -->
      <div class="search-filter-section">
        <div class="search-content-container">
          <!-- PC端：搜索框和筛选标签在同一行 -->
          <div class="search-filter-row">
            <SearchBar 
              class="search-bar"
              @search="handleSearch"
              @locationSelected="handleLocationSelected"
            />
            <FilterTabs 
              class="filter-tabs-right"
              :filter-panel-open="showFilterPanel"
              @toggleFullPanel="handleToggleFullPanel"
              @filtersChanged="handleQuickFiltersChanged"
            />
          </div>
          
          <!-- 结果统计 -->
          <div class="results-summary chinese-text">
            <p class="results-count">
              找到 <strong>{{ propertiesStore.filteredProperties.length }}</strong> 套房源
            </p>
          </div>
        </div>
      </div>

      <!-- 房源列表 -->
      <div class="container">
        <div class="properties-section">
          <!-- 加载状态 -->
          <div v-if="propertiesStore.loading" class="loading-spinner">
            <el-icon class="is-loading" :size="24">
              <Loading />
            </el-icon>
            <span class="chinese-text">正在加载房源...</span>
          </div>

          <!-- 错误状态 -->
          <div v-else-if="propertiesStore.error" class="error-message">
            <el-icon :size="48" color="#f56c6c">
              <Warning />
            </el-icon>
            <p class="chinese-text">{{ propertiesStore.error }}</p>
            <el-button type="primary" @click="retryLoadProperties">
              重新加载
            </el-button>
          </div>

          <!-- 空状态 -->
          <div v-else-if="propertiesStore.filteredProperties.length === 0" class="empty-state">
            <el-icon :size="64" color="#d9d9d9">
              <House />
            </el-icon>
            <h3 class="chinese-text">没有找到匹配的房源</h3>
            <p class="chinese-text">请尝试调整搜索条件或筛选器</p>
            <el-button type="primary" @click="clearFilters">
              清除筛选条件
            </el-button>
          </div>

          <!-- 房源网格 -->
          <div v-else class="properties-grid">
            <PropertyCard
              v-for="property in displayedProperties"
              :key="property.listing_id"
              :property="property"
              @click="goToPropertyDetail"
              @contact="handleContactProperty"
            />
          </div>

          <!-- 分页组件 -->
          <div v-if="propertiesStore.totalPages > 1" class="pagination-container">
            <el-pagination
              v-model:current-page="propertiesStore.currentPage"
              :page-size="propertiesStore.pageSize"
              :total="propertiesStore.filteredProperties.length"
              layout="prev, pager, next"
              class="pagination"
              @current-change="handlePageChange"
            />
          </div>
        </div>
      </div>
    </main>

    <!-- 筛选面板 -->
    <FilterPanel 
      v-model="showFilterPanel"
      @filtersChanged="handleFiltersChanged"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { usePropertiesStore } from '@/stores/properties'
import PropertyCard from '@/components/PropertyCard.vue'
import SearchBar from '@/components/SearchBar.vue'
import FilterTabs from '@/components/FilterTabs.vue'
import FilterPanel from '@/components/FilterPanel.vue'
import { Loading, Warning, House } from '@element-plus/icons-vue'

// 路由
const router = useRouter()

// 状态管理
const propertiesStore = usePropertiesStore()

// 响应式数据
const showFilterPanel = ref(false)

// 计算属性
const displayedProperties = computed(() => {
  return propertiesStore.paginatedProperties
})

// 方法
const handleSearch = (query) => {
  console.log('🔍 执行搜索:', query)
  // 搜索逻辑已在SearchBar组件中处理，这里主要是响应搜索事件
}

const handleLocationSelected = (location) => {
  console.log('📍 区域选择变更:', location)
  // 应用筛选
  applyCurrentFilters()
}

const handleToggleFullPanel = (show) => {
  console.log('🔧 切换完整筛选面板:', show)
  showFilterPanel.value = show
}

const handleQuickFiltersChanged = (filters) => {
  console.log('⚡ 快速筛选变更:', filters)
  // 快速筛选逻辑已在FilterTabs组件中处理
}

const handleFiltersChanged = (filters) => {
  console.log('🔧 筛选条件变更:', filters)
  // 筛选逻辑已在FilterPanel组件中处理
}

const handlePageChange = (page) => {
  console.log('📄 页面切换:', page)
  propertiesStore.setCurrentPage(page)
  
  // 滚动到顶部
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

const goToPropertyDetail = (property) => {
  console.log('🏠 查看房源详情:', property.listing_id)
  router.push(`/property/${property.listing_id}`)
}

const handleContactProperty = (property) => {
  console.log('📞 联系JUWO:', property.listing_id)
  // TODO: 实现联系我们功能
  // 可以打开联系表单、跳转到联系页面等
  ElMessage.success(`正在为您联系关于 ${property.address} 的房源信息`)
}

const retryLoadProperties = () => {
  propertiesStore.clearError()
  loadProperties()
}

const clearFilters = () => {
  propertiesStore.resetFilters()
  showFilterPanel.value = false
}

const applyCurrentFilters = () => {
  // 应用当前的筛选条件
  propertiesStore.applyFilters({
    minPrice: null,
    maxPrice: null,
    bedrooms: 'any',
    bathrooms: 'any',
    parking: 'any',
    availableDate: 'any',
    isFurnished: false
  })
}

const loadProperties = async () => {
  try {
    await propertiesStore.fetchProperties()
    console.log('✅ 房源数据加载完成')
  } catch (error) {
    console.error('❌ 房源数据加载失败:', error)
  }
}

// 生命周期
onMounted(() => {
  loadProperties()
})
</script>

<style scoped>
/* 主页容器 */
.home-container {
  min-height: 100vh;
  background-color: var(--color-bg-page);
  padding-bottom: 80px; /* 为移动端底部导航留空间 */
}

@media (min-width: 769px) {
  .home-container {
    padding-bottom: 0;
  }
}

/* 主内容区域 */
.main-content {
  width: 100%;
}

.container {
  max-width: 1200px; /* 统一最大宽度 */
  margin: 0 auto;
  padding: 24px 32px;
}

@media (min-width: 768px) {
  .container {
    padding: 32px 32px;
  }
}

@media (min-width: 1024px) {
  .container {
    padding: 40px 32px;
  }
}

/* 页面标题 */
.page-header {
  margin-bottom: 32px;
  text-align: left;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 8px;
  line-height: 1.2;
}

.page-subtitle {
  font-size: 18px;
  color: var(--color-text-secondary);
  line-height: 1.4;
}

@media (min-width: 768px) {
  .page-title {
    font-size: 36px;
  }
  
  .page-subtitle {
    font-size: 20px;
  }
}

/* 移动端Logo区域 */
.mobile-logo-section {
  display: block;
  margin-bottom: 20px;
}

.mobile-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px 0;
}

.logo-icon {
  width: 28px;
  height: 28px;
  background: var(--juwo-primary);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 14px;
}

.logo-text {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-text-primary);
}

/* PC端隐藏移动端Logo */
@media (min-width: 769px) {
  .mobile-logo-section {
    display: none;
  }
}

/* Domain标准搜索区域 - 全屏容器 */
.search-filter-section {
  /* 从一开始就横贯整个屏幕，像Domain一样 */
  width: 100%;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  margin-bottom: 24px;
  position: sticky;
  top: 0; /* 粘在屏幕顶部，导航栏滚动消失后搜索框占据顶部 */
  z-index: 50;
}

.search-content-container {
  /* 搜索内容居中对齐容器 */
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px 32px 16px 32px;
}

/* 搜索行布局 */
.search-filter-row {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 12px;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.search-bar {
  width: 580px; /* 与房源卡片宽度一致 */
  flex-shrink: 0;
}

.filter-tabs-right {
  flex-shrink: 0;
  display: flex;
  align-items: center;
}

.results-summary {
  max-width: 1200px;
  margin: 0 auto;
}

.results-count {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin: 0;
}

.results-count strong {
  color: var(--juwo-primary);
  font-weight: 600;
}

/* 移动端布局调整 */
@media (max-width: 768px) {
  .search-filter-section {
    margin-bottom: 16px;
  }
  
  .search-content-container {
    padding: 16px 24px 12px 24px;
  }
  
  .search-filter-row {
    flex-direction: column;
    gap: 12px;
  }
  
  .search-bar {
    width: 100%;
  }
  
  .filter-tabs-right {
    width: 100%;
  }
}

/* 房源列表区域 */
.properties-section {
  min-height: 400px;
}

/* 加载状态 */
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  gap: 16px;
  color: var(--color-text-secondary);
}

/* 错误状态 */
.error-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  gap: 16px;
  text-align: center;
}

.error-message p {
  font-size: 16px;
  color: var(--color-text-secondary);
  margin: 0;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  gap: 16px;
  text-align: center;
}

.empty-state h3 {
  font-size: 20px;
  color: var(--color-text-primary);
  margin: 0;
}

.empty-state p {
  font-size: 16px;
  color: var(--color-text-secondary);
  margin: 0;
}

/* 房源网格 - 单列布局 */
.properties-grid {
  display: flex;
  flex-direction: column;
  gap: 24px;
  align-items: flex-start;
  /* max-width 将由外部容器 .container 控制 */
}

/* 分页容器 */
.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 40px;
  padding: 20px;
}

.pagination :deep(.el-pager .number) {
  color: var(--color-text-secondary);
}

.pagination :deep(.el-pager .number:hover) {
  color: var(--juwo-primary);
}

.pagination :deep(.el-pager .number.is-active) {
  color: var(--juwo-primary);
  background-color: var(--juwo-primary-50);
}

.pagination :deep(.btn-prev),
.pagination :deep(.btn-next) {
  color: var(--color-text-secondary);
}

.pagination :deep(.btn-prev):hover,
.pagination :deep(.btn-next):hover {
  color: var(--juwo-primary);
}

/* 响应式搜索筛选区域 */
@media (max-width: 767px) {
  .search-filter-section {
    max-width: none;
    margin-bottom: 16px;
  }
  
  .search-filter-container {
    flex-direction: column;
    gap: 12px;
    width: 100%;
  }
  
  .search-bar {
    width: 100%;
  }
  
  .filter-trigger-btn {
    width: 100%;
    height: 48px;
    border-radius: 6px;
  }
}
</style>
