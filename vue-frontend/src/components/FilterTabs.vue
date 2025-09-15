<template>
  <!-- 顶部筛选标签栏 - PC模式分离式面板 -->
  <div v-if="!isMobile" class="filter-tabs-container">
    <div class="filter-tabs">
      <!-- 区域 -->
      <div class="filter-tab-entry">
        <button
          ref="areaTabRef"
          class="filter-tab"
          :class="{ active: activePanel === 'area', applied: areaApplied }"
          @click.stop="togglePanel('area', $event)"
        >
          <span class="chinese-text">{{ areaTabText }}</span>
          <svg
            v-if="activePanel !== 'area'"
            class="chevron-icon"
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
          >
            <path
              d="M6 9l6 6 6-6"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
          <svg
            v-else
            class="chevron-icon"
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
          >
            <path
              d="M18 15l-6-6-6 6"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </button>
        <FilterDropdown
          :modelValue="activePanel === 'area'"
          @update:modelValue="(val) => !val && (activePanel = null)"
          :trigger="areaTabRef"
          :explicit-position="positions.area"
          @close="activePanel = null"
        >
          <AreaFilterPanel @close="activePanel = null" />
        </FilterDropdown>
      </div>

      <!-- 卧室 -->
      <div class="filter-tab-entry">
        <button
          ref="bedroomsTabRef"
          class="filter-tab"
          :class="{ active: activePanel === 'bedrooms', applied: bedroomsApplied }"
          @click.stop="togglePanel('bedrooms', $event)"
        >
          <span class="chinese-text">{{ bedroomsTabText }}</span>
          <svg
            v-if="activePanel !== 'bedrooms'"
            class="chevron-icon"
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
          >
            <path
              d="M6 9l6 6 6-6"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
          <svg
            v-else
            class="chevron-icon"
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
          >
            <path
              d="M18 15l-6-6-6 6"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </button>
        <FilterDropdown
          :modelValue="activePanel === 'bedrooms'"
          @update:modelValue="(val) => !val && (activePanel = null)"
          :trigger="bedroomsTabRef"
          :explicit-position="positions.bedrooms"
          @close="activePanel = null"
        >
          <BedroomsFilterPanel @close="activePanel = null" />
        </FilterDropdown>
      </div>

      <!-- 价格 -->
      <div class="filter-tab-entry">
        <button
          ref="priceTabRef"
          class="filter-tab"
          :class="{ active: activePanel === 'price', applied: priceApplied }"
          @click.stop="togglePanel('price', $event)"
        >
          <span class="chinese-text">{{ priceTabText }}</span>
          <svg
            v-if="activePanel !== 'price'"
            class="chevron-icon"
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
          >
            <path
              d="M6 9l6 6 6-6"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
          <svg
            v-else
            class="chevron-icon"
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
          >
            <path
              d="M18 15l-6-6-6 6"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </button>
        <FilterDropdown
          :modelValue="activePanel === 'price'"
          @update:modelValue="(val) => !val && (activePanel = null)"
          :trigger="priceTabRef"
          :explicit-position="positions.price"
          @close="activePanel = null"
        >
          <PriceFilterPanel @close="activePanel = null" />
        </FilterDropdown>
      </div>

      <!-- 空出时间 -->
      <div class="filter-tab-entry">
        <button
          ref="availabilityTabRef"
          class="filter-tab"
          :class="{ active: activePanel === 'availability', applied: availabilityApplied }"
          @click.stop="togglePanel('availability', $event)"
        >
          <span class="chinese-text">{{ availabilityTabText }}</span>
          <svg
            v-if="activePanel !== 'availability'"
            class="chevron-icon"
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
          >
            <path
              d="M6 9l6 6 6-6"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
          <svg
            v-else
            class="chevron-icon"
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
          >
            <path
              d="M18 15l-6-6-6 6"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </button>
        <FilterDropdown
          :modelValue="activePanel === 'availability'"
          @update:modelValue="(val) => !val && (activePanel = null)"
          :trigger="availabilityTabRef"
          :explicit-position="positions.availability"
          @close="activePanel = null"
        >
          <AvailabilityFilterPanel @close="activePanel = null" />
        </FilterDropdown>
      </div>

      <!-- 更多（高级筛选） -->
      <div class="filter-tab-entry">
        <button
          ref="moreTabRef"
          class="filter-tab"
          :class="{ active: activePanel === 'more', applied: moreApplied }"
          @click.stop="togglePanel('more', $event)"
        >
          <span class="chinese-text">{{ moreTabText }}</span>
          <svg
            v-if="activePanel !== 'more'"
            class="chevron-icon"
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
          >
            <path
              d="M6 9l6 6 6-6"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
          <svg
            v-else
            class="chevron-icon"
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
          >
            <path
              d="M18 15l-6-6-6 6"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </button>
        <FilterDropdown
          :modelValue="activePanel === 'more'"
          @update:modelValue="(val) => !val && (activePanel = null)"
          :trigger="moreTabRef"
          :explicit-position="positions.more"
          @close="activePanel = null"
        >
          <MoreFilterPanel @close="activePanel = null" />
        </FilterDropdown>
      </div>

      <!-- 保存搜索按钮 -->
      <div class="save-search-section">
        <button
          class="save-search-btn"
          :class="{ disabled: !hasActiveFilters }"
          :disabled="!hasActiveFilters"
          @click="handleSaveSearch"
        >
          <svg
            class="save-icon"
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
          >
            <path
              d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
          <span>保存搜索</span>
        </button>
      </div>
    </div>
  </div>

  <!-- 移动端触发统一面板的按钮 -->
  <div v-else class="filter-tabs-mobile">
    <button class="filter-button" @click="$emit('requestOpenFullPanel')">
      <svg
        class="filter-icon"
        xmlns="http://www.w3.org/2000/svg"
        width="16"
        height="16"
        viewBox="0 0 24 24"
        fill="none"
      >
        <path
          d="M3 4h18M3 12h18M3 20h18"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
        />
      </svg>
      <span>筛选</span>
    </button>

    <!-- 移动端保存搜索按钮 -->
    <button
      class="save-search-btn-mobile"
      :class="{ disabled: !hasActiveFilters }"
      :disabled="!hasActiveFilters"
      @click="handleSaveSearch"
    >
      <svg
        class="save-icon"
        xmlns="http://www.w3.org/2000/svg"
        width="16"
        height="16"
        viewBox="0 0 24 24"
        fill="none"
      >
        <path
          d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
      <span>保存</span>
    </button>
  </div>

  <!-- 保存搜索弹窗 -->
  <SaveSearchModal
    v-model="showSaveModal"
    :filter-conditions="currentFilterConditions"
    @saved="handleSearchSaved"
  />
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import FilterDropdown from './FilterDropdown.vue'
import AreaFilterPanel from './filter-panels/AreaFilterPanel.vue'
import BedroomsFilterPanel from './filter-panels/BedroomsFilterPanel.vue'
import PriceFilterPanel from './filter-panels/PriceFilterPanel.vue'
import AvailabilityFilterPanel from './filter-panels/AvailabilityFilterPanel.vue'
import MoreFilterPanel from './filter-panels/MoreFilterPanel.vue'
import SaveSearchModal from './SaveSearchModal.vue'
import { usePropertiesStore } from '@/stores/properties'

