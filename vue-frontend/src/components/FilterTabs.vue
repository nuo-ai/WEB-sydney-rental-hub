<template>
  <!-- 顶部筛选标签栏 - PC模式分离式面板 -->
  <div v-if="!isMobile" class="filter-tabs-container">
    <div class="filter-tabs">
      <!-- 区域 -->
      <div class="filter-tab-entry">
        <button
          ref="areaTabRef"
          class="filter-tab"
          :class="{ active: activePanel === 'area' }"
          @click.stop="togglePanel('area', $event)"
        >
          <span class="chinese-text">区域</span>
          <svg v-if="activePanel !== 'area'" class="chevron-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none">
            <path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <svg v-else class="chevron-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none">
            <path d="M18 15l-6-6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <FilterDropdown
          :modelValue="activePanel === 'area'"
          @update:modelValue="val => !val && (activePanel = null)"
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
          :class="{ active: activePanel === 'bedrooms' }"
          @click.stop="togglePanel('bedrooms', $event)"
        >
          <span class="chinese-text">卧室</span>
          <svg v-if="activePanel !== 'bedrooms'" class="chevron-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none">
            <path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <svg v-else class="chevron-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none">
            <path d="M18 15l-6-6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <FilterDropdown
          :modelValue="activePanel === 'bedrooms'"
          @update:modelValue="val => !val && (activePanel = null)"
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
          :class="{ active: activePanel === 'price' }"
          @click.stop="togglePanel('price', $event)"
        >
          <span class="chinese-text">价格</span>
          <svg v-if="activePanel !== 'price'" class="chevron-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none">
            <path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <svg v-else class="chevron-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none">
            <path d="M18 15l-6-6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <FilterDropdown
          :modelValue="activePanel === 'price'"
          @update:modelValue="val => !val && (activePanel = null)"
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
          :class="{ active: activePanel === 'availability' }"
          @click.stop="togglePanel('availability', $event)"
        >
          <span class="chinese-text">空出时间</span>
          <svg v-if="activePanel !== 'availability'" class="chevron-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none">
            <path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <svg v-else class="chevron-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none">
            <path d="M18 15l-6-6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <FilterDropdown
          :modelValue="activePanel === 'availability'"
          @update:modelValue="val => !val && (activePanel = null)"
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
          :class="{ active: activePanel === 'more' }"
          @click.stop="togglePanel('more', $event)"
        >
          <span class="chinese-text">更多</span>
          <svg v-if="activePanel !== 'more'" class="chevron-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none">
            <path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <svg v-else class="chevron-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none">
            <path d="M18 15l-6-6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <FilterDropdown
          :modelValue="activePanel === 'more'"
          @update:modelValue="val => !val && (activePanel = null)"
          :trigger="moreTabRef"
          :explicit-position="positions.more"
          @close="activePanel = null"
        >
          <div class="more-filter-placeholder">
            <p>更多筛选选项</p>
          </div>
        </FilterDropdown>
      </div>
    </div>
  </div>

  <!-- 移动端触发统一面板的按钮 -->
  <div v-else class="filter-tabs-mobile">
    <button class="filter-button" @click="$emit('requestOpenFullPanel')">
      <svg class="filter-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none">
        <path d="M3 4h18M3 12h18M3 20h18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      </svg>
      <span>筛选</span>
    </button>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import FilterDropdown from './FilterDropdown.vue'
import AreaFilterPanel from './filter-panels/AreaFilterPanel.vue'
import BedroomsFilterPanel from './filter-panels/BedroomsFilterPanel.vue'
import PriceFilterPanel from './filter-panels/PriceFilterPanel.vue'
import AvailabilityFilterPanel from './filter-panels/AvailabilityFilterPanel.vue'

// 中文注释：PC端改为分离式下拉面板，移动端保持统一大面板
// 使用 requestOpenFullPanel 事件触发移动端的统一面板

// 定义事件（在模板中通过 $emit 使用）
// eslint-disable-next-line no-unused-vars
const emit = defineEmits(['requestOpenFullPanel'])

// 响应式状态
const activePanel = ref(null) // 'area', 'bedrooms', 'price', 'availability', 'more' 或 null

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
    case 'area': return areaTabRef
    case 'bedrooms': return bedroomsTabRef
    case 'price': return priceTabRef
    case 'availability': return availabilityTabRef
    case 'more': return moreTabRef
    default: return null
  }
}

// 中文注释：从触发元素计算显式定位（fixed 参考视口坐标）
const computePosition = (el) => {
  if (!el) return null
  const rect = el.getBoundingClientRect()
  const vw = window.innerWidth
  const width = Math.max(rect.width, 280)
  let left = rect.left
  // 边缘保护：左右至少 10px 余量
  if (left + width > vw - 10) left = Math.max(10, vw - width - 10)
  if (left < 10) left = 10
  const top = rect.bottom + 8
  return { top, left, width }
}

// 移动端判断
const isMobile = computed(() => {
  return typeof window !== 'undefined' ? window.innerWidth < 768 : false
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
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
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
@media (min-width: 769px) {
  .filter-tabs-container {
    max-width: none;
  }
  .filter-tabs {
    justify-content: flex-start; /* 紧邻搜索框 */
    flex-wrap: wrap;
  }
}

/* 移动端保持原有流式排列 */
@media (max-width: 768px) {
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
  background: var(--chip-bg, #f7f8fa);
  border: none;
  border-radius: 0;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: background-color 0.2s ease, color 0.2s ease;
  white-space: nowrap;
}

.filter-tab:hover {
  background: var(--chip-bg-hover, #eef1f4);
  color: var(--color-text-primary);
}

/* 激活状态样式 */
.filter-tab.active {
  background: #ffefe9; /* 极弱浅橙，非品牌强底色 */
  border-color: var(--color-border-strong);
  color: var(--color-text-primary);
}

/* 箭头图标 */
.chevron-icon {
  width: 16px;
  height: 16px;
  color: currentColor;
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
  border-radius: 9999px;
  background: #fff;
  color: var(--color-text-secondary);
  font-weight: 500;
  font-size: 13px;
  line-height: 1;
}

.filter-button:hover {
  border-color: var(--color-border-strong);
  color: var(--color-text-primary);
  background: #f7f8fa;
}

.filter-icon {
  width: 16px;
  height: 16px;
}

/* 更多筛选面板占位 */
.more-filter-placeholder {
  width: 280px;
  padding: 20px;
  text-align: center;
  color: var(--color-text-secondary);
}
</style>
