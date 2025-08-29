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
      <div 
        ref="searchBarElement"
        class="search-filter-section"
        :class="{ 
          'is-fixed': isSearchBarFixed,
          'nav-hidden': isNavHidden && windowWidth > 768
        }"
      >
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
              找到 <strong>{{ propertiesStore.totalCount }}</strong> 套房源
            </p>
          </div>
        </div>
      </div>

      <!-- 布局偏移补偿 -->
      <div 
        v-if="isSearchBarFixed" 
        class="search-bar-spacer" 
        :style="{ height: searchBarHeight + 'px' }"
      ></div>

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
              :current-page="propertiesStore.currentPage"
              :page-size="propertiesStore.pageSize"
              :total="propertiesStore.totalCount"
              :disabled="propertiesStore.loading"
              layout="prev, pager, next, total"
              class="pagination"
              @current-change="handlePageChange"
            />
          </div>
        </div>
      </div>
    </main>

    <!-- 筛选面板 -->
    <FilterPanel 
      ref="filterPanelRef"
      v-model="showFilterPanel"
      @filtersChanged="handleFiltersChanged"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
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
const isSearchBarFixed = ref(false)
const searchBarHeight = ref(0)
const searchBarElement = ref(null)
const lastScrollY = ref(0)
const isNavHidden = ref(false)
const windowWidth = ref(window.innerWidth)
const filterPanelRef = ref(null)  // 添加FilterPanel组件的引用

// 定义事件发射器
const emit = defineEmits(['updateNavVisibility'])

// 计算属性
const displayedProperties = computed(() => {
  return propertiesStore.paginatedProperties
})

// 方法
const handleSearch = () => {
  // 搜索逻辑已在SearchBar组件中处理，这里主要是响应搜索事件
}

const handleLocationSelected = async (location) => {
  // 当选择或移除区域后，调用API进行服务端筛选
  const selectedSuburbs = propertiesStore.selectedLocations.map(loc => loc.name)
  console.log('🏠 handleLocationSelected被调用:', { 
    location, 
    selectedSuburbs,
    selectedCount: selectedSuburbs.length 
  })
  
  try {
    if (selectedSuburbs.length > 0) {
      // 有选中的区域，进行筛选
      const params = {
        suburb: selectedSuburbs.join(',')
      }
      console.log('🔍 发送筛选请求:', params)
      await propertiesStore.fetchProperties(params)
    } else {
      // 没有选中的区域，加载所有房源
      console.log('📂 加载所有房源')
      await propertiesStore.fetchProperties()
    }
  } catch (error) {
    console.error('筛选房源失败:', error)
  }
}

const handleToggleFullPanel = (show) => {
  showFilterPanel.value = show
}

const handleQuickFiltersChanged = (filterParams) => {
  // 同步快速筛选数据到FilterPanel
  if (filterPanelRef.value) {
    // 转换格式以同步到FilterPanel
    const syncData = {
      priceRange: filterParams.minPrice !== null || filterParams.maxPrice !== null
        ? [filterParams.minPrice || 0, filterParams.maxPrice || 5000]
        : [0, 5000],
      bedrooms: filterParams.bedrooms === 'any' ? [] : filterParams.bedrooms.split(','),
      bathrooms: filterParams.bathrooms === 'any' ? [] : filterParams.bathrooms?.split(',') || [],
      parking: filterParams.parking === 'any' ? [] : filterParams.parking?.split(',') || []
    }
    filterPanelRef.value.setFilters(syncData)
  }
}

const handleFiltersChanged = () => {
  // 筛选逻辑已在FilterPanel组件中处理
}

const handlePageChange = async (page) => {
  await propertiesStore.setCurrentPage(page)
  
  // 滚动到顶部
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

const goToPropertyDetail = (property) => {
  // 将当前房源数据存储到store，这样详情页可以立即显示
  propertiesStore.currentProperty = property
  router.push({ name: 'PropertyDetail', params: { id: property.listing_id } })
}

const handleContactProperty = (property) => {
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
  } catch (error) {
    console.error('❌ 房源数据加载失败:', error)
  }
}

// 窗口大小变化处理
const handleResize = () => {
  windowWidth.value = window.innerWidth
}