// 中文注释：PC端改为分离式下拉面板，移动端保持统一大面板
// 使用 requestOpenFullPanel 事件触发移动端的统一面板

// 定义事件（在模板中通过 $emit 使用）
// eslint-disable-next-line no-unused-vars
const emit = defineEmits(['requestOpenFullPanel', 'searchSaved'])

// 响应式状态
const activePanel = ref(null) // 'area', 'bedrooms', 'price', 'availability', 'more' 或 null

// 依赖 Store 的“已应用参数 + 草稿”用于顶部标签文案与小蓝点
const propertiesStore = usePropertiesStore()
const appliedParams = computed(() => propertiesStore.currentFilterParams || {})

/* 移除未应用变更小蓝点相关计算，保留 applied 文案与高亮 */

// 1) 区域
const areaApplied = computed(() => (propertiesStore.selectedLocations?.length || 0) > 0)
/* removed: areaHasDraft */
const areaTabText = computed(() => {
  const list = propertiesStore.selectedLocations || []
  if (!list.length) return '区域'
  const names = list.map((l) => (l?.name ? String(l.name) : '')).filter(Boolean)
  if (!names.length) return '区域'
  const first = names[0]
  const more = Math.max(0, names.length - 1)
  return more > 0 ? `${first} +${more}` : first
})

