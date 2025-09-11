<template>
  <div class="home-container">
    <!-- 主页内容 -->
    <main class="main-content">
      <!-- 移动端Logo区域 -->
      <div class="mobile-logo-section">
        <div class="container">
          <div class="mobile-logo">
            <span class="brand-text">Juwo</span>
          </div>
        </div>
      </div>

      <!-- 搜索和筛选区域 - Domain风格全屏容器 -->
      <div
        ref="searchBarElement"
        class="search-filter-section"
        :class="{
          'is-fixed': isSearchBarFixed,
          'nav-hidden': isNavHidden && windowWidth > 768,
        }"
      >
        <div class="search-content-container">
          <!-- PC端：搜索框和筛选标签在同一行 -->
          <div class="search-filter-row">
            <SearchBar
              v-if="windowWidth <= 768"
              class="search-bar"
              @search="handleSearch"
              @locationSelected="handleLocationSelected"
              @openFilterPanel="handleOpenFilterPanel"
            />
            <!-- 桌面端使用分离式筛选面板，完全在 FilterTabs 组件内部处理 -->
            <FilterTabs class="filter-tabs-right" @requestOpenFullPanel="handleOpenFilterPanel" />
          </div>

          <!-- 结果统计移至搜索容器下方的新容器中；此处移除以避免双处回显 -->
        </div>
      </div>

      <!-- 布局偏移补偿 -->
      <div
        v-if="isSearchBarFixed"
        class="search-bar-spacer"
        :style="{ height: searchBarHeight + 'px' }"
      ></div>

      <!-- 标题区：面包屑 / H1 / 操作行（390 视口对齐参考站） -->
      <div class="container title-block" :class="{ 'align-to-card': !useVirtualScroll }">
        <nav class="breadcrumbs">
          <template v-if="isMultiSelect">
            首页/ NSW
          </template>
          <template v-else>
            首页 › NSW › {{ suburb || '—' }}
          </template>
        </nav>

        <h1 class="page-h1">
          <template v-if="isMultiSelect">
            {{ propertiesStore.totalCount }} 套房源，覆盖及周边 {{ selectedLocationsCount }} 个郊区
          </template>
          <template v-else-if="hasSingleSelection">
            {{ propertiesStore.totalCount }} 套房源在 {{ suburb || 'Sydney' }}, NSW
          </template>
          <template v-else>
            {{ propertiesStore.totalCount }} 套待租房源在 {{ suburb || 'Sydney' }}, NSW<span v-if="postcode">, {{ postcode }}</span>
          </template>
        </h1>

        <div class="actions-row">
          <div class="alert-left">
            <Bell :size="20" />
            <span class="label">Property alert</span>
            <el-switch v-model="alertOn" size="small" inactive-text="Off" />
          </div>

          <el-dropdown @command="onSortCommand" placement="bottom-end" :teleported="false">
            <button class="sort-btn" type="button">
              <ArrowUpDown :size="20" />
              <span class="label">Sort</span>
            </button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="price_asc">按最小价格</el-dropdown-item>
                <el-dropdown-item command="available_date_asc">按空出时间</el-dropdown-item>
                <el-dropdown-item command="inspection_earliest">按最早看房时间</el-dropdown-item>
                <el-dropdown-item command="suburb_az">按区域（首字母）</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
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
            <el-icon :size="48" class="error-icon">
              <Warning />
            </el-icon>
            <p class="chinese-text">{{ propertiesStore.error }}</p>
            <el-button type="primary" @click="retryLoadProperties"> 重新加载 </el-button>
          </div>

          <!-- 空状态 -->
          <div v-else-if="propertiesStore.filteredProperties.length === 0" class="empty-state">
            <el-icon :size="64" class="empty-icon">
              <House />
            </el-icon>
            <h3 class="chinese-text">没有找到匹配的房源</h3>
            <p class="chinese-text">请尝试调整搜索条件或筛选器</p>
            <el-button type="primary" @click="clearFilters"> 清除筛选条件 </el-button>
          </div>

          <!-- 房源列表容器 -->
          <div v-else class="properties-container">
            <!-- 虚拟滚动：数据量超过50条时启用，避免DOM节点过多导致的性能问题 -->
            <VirtualPropertyList
              v-if="useVirtualScroll"
              :properties="displayedProperties"
              @property-click="goToPropertyDetail"
              @contact-property="handleContactProperty"
            />

            <!-- 普通网格：小数据量保持原有交互体验，避免滚动条跳动 -->
            <div v-else class="properties-grid">
              <PropertyCard
                v-for="property in displayedProperties"
                :key="property.listing_id"
                :property="property"
                @click="goToPropertyDetail"
                @contact="handleContactProperty"
              />
            </div>
          </div>

          <!-- 分页组件：虚拟滚动启用时隐藏，两种导航方式互斥避免用户困惑 -->
          <div
            v-if="!useVirtualScroll && propertiesStore.totalPages > 1"
            class="pagination-container"
          >
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
      :focusSection="focusSection"
      @filtersChanged="handleFiltersChanged"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { usePropertiesStore } from '@/stores/properties'