// 滚动处理逻辑
const handleScroll = () => {
  if (!searchBarElement.value) return
  
  const currentScrollY = window.scrollY
  const scrollDelta = currentScrollY - lastScrollY.value
  const isMobileView = windowWidth.value <= 768
  
  // 搜索栏固定逻辑 - 改进移动端逻辑
  const searchBarRect = searchBarElement.value.getBoundingClientRect()
  
  if (isMobileView) {
    // 移动端：更精确的固定逻辑，考虑logo区域高度
    const logoSection = document.querySelector('.mobile-logo-section')
    const logoHeight = logoSection ? logoSection.offsetHeight : 32 // fallback高度
    const shouldBeFixed = currentScrollY > logoHeight
    
    if (shouldBeFixed && !isSearchBarFixed.value) {
      searchBarHeight.value = searchBarElement.value.offsetHeight
      isSearchBarFixed.value = true
    } else if (!shouldBeFixed && isSearchBarFixed.value) {
      isSearchBarFixed.value = false
      searchBarHeight.value = 0
    }
  } else {
    // 桌面端：保持原有逻辑
    const shouldBeFixed = searchBarRect.top <= 0
    
    if (shouldBeFixed && !isSearchBarFixed.value) {
      searchBarHeight.value = searchBarElement.value.offsetHeight
      isSearchBarFixed.value = true
    } else if (!shouldBeFixed && isSearchBarFixed.value) {
      isSearchBarFixed.value = false
      searchBarHeight.value = 0
    }
  }
  
  // 导航栏显示/隐藏逻辑（仅在桌面端）
  if (!isMobileView) {
    const scrollThreshold = 5
    
    // 回到顶部附近时强制重置导航栏状态
    if (currentScrollY < 50) {
      if (isNavHidden.value) {
        isNavHidden.value = false
        emit('updateNavVisibility', false)
      }
    } else if (Math.abs(scrollDelta) > scrollThreshold) {
      if (scrollDelta > 0 && currentScrollY > 100) {
        // 向下滚动且距离超过100px，隐藏导航栏
        if (!isNavHidden.value) {
          isNavHidden.value = true
          emit('updateNavVisibility', true)
        }
      } else if (scrollDelta < 0) {
        // 向上滚动，显示导航栏
        if (isNavHidden.value) {
          isNavHidden.value = false
          emit('updateNavVisibility', false)
        }
      }
    }
  } else {
    // 移动端：强制确保状态清洁
    if (isNavHidden.value) {
      isNavHidden.value = false
      // 不发送emit事件，避免影响App组件
    }
  }
  
  lastScrollY.value = currentScrollY
}

// 初始化搜索栏高度
const initSearchBarHeight = async () => {
  await nextTick()
  if (searchBarElement.value) {
    searchBarHeight.value = searchBarElement.value.offsetHeight
  }
}

// 生命周期
onMounted(async () => {
  // 只在没有数据时才加载，避免覆盖筛选结果
  if (propertiesStore.filteredProperties.length === 0) {
    loadProperties()
  }
  await initSearchBarHeight()
  lastScrollY.value = window.scrollY
  window.addEventListener('scroll', handleScroll, { passive: true })
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
/* 主页容器 */
.home-container {
  min-height: 100vh;
  background-color: var(--color-bg-page);
  padding-bottom: 80px; /* 为移动端底部导航留空间 */
  overflow-x: hidden; /* 防止固定宽度元素造成水平滚动，不影响内部粘性定位 */
}

@media (min-width: 769px) {
  .home-container {
    padding-bottom: 0;
  }
}

/* 主内容区域 */
.main-content {
  width: 100%;
  /* 移除 overflow-x: hidden 以修复粘性定位 */
}

.container {
  max-width: 1200px; /* 统一最大宽度 */
  margin: 0 auto;
  padding: 16px 32px; /* 减少移动端上下padding */
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


/* Domain标准搜索区域 - 全屏容器 */
.search-filter-section {
  /* 从一开始就横贯整个屏幕，像Domain一样 */
  width: 100%;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  margin-bottom: 16px; /* 减少移动端下边距 */
  z-index: 50;
  transition: all 0.2s ease-out;
}

/* 固定定位状态 */
.search-filter-section.is-fixed {
  position: fixed;
  top: 64px; /* 默认在导航栏下方 */
  left: 0;
  right: 0;
  margin-bottom: 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: top 0.2s ease-in-out;
}

/* 当导航栏隐藏时，搜索栏贴顶 */
@media (min-width: 769px) {
  .search-filter-section.is-fixed.nav-hidden {
    top: 0;
  }
}

/* 移动端搜索栏始终贴顶 */
@media (max-width: 768px) {
  .search-filter-section.is-fixed {
    top: 0;
  }
}

/* 布局偏移补偿 */
.search-bar-spacer {
  width: 100%;
}

/* 移动端Logo区域 */
.mobile-logo-section {
  padding: 8px 0 12px 0; /* 减少上下间距，上8px下12px */
  position: relative;
  /* 移除高z-index，避免与fixed搜索栏产生叠加问题 */
}

.mobile-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 20px;
  font-weight: 600;
  color: var(--juwo-primary);
}

.logo-icon {
  font-size: 24px;
}

/* 在桌面端隐藏移动端Logo */
@media (min-width: 769px) {
  .mobile-logo-section {
    display: none;
  }
}

.search-content-container {
  /* 搜索内容居中对齐容器 */
  max-width: 1200px;
  margin: 0 auto;
  padding: 16px 32px 12px 32px; /* 减少上下padding */
}

/* 搜索行布局 */
.search-filter-row {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 12px;
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
    margin-bottom: 12px; /* 进一步减少移动端间距 */
  }
  
  .search-content-container {
    padding: 12px 24px 8px 24px; /* 减少移动端搜索内容padding */
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