// 2) 卧室
const bedroomsApplied = computed(() => {
  const v = appliedParams.value?.bedrooms
  return v !== undefined && v !== null && String(v) !== ''
})
/* removed: bedroomsHasDraft */
const bedroomsTabText = computed(() => {
  if (!bedroomsApplied.value) return '卧室'
  const v = String(appliedParams.value?.bedrooms)
  if (v === '0' || v.toLowerCase() === 'studio') return 'Studio'
  return v.endsWith('+') ? `${v}卧` : `${v}卧`
})

// 3) 价格
const priceApplied = computed(() => {
  const p = appliedParams.value || {}
  const min = p.minPrice ?? p.price_min
  const max = p.maxPrice ?? p.price_max
  return (min != null && min !== '') || (max != null && max !== '')
})
/* removed: priceHasDraft */
const priceTabText = computed(() => {
  const p = appliedParams.value || {}
  const min = p.minPrice ?? p.price_min
  const max = p.maxPrice ?? p.price_max
  const minNum = min != null && min !== '' ? Number(min) : null
  const maxNum = max != null && max !== '' ? Number(max) : null
  if (minNum == null && maxNum == null) return '价格'
  if (minNum != null && maxNum != null) return `$${minNum} - $${maxNum}`
  if (minNum != null) return `≥$${minNum}`
  return `≤$${maxNum}`
})

// 4) 空出时间
const availabilityApplied = computed(() => {
  const p = appliedParams.value || {}
  return (p.date_from && String(p.date_from) !== '') || (p.date_to && String(p.date_to) !== '')
})
/* removed: availabilityHasDraft */
const availabilityTabText = computed(() => {
  const p = appliedParams.value || {}
  const from = p.date_from ? String(p.date_from).slice(0, 10) : null
  const to = p.date_to ? String(p.date_to).slice(0, 10) : null
  if (from && to) return `${from} - ${to}`
  if (from) return `From ${from}`
  if (to) return `Until ${to}`
  return '空出时间'
})

// 5) 更多
const moreApplied = computed(() => {
  const p = appliedParams.value || {}
  // 中文注释：与当前 UI 对齐——“更多”仅体现带家具 Furnished，浴室/车位归“卧室”面板管理
  return p.isFurnished === true || p.furnished === true
})
/* removed: moreHasDraft */
const moreTabText = computed(() => {
  const p = appliedParams.value || {}
  // 中文注释：仅在 Furnished 为 true 时显示；否则显示“更多”
  if (p.isFurnished === true || p.furnished === true) return 'Furnished'
  return '更多'
})

// 面板触发元素引用
const areaTabRef = ref(null)
const bedroomsTabRef = ref(null)
const priceTabRef = ref(null)
const availabilityTabRef = ref(null)
const moreTabRef = ref(null)

// 中文注释：显式坐标（由触发按钮计算），用于避免 ref/布局时序造成的 0,0 定位
const positions = reactive({
  area: null,
  bedrooms: null,
  price: null,
  availability: null,
  more: null,
})

const getRef = (panel) => {
  switch (panel) {
    case 'area':
      return areaTabRef
    case 'bedrooms':
      return bedroomsTabRef
    case 'price':
      return priceTabRef
    case 'availability':
      return availabilityTabRef
    case 'more':
      return moreTabRef
    default:
      return null
  }
}

// 中文注释：从触发元素计算显式定位（fixed 参考视口坐标）
const computePosition = (el) => {
  if (!el) return null
  const rect = el.getBoundingClientRect()
  const vw = window.innerWidth
  // 中文注释：PC 下所有面板统一宽度 380；移动端保持至少与触发等宽
  const desktop = typeof window !== 'undefined' ? window.innerWidth >= 768 : true
  const width = desktop ? 380 : Math.max(rect.width, 280)
  let left = rect.left
  // 边缘保护：左右至少 10px 余量
  if (left + width > vw - 10) left = Math.max(10, vw - width - 10)
  if (left < 10) left = 10
  const top = rect.bottom + 8
  return { top, left, width }
}