import PropertyCard from '@/components/PropertyCard.vue'
import VirtualPropertyList from '@/components/VirtualPropertyList.vue'
import SearchBar from '@/components/SearchBar.vue'
import FilterPanel from '@/components/FilterPanel.vue'
import FilterTabs from '@/components/FilterTabs.vue'
import { Loading, Warning, House } from '@element-plus/icons-vue'
import { Bell, ArrowUpDown } from 'lucide-vue-next'

/* 路由 */
const router = useRouter()
const route = useRoute()

/* 状态管理 */
const propertiesStore = usePropertiesStore()

// 响应式数据
const showFilterPanel = ref(false)
const isSearchBarFixed = ref(false)
const searchBarHeight = ref(0)
const searchBarElement = ref(null)
const lastScrollY = ref(0)
const isNavHidden = ref(false)
const windowWidth = ref(window.innerWidth)
const filterPanelRef = ref(null) // 添加FilterPanel组件的引用
const focusSection = ref(null) // 指定面板打开时的聚焦分组

/* 排序入口：仅透传到后端；URL 状态同步，不做前端本地排序 */
const sortValue = ref('')
const handleSortChange = async (val) => {
  try {
    const newQuery = { ...route.query }
    if (val) newQuery.sort = val
    else delete newQuery.sort
    await router.replace({ query: newQuery })
    await propertiesStore.setSort(val)
  } catch (e) {
    console.error('排序切换失败:', e)
  }
}
/* 下拉命令转发至排序处理 */
const onSortCommand = (val) => handleSortChange(val)

/* 左侧通知开关占位（未来接入真实通知） */
const alertOn = ref(false)

/* 计算 suburb/postcode：从首个已选区域回显；无则优雅回退 */
const suburb = computed(() => {
  const list = propertiesStore.selectedLocations
  if (Array.isArray(list) && list.length) {
    const first = list[0]
    // 优先使用 suburb 名称；若是 postcode 类型且带 suburb 字段则取其 suburb
    return first?.type === 'suburb' ? first.name : first.suburb || first.name || ''
  }
  return ''
})
const postcode = computed(() => {
  const list = propertiesStore.selectedLocations
  if (Array.isArray(list) && list.length) {
    const first = list[0]
    // 常见 4 位邮编；若对象自带 postcode 字段优先
    const pc = first?.postcode || first?.name
    return typeof pc === 'string' && /^\d{4}$/.test(pc) ? pc : ''
  }
  return ''
})

// 选择状态：用于标题与面包屑的前端表现
// 说明：统一在前端用选择数量来判断“单选/多选”，避免依赖 store 内部实现细节
const selectedLocationsCount = computed(() => {
  const list = propertiesStore.selectedLocations
  return Array.isArray(list) ? list.length : 0
})
const hasSingleSelection = computed(() => selectedLocationsCount.value === 1)
const isMultiSelect = computed(() => selectedLocationsCount.value > 1)

// 定义事件发射器
const emit = defineEmits(['updateNavVisibility'])

// 计算属性
const displayedProperties = computed(() => {
  return propertiesStore.paginatedProperties
})

// 虚拟滚动控制：localStorage开关便于A/B测试和问题快速回滚
const VIRTUAL_SCROLL_THRESHOLD = 50
const useVirtualScroll = computed(() => {
  const enableVirtual = localStorage.getItem('enableVirtualScroll') !== 'false'
  return enableVirtual && displayedProperties.value.length > VIRTUAL_SCROLL_THRESHOLD
})

/* 方法 */
// 工具：是否已选择区域（suburb/postcode）

const handleSearch = () => {
  // 搜索逻辑已在SearchBar组件中处理，这里主要是响应搜索事件
}

