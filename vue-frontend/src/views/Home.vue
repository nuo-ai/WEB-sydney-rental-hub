<template>
  <div class="home-container">
    <!-- 主页内容 -->
    <main class="main-content">
      <div class="container">
        <!-- 页面标题 -->
        <header class="page-header">
          <h1 class="page-title chinese-text">为你找到的房源</h1>
          <p class="page-subtitle chinese-text">基于你的偏好，我们推荐以下房源</p>
        </header>

        <!-- 搜索和筛选区域 -->
        <div class="search-filter-section">
          <div class="search-filter-container">
            <!-- 搜索栏 -->
            <SearchBar 
              class="search-bar"
              @search="handleSearch"
              @locationSelected="handleLocationSelected"
            />
            
            <!-- 筛选按钮 -->
            <el-button 
              class="filter-trigger-btn"
              size="large"
              @click="showFilterPanel = true"
            >
              <i class="fa-solid fa-sliders"></i>
            </el-button>
          </div>
          
          <!-- 结果统计 -->
          <div class="results-summary chinese-text">
            <p class="results-count">
              找到 <strong>{{ propertiesStore.filteredProperties.length }}</strong> 套房源
            </p>
          </div>
        </div>

        <!-- 房源列表 -->
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
    padding-top: 64px; /* 为桌面端顶部导航留空间 */
    padding-bottom: 0;
  }
}

/* 主内容区域 */
.main-content {
  width: 100%;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px 16px;
}

@media (min-width: 768px) {
  .container {
    padding: 32px 24px;
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

/* 搜索筛选区域 */
.search-filter-section {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: var(--radius-lg);
  padding: 20px;
  margin-bottom: 32px;
  border: 1px solid var(--color-border-default);
  position: sticky;
  top: 80px;
  z-index: 50;
}

@media (min-width: 769px) {
  .search-filter-section {
    top: 80px;
  }
}

.search-filter-container {
  display: flex;
  gap: 16px;
  align-items: flex-start;
  margin-bottom: 16px;
}

.search-bar {
  flex: 1;
}

.filter-trigger-btn {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  border-radius: var(--radius-lg);
  border: 2px solid var(--color-border-default);
  background: white;
  color: var(--color-text-secondary);
  transition: all 0.2s ease;
}

.filter-trigger-btn:hover {
  border-color: var(--juwo-primary);
  color: var(--juwo-primary);
  background: var(--juwo-primary-50);
}

/* 结果统计 */
.results-summary {
  border-top: 1px solid var(--color-border-default);
  padding-top: 16px;
}

.results-count {
  font-size: 16px;
  color: var(--color-text-primary);
  margin: 0;
}

.results-count strong {
  color: var(--juwo-primary);
  font-weight: 700;
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

/* 房源网格 */
.properties-grid {
  display: grid;
  gap: 24px;
  justify-items: center;
}

/* 移动端 - 单列布局 */
@media (max-width: 767px) {
  .properties-grid {
    grid-template-columns: 1fr;
  }
}

/* 平板端 - 双列布局 */
@media (min-width: 768px) and (max-width: 1199px) {
  .properties-grid {
    grid-template-columns: repeat(2, 1fr);
    max-width: 1200px;
    margin: 0 auto;
  }
}

/* 桌面端 - 灵活布局 */
@media (min-width: 1200px) {
  .properties-grid {
    grid-template-columns: repeat(auto-fit, minmax(580px, 1fr));
    max-width: 1800px;
    margin: 0 auto;
  }
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
    margin: 0 -16px 24px -16px;
    border-radius: 0;
    border-left: none;
    border-right: none;
    top: 0;
  }
  
  .search-filter-container {
    flex-direction: column;
    gap: 12px;
  }
  
  .filter-trigger-btn {
    width: 100%;
    height: 48px;
  }
}
</style>