// 移动端判断
const viewportWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 1024)
const isMobile = computed(() => {
  return viewportWidth.value < 768
})

// 切换面板显示状态
const togglePanel = (panel, evt) => {
  const wasOpen = activePanel.value === panel
  activePanel.value = wasOpen ? null : panel
  // 中文注释：优先使用事件的 currentTarget；退化到已保存的 ref
  const el = (evt && evt.currentTarget) || getRef(panel)?.value
  positions[panel] = computePosition(el)
}

// 全局事件处理
const handleResize = () => {
  // 同步视口宽度为响应式依赖，驱动 isMobile 重新计算
  if (typeof window !== 'undefined') {
    viewportWidth.value = window.innerWidth
  }
  // 当切换到移动端视图时，自动关闭任何打开的面板
  if (isMobile.value && activePanel.value) {
    activePanel.value = null
    return
  }
  // PC 场景：若有面板打开，随窗口变化重新计算显式定位
  if (activePanel.value) {
    const el = getRef(activePanel.value)?.value
    positions[activePanel.value] = computePosition(el)
  }
}

// 生命周期钩子
onMounted(() => {
  // 中文注释：组件挂载时即同步一次视口宽度，避免 SSR/初始值造成的断点误判
  if (typeof window !== 'undefined') {
    viewportWidth.value = window.innerWidth
  }
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})

// 保存搜索相关状态
const showSaveModal = ref(false)

// 检查是否有活跃的筛选条件
const hasActiveFilters = computed(() => {
  return areaApplied.value ||
         bedroomsApplied.value ||
         priceApplied.value ||
         availabilityApplied.value ||
         moreApplied.value
})

// 构建当前筛选条件对象
const currentFilterConditions = computed(() => {
  const conditions = {}

  // 从 appliedParams 获取当前筛选条件
  const params = appliedParams.value || {}

  // 房型
  if (params.bedrooms) {
    conditions.bedrooms = params.bedrooms
  }

  // 价格范围
  const minPrice = params.minPrice ?? params.price_min
  const maxPrice = params.maxPrice ?? params.price_max
  if (minPrice != null || maxPrice != null) {
    conditions.priceRange = [
      minPrice != null ? Number(minPrice) : 0,
      maxPrice != null ? Number(maxPrice) : 5000
    ]
  }

  // 浴室
  if (params.bathrooms) {
    conditions.bathrooms = params.bathrooms
  }

  // 车位
  if (params.parking) {
    conditions.parking = params.parking
  }

  // 家具
  if (params.isFurnished === true || params.furnished === true) {
    conditions.furnished = true
  }

  // 日期
  if (params.date_from) {
    conditions.dateFrom = new Date(params.date_from)
  }
  if (params.date_to) {
    conditions.dateTo = new Date(params.date_to)
  }

  return conditions
})

// 处理保存搜索按钮点击
const handleSaveSearch = () => {
  if (!hasActiveFilters.value) return
  showSaveModal.value = true
}

// 处理搜索保存成功
const handleSearchSaved = async (savedSearch) => {
  try {
    // 保存成功后，应用筛选并刷新页面
    await propertiesStore.applyFilters(appliedParams.value)

    // 向父组件发射事件
    emit('searchSaved', savedSearch)

    console.log('搜索已保存并应用！', savedSearch)

  } catch (error) {
    console.error('应用筛选失败:', error)
  }
}
</script>

<style scoped>
/* 顶部筛选标签栏 */
.filter-tabs-container {
  position: relative;
  width: 100%;
  margin-bottom: 0;
}

.filter-tabs {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap; /* PC端允许换行 */
  padding: 0;
  height: 48px; /* 与搜索框高度一致 */
}

/* PC端右侧布局时的样式调整 */
@media (width >= 769px) {
  .filter-tabs-container {
    max-width: none;
  }

  .filter-tabs {
    justify-content: flex-start; /* 紧邻搜索框 */
    flex-wrap: wrap;
  }
}