const handleLocationSelected = async () => {
  try {
    const hasSel =
      Array.isArray(propertiesStore.selectedLocations) &&
      propertiesStore.selectedLocations.length > 0

    if (hasSel) {
      // 统一走 applyFilters：内部会用 selectedLocations 构造并保存 currentFilterParams，保证翻页/改每页大小不丢条件
      await propertiesStore.applyFilters({})
    } else {
      // 无选区：重置筛选并回到无筛选列表（同时清空 currentFilterParams，保持行为一致）
      await propertiesStore.resetFilters()
    }
  } catch (error) {
    console.error('筛选房源失败:', error)
  }
}

const handleOpenFilterPanel = () => {
  // 仅移动端打开统一 FilterPanel；PC 端采用分离式下拉面板（FilterTabs 内部处理）
  if (windowWidth.value > 768) return
  focusSection.value = null
  showFilterPanel.value = true
}

const handleFiltersChanged = () => {
  // 筛选逻辑已在FilterPanel组件中处理
}

const handlePageChange = async (page) => {
  await propertiesStore.setCurrentPage(page)

  // 滚动到顶部
  window.scrollTo({
    top: 0,
    behavior: 'smooth',
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
  // 从 URL 恢复排序（URL 状态同步）：存在 sort 时恢复并触发服务端排序透传
  const sortQ = route.query?.sort
  if (typeof sortQ === 'string' && sortQ) {
    sortValue.value = sortQ
    await propertiesStore.setSort(sortQ)
  }

  // 首次加载自动应用：若已存在“已选区域/或URL筛选参数”，自动等效一次“确定”
  try {
    const hasApplied =
      propertiesStore.currentFilterParams &&
      Object.keys(propertiesStore.currentFilterParams).length > 0

    const hasSelections =
      Array.isArray(propertiesStore.selectedLocations) &&
      propertiesStore.selectedLocations.length > 0

    const queryKeys = [
      'suburbs',
      'suburb',
      'postcodes',
      'date_from',
      'date_to',
      'price_min',
      'price_max',
      'bedrooms',
      'isFurnished',
      'bathrooms',
      'parking',
      'include_nearby',
    ]
    const queryHasAny = Object.keys(route.query || {}).some(
      (k) => queryKeys.includes(k) && route.query[k] !== undefined && route.query[k] !== '',
    )

    if (!hasApplied && (hasSelections || queryHasAny)) {
      // 将当前路由参数作为原始 filters 传入（store 内部会做契约映射与清洗）
      const plainFilters = { ...(route.query || {}) }
      await propertiesStore.applyFilters(plainFilters)
    } else {
      // 无可用上下文时才加载“无筛选”列表，避免覆盖筛选结果
      if (propertiesStore.filteredProperties.length === 0) {
        loadProperties()
      }
    }
  } catch (e) {
    // 兜底：若自动应用失败，不阻断页面
    console.warn('auto-apply on first load failed (ignored):', e)
    if (propertiesStore.filteredProperties.length === 0) {
      loadProperties()
    }
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

@media (width >= 769px) {
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

@media (width >= 768px) {
  .container {
    padding: 32px;
  }
}

@media (width >= 1024px) {
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

@media (width >= 768px) {
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
  box-shadow: 0 2px 8px rgb(0 0 0 / 6%);
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
  box-shadow: 0 4px 12px rgb(0 0 0 / 10%);
  transition: top 0.2s ease-in-out;
}

/* 当导航栏隐藏时，搜索栏贴顶 */
@media (width >= 769px) {
  .search-filter-section.is-fixed.nav-hidden {
    top: 0;
  }
}

/* 移动端搜索栏始终贴顶 */
@media (width <= 768px) {
  .search-filter-section.is-fixed {
    top: 0;
  }
}

/* 布局偏移补偿 */
.search-bar-spacer {
  width: 100%;
}

/* 移动端Logo区域
   中文注释：用“一层控高 + 一层水平留白”的结构，避免多层 padding 叠加导致总高失控 */
.mobile-logo-section {
  height: var(--nav-h-mob, 54px); /* 目标总高度=54px */
  padding-block: 0;               /* 垂直高度由容器控制，禁止再叠加上下padding */
  position: relative;
  display: flex;
  align-items: center;
  justify-content: flex-start;    /* 水平靠左 */
  background: var(--color-bg-card);              /* 纯白背景 */
  border-bottom: 1px solid var(--color-border-default); /* 底部分隔线 */
}

/* 仅在 LOGO 顶栏内部，移除通用 .container 的上下内边距，保留左右留白 */
.mobile-logo-section > .container {
  padding-top: 0;
  padding-bottom: 0;
  margin-left: 0;   /* 靠左贴齐，保留左右 padding 16px */
  margin-right: auto;
}

.mobile-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 20px;
  font-weight: 700;                    /* 粗体 */
  color: var(--color-text-primary);    /* 黑色（主文案色） */
}


/* 在桌面端隐藏移动端Logo */
@media (width >= 769px) {
  .mobile-logo-section {
    display: none;
  }
}

.search-content-container {
  /* 搜索内容居中对齐容器 */
  max-width: 1200px;
  margin: 0 auto;
  padding: 16px 32px 12px; /* 减少上下padding */
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

/* 桌面端筛选按钮（与行内控件间距一致） */
.filter-trigger-btn {
  display: none;
  align-items: center;
  justify-content: center;
  height: 34px;
  padding: 0 12px; /* 更紧凑的药丸尺寸 */
  gap: 2px; /* 图标与文字更紧凑 */
  border: 1px solid var(--color-border-default);
  border-radius: 9999px; /* 强制药丸型 */
  background: #fff;
  color: var(--color-text-secondary);
  font-weight: 500;
  font-size: 13px;
  line-height: 1; /* 垂直居中更稳 */
}

.filter-trigger-btn:hover {
  border-color: var(--color-border-strong);
  color: var(--color-text-primary);
  background: #f7f8fa;
}

.filter-trigger-btn:focus {
  outline: none; /* 去除浏览器默认 focus ring */
  box-shadow: none;
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

/* 标题区（面包屑/H1/操作行）——对齐参考站 390 规格 */
.title-block {
  padding-top: 8px;
}

.breadcrumbs {
  font-size: 12px;
  color: var(--color-text-secondary);
  margin-bottom: 10px;
}

.page-h1 {
  font-size: 22px;
  line-height: 26px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 14px;
}

.actions-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.alert-left {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--color-text-secondary);
}

.alert-left .label {
  font-weight: 500;
}

.sort-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--color-text-secondary);
  background: transparent;
  border: 0;
  padding: 8px 0;
}

.sort-btn .label {
  font-weight: 600;
}

/* 移动端下保持点击区可达性 */
@media (width <= 768px) {
  .actions-row {
    gap: 10px;
  }
}

/* 移动端布局调整 */
@media (width <= 768px) {
  .container {
    padding: 12px 16px;
  } /* 统一移动端左右 16px，与卡片内容区一致 */
  .search-filter-section {
    margin-bottom: 12px; /* 进一步减少移动端间距 */
  }

  .search-content-container {
    padding: 12px 16px 8px; /* 与卡片内容区(16px)左右对齐 */
  }

  .search-filter-row {
    flex-direction: row; /* 移动端与搜索框同排 */
    align-items: center;
    gap: 8px;
  }

  .search-bar {
    width: 100%;
    flex: 1;
  }

  .filter-tabs-right {
    display: inline-flex; /* 移动端显示 FilterTabs 组件（内部会自动切换为“筛选”按钮） */
  }

  .filter-trigger-btn {
    display: inline-flex; /* 仅移动端显示按钮 */
    height: 34px;
    padding: 0 12px; /* 更紧凑但可点击 */
    border-radius: 9999px;
    gap: 2px;
    font-size: 13px;
    line-height: 1;
    margin-right: 3px; /* 对齐卡片“···”右缘（按钮右侧退 3px） */
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
@media (width <= 767px) {
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
    display: inline-flex;
    width: auto;
    height: 34px;
    padding: 0 12px; /* 与上方断点一致 */
    border-radius: 9999px;
    gap: 2px;
    font-size: 13px;
    line-height: 1;
  }
}

/* 统一图标语义色（错误/空状态），改用设计令牌，避免内联硬编码 */
.error-message .el-icon.error-icon {
  color: var(--color-danger);
}

.empty-state .el-icon.empty-icon {
  color: var(--color-border-default);
}

/* 标题区与卡片右缘对齐（单列卡片场景）：
   让 actions-row 使用与卡片一致的内容宽度，并以左侧为锚点 */
@media (width >= 1024px) {
  /* 始终让标题区操作行与卡片内容宽度一致（PC 断点） */
  .title-block .actions-row {
    width: var(--card-content-w);
  }
}
</style>