/* 移动端保持原有流式排列 */
@media (width <= 768px) {
  .filter-tabs-container {
    width: 100%;
    max-width: 100%;
    margin-bottom: 16px;
    padding: 0 16px;
    box-sizing: border-box;
  }

  .filter-tabs {
    flex-wrap: nowrap;
    overflow-x: auto;
    padding-bottom: 4px; /* 为滚动条留空间 */
  }
}

.filter-tabs::-webkit-scrollbar {
  display: none;
}

/* 单个入口 */
.filter-tab-entry {
  position: relative;
}

/* 筛选标签按钮（保持与现有 token 一致） */
.filter-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: var(--chip-bg);
  border: none;
  border-radius: 0;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
  cursor: pointer;
  transition:
    background-color 0.2s ease,
    color 0.2s ease;
  white-space: nowrap;
  position: relative; /* 为小蓝点定位 */
}

.filter-tab:hover {
  background: var(--chip-bg-hover);
  color: var(--color-text-primary);
}

/* 激活状态样式 */
.filter-tab.active {
  background: var(--chip-bg-selected); /* 中文注释：激活态统一为中性 chips 选中底色 */
  color: var(--color-text-primary);
}

/* 箭头图标 */
.chevron-icon {
  width: 16px;
  height: 16px;
  color: currentcolor;
}

/* 移动端筛选按钮 */
.filter-tabs-mobile {
  display: flex;
  justify-content: flex-end;
}

.filter-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 34px;
  padding: 0 12px;
  gap: 2px;
  border: 1px solid var(--color-border-default);
  border-radius: var(--filter-radius-lg);
  background: var(--color-bg-card);
  color: var(--color-text-secondary);
  font-weight: 500;
  font-size: 13px;
  line-height: 1;
}

.filter-button:hover {
  border-color: var(--color-border-strong);
  color: var(--color-text-primary);
  background: var(--bg-hover);
}

.filter-icon {
  width: 16px;
  height: 16px;
}

/* 已应用高亮（严格使用 design token，与 active 保持一致风格） */
.filter-tab.applied {
  background: var(--chip-bg-selected);
  color: var(--color-text-primary);
}

/* 移除小蓝点样式 */

/* 保存搜索按钮样式 */
.save-search-section {
  margin-left: 16px;
}

.save-search-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 40px;
  padding: 0 16px;
  gap: 8px;
  border: none;
  border-radius: 8px;
  background: var(--juwo-primary);
  color: white;
  font-weight: 600;
  font-size: 14px;
  line-height: 1;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.save-search-btn:hover:not(:disabled) {
  background: var(--juwo-primary-light);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.save-search-btn:disabled,
.save-search-btn.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: var(--color-border-default);
  color: var(--color-text-secondary);
}

.save-search-btn:disabled:hover,
.save-search-btn.disabled:hover {
  transform: none;
  box-shadow: none;
}

.save-icon {
  width: 16px;
  height: 16px;
  stroke: currentColor;
}

/* 移动端保存搜索按钮 */
.filter-tabs-mobile {
  gap: 8px;
}

.save-search-btn-mobile {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 34px;
  padding: 0 12px;
  gap: 6px;
  border: 1px solid var(--juwo-primary);
  border-radius: var(--filter-radius-lg);
  background: var(--juwo-primary);
  color: white;
  font-weight: 600;
  font-size: 13px;
  line-height: 1;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.save-search-btn-mobile:hover:not(:disabled) {
  background: var(--juwo-primary-light);
  border-color: var(--juwo-primary-light);
}

.save-search-btn-mobile:disabled,
.save-search-btn-mobile.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: var(--color-border-default);
  border-color: var(--color-border-default);
  color: var(--color-text-secondary);
}

/* 更多筛选面板占位 */
.more-filter-placeholder {
  width: 280px;
  padding: 20px;
  text-align: center;
  color: var(--color-text-secondary);
}

/* PC端保存搜索按钮在筛选按钮右侧的布局调整 */
@media (width >= 769px) {
  .filter-tabs {
    align-items: center;
  }

  .save-search-section {
    margin-left: auto;
    padding-left: 16px;
  }
}

/* 移动端布局调整 */
@media (width <= 768px) {
  .filter-tabs-mobile {
    justify-content: space-between;
    width: 100%;
  }

  .save-search-btn-mobile {
    flex-shrink: 0;
  }
}
</style>
