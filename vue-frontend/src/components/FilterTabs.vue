<template>
  <!-- Domain风格顶部筛选标签栏 -->
  <div class="filter-tabs-container">
    <div class="filter-tabs">
      <!-- 筛选标签 - 打开完整筛选面板 -->
      <button 
        class="filter-tab"
        :class="{ 'active': props.filterPanelOpen }"
        @click="toggleFullPanel"
      >
        <i class="fa-solid fa-sliders"></i>
        <span class="chinese-text">筛选</span>
      </button>

      <!-- 区域标签 - 快速区域选择 -->
      <div class="filter-tab-dropdown" :class="{ 'active': activeDropdown === 'area' }">
        <button 
          class="filter-tab"
          @click.stop="toggleDropdown('area')"
        >
          <span class="chinese-text">区域</span>
          <i class="fa-solid fa-chevron-down"></i>
          <span v-if="selectedAreas.length > 0" class="filter-badge">{{ selectedAreas.length }}</span>
        </button>
        
        <!-- 区域快速选择下拉 -->
        <div v-if="activeDropdown === 'area'" class="quick-filter-dropdown">
          <div class="dropdown-header chinese-text">选择区域</div>
          <div class="area-options">
            <label v-for="area in popularAreas" :key="area.value" class="area-option">
              <input 
                type="checkbox" 
                :value="area.value"
                :checked="selectedAreas.includes(area.value)"
                @click="toggleArea(area.value)"
              >
              <span>{{ area.label }}</span>
            </label>
          </div>
        </div>
      </div>

      <!-- 卧室标签 - 快速卧室选择 -->
      <div class="filter-tab-dropdown" :class="{ 'active': activeDropdown === 'bedrooms' }">
        <button 
          class="filter-tab"
          @click.stop="toggleDropdown('bedrooms')"
        >
          <span class="chinese-text">卧室</span>
          <i class="fa-solid fa-chevron-down"></i>
          <span v-if="selectedBedrooms.length > 0" class="filter-badge">{{ selectedBedrooms.length }}</span>
        </button>
        
        <!-- 卧室快速选择下拉 -->
        <div v-if="activeDropdown === 'bedrooms'" class="quick-filter-dropdown">
          <div class="dropdown-header chinese-text">卧室数量</div>
          <div class="bedroom-options">
            <button 
              v-for="option in bedroomOptions" 
              :key="option.value"
              class="option-btn"
              :class="{ 'selected': selectedBedrooms.includes(option.value) }"
              @click="toggleBedroom(option.value)"
            >
              {{ option.label }}
            </button>
          </div>
        </div>
      </div>

      <!-- 价格标签 - 快速价格选择 -->
      <div class="filter-tab-dropdown" :class="{ 'active': activeDropdown === 'price' }">
        <button 
          class="filter-tab"
          @click.stop="toggleDropdown('price')"
        >
          <span class="chinese-text">价格</span>
          <i class="fa-solid fa-chevron-down"></i>
          <span v-if="priceRangeText !== 'Any Price'" class="filter-badge">1</span>
        </button>
        
        <!-- 价格快速选择下拉 -->
        <div v-if="activeDropdown === 'price'" class="quick-filter-dropdown">
          <div class="dropdown-header chinese-text">价格范围 (周租)</div>
          <div class="price-options">
            <button 
              v-for="range in priceRanges" 
              :key="range.label"
              class="option-btn"
              :class="{ 'selected': isPriceRangeSelected(range) }"
              @click="selectPriceRange(range)"
            >
              {{ range.label }}
            </button>
          </div>
          <!-- 自定义价格范围 -->
          <div class="custom-price">
            <el-slider
              v-model="customPriceRange"
              range
              :min="0"
              :max="5000"
              :step="50"
              class="price-slider-mini"
              @change="updateCustomPrice"
            />
            <div class="price-range-display">
              ${{ customPriceRange[0] }} - ${{ customPriceRange[1] }}
            </div>
          </div>
        </div>
      </div>

      <!-- 空出时间标签 - 快速时间选择 -->
      <div class="filter-tab-dropdown" :class="{ 'active': activeDropdown === 'availability' }">
        <button 
          class="filter-tab"
          @click.stop="toggleDropdown('availability')"
        >
          <span class="chinese-text">空出时间</span>
          <i class="fa-solid fa-chevron-down"></i>
          <span v-if="selectedAvailability !== 'any'" class="filter-badge">1</span>
        </button>
        
        <!-- 空出时间快速选择下拉 -->
        <div v-if="activeDropdown === 'availability'" class="quick-filter-dropdown">
          <div class="dropdown-header chinese-text">入住时间</div>
          <div class="availability-options">
            <button 
              v-for="option in availabilityOptions" 
              :key="option.value"
              class="option-btn"
              :class="{ 'selected': selectedAvailability === option.value }"
              @click="selectAvailability(option.value)"
            >
              {{ option.label }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 点击其他区域关闭下拉 -->
    <div v-if="activeDropdown" class="dropdown-overlay" @click="closeDropdown"></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { usePropertiesStore } from '@/stores/properties'

// 组件props
const props = defineProps({
  filterPanelOpen: {
    type: Boolean,
    default: false
  },
  currentFilters: {
    type: Object,
    default: () => ({})
  }
})

// 组件事件
const emit = defineEmits(['toggleFullPanel', 'filtersChanged'])

// 状态管理
const propertiesStore = usePropertiesStore()

// 响应式数据
const activeDropdown = ref(null)
const selectedAreas = ref([])
const selectedBedrooms = ref(['any'])
const customPriceRange = ref([0, 5000])
const selectedAvailability = ref('any')

// 选项数据
const popularAreas = [
  { value: 'sydney', label: 'Sydney CBD' },
  { value: 'bondi', label: 'Bondi' },
  { value: 'manly', label: 'Manly' },
  { value: 'parramatta', label: 'Parramatta' },
  { value: 'chatswood', label: 'Chatswood' },
  { value: 'newtown', label: 'Newtown' }
]

const bedroomOptions = [
  { value: 'any', label: 'Any' },
  { value: '1', label: '1' },
  { value: '2', label: '2' },
  { value: '3', label: '3' },
  { value: '4+', label: '4+' }
]

const priceRanges = [
  { label: 'Any Price', min: 0, max: 5000 },
  { label: '$0 - $400', min: 0, max: 400 },
  { label: '$400 - $600', min: 400, max: 600 },
  { label: '$600 - $800', min: 600, max: 800 },
  { label: '$800 - $1200', min: 800, max: 1200 },
  { label: '$1200+', min: 1200, max: 5000 }
]

const availabilityOptions = [
  { value: 'any', label: '任何时间' },
  { value: 'immediate', label: '立即入住' },
  { value: 'thisWeek', label: '本周' },
  { value: 'thisMonth', label: '本月' },
  { value: 'nextMonth', label: '下个月' }
]

// 计算属性
const priceRangeText = computed(() => {
  const [min, max] = customPriceRange.value
  if (min === 0 && max === 5000) {
    return 'Any Price'
  } else if (max === 5000) {
    return `$${min}+`
  } else {
    return `$${min} - $${max}`
  }
})

// 方法
const toggleFullPanel = () => {
  closeDropdown()
  emit('toggleFullPanel', !props.filterPanelOpen)
}

const toggleDropdown = (dropdown) => {
  if (activeDropdown.value === dropdown) {
    closeDropdown()
  } else {
    // 确保关闭主筛选面板
    if (props.filterPanelOpen) {
      emit('toggleFullPanel', false)
    }
    activeDropdown.value = dropdown
  }
}

const closeDropdown = () => {
  activeDropdown.value = null
}

const toggleArea = (areaValue) => {
  const index = selectedAreas.value.indexOf(areaValue)
  
  if (index > -1) {
    selectedAreas.value.splice(index, 1)
  } else {
    selectedAreas.value.push(areaValue)
  }
  applyFilters()
}

const toggleBedroom = (value) => {
  if (value === 'any') {
    selectedBedrooms.value = ['any']
  } else {
    const index = selectedBedrooms.value.indexOf(value)
    if (index > -1) {
      selectedBedrooms.value.splice(index, 1)
      // 如果没有选中任何项，设置为'any'
      if (selectedBedrooms.value.length === 0) {
        selectedBedrooms.value = ['any']
      }
    } else {
      // 移除'any'选项，添加具体选项
      selectedBedrooms.value = selectedBedrooms.value.filter(v => v !== 'any')
      selectedBedrooms.value.push(value)
    }
  }
  applyFilters()
}

const isPriceRangeSelected = (range) => {
  return customPriceRange.value[0] === range.min && customPriceRange.value[1] === range.max
}

const selectPriceRange = (range) => {
  customPriceRange.value = [range.min, range.max]
  applyFilters()
}

const updateCustomPrice = () => {
  applyFilters()
}

const selectAvailability = (value) => {
  selectedAvailability.value = value
  applyFilters()
  closeDropdown()
}

const applyFilters = () => {
  const filterParams = {
    areas: selectedAreas.value,
    bedrooms: selectedBedrooms.value.includes('any') ? 'any' : selectedBedrooms.value.join(','),
    minPrice: customPriceRange.value[0] > 0 ? customPriceRange.value[0] : null,
    maxPrice: customPriceRange.value[1] < 5000 ? customPriceRange.value[1] : null,
    availability: selectedAvailability.value
  }
  
  propertiesStore.applyFilters(filterParams)
  emit('filtersChanged', filterParams)
}

// 生命周期
onMounted(() => {
  // 点击外部关闭下拉
  document.addEventListener('click', handleClickOutside)
  
  // 同步初始筛选状态
  if (props.currentFilters) {
    syncFiltersFromPanel(props.currentFilters)
  }
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

const handleClickOutside = (event) => {
  if (!event.target.closest('.filter-tabs-container')) {
    closeDropdown()
  }
}

// 同步来自FilterPanel的筛选状态
const syncFiltersFromPanel = (filters) => {
  if (filters.areas) {
    selectedAreas.value = Array.isArray(filters.areas) ? filters.areas : []
  }
  if (filters.bedrooms) {
    selectedBedrooms.value = filters.bedrooms === 'any' ? ['any'] : filters.bedrooms.split(',')
  }
  if (filters.minPrice !== undefined || filters.maxPrice !== undefined) {
    customPriceRange.value = [
      filters.minPrice || 0,
      filters.maxPrice || 5000
    ]
  }
  if (filters.availability) {
    selectedAvailability.value = filters.availability
  }
}

// 暴露方法给父组件
defineExpose({
  syncFiltersFromPanel
})
</script>

<style scoped>
/* Domain风格筛选标签栏 */
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
  padding: 0; /* 移除padding让对齐更精确 */
  height: 48px; /* 与搜索框高度一致 */
}

/* PC端右侧布局时的样式调整 */
@media (min-width: 769px) {
  .filter-tabs-container {
    max-width: none;
  }
  
  .filter-tabs {
    justify-content: flex-start; /* 紧邻搜索框，不要右对齐 */
    flex-wrap: wrap;
  }
}

/* 移动端保持原有样式 */
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
  
  /* 移动端下拉框调整 */
  .quick-filter-dropdown {
    position: fixed;  /* 移动端使用fixed定位 */
    left: 50%;
    transform: translateX(-50%);
    width: 90%;
    max-width: 340px;
  }
}

.filter-tabs::-webkit-scrollbar {
  display: none;
}

/* 筛选标签按钮 */
.filter-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: white;
  border: 1px solid var(--color-border-default);
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  position: relative;
}

.filter-tab:hover {
  border-color: var(--juwo-primary);
  color: var(--juwo-primary);
  background: var(--juwo-primary-50);
}

.filter-tab.active,
.filter-tab-dropdown.active .filter-tab {
  background: var(--juwo-primary);
  border-color: var(--juwo-primary);
  color: white;
}

.filter-tab i {
  font-size: 12px;
}

/* 筛选状态标识 */
.filter-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: var(--juwo-primary);
  color: white;
  font-size: 10px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 16px;
  text-align: center;
}

.filter-tab.active .filter-badge {
  background: white;
  color: var(--juwo-primary);
}

/* 下拉框容器 */
.filter-tab-dropdown {
  position: relative;
}

/* 快速筛选下拉框 */
.quick-filter-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  background: white;
  border: 1px solid var(--color-border-default);
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  z-index: 10001;  /* 提高z-index以确保在FilterPanel之上 */
  min-width: 220px;
  max-width: 280px;
  padding: 16px;
  margin-top: 4px;
  pointer-events: auto;  /* 确保可以接收点击事件 */
}

.dropdown-header {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 12px;
}

/* 区域选项 */
.area-options {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.area-option {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.area-option:hover {
  background: var(--juwo-primary-50);
}

.area-option input[type="checkbox"] {
  margin: 0;
}

/* 选项按钮 */
.bedroom-options,
.availability-options {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.price-options {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 16px;
}

.option-btn {
  padding: 8px 12px;
  border: 1px solid var(--color-border-default);
  border-radius: 6px;
  background: white;
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.option-btn:hover {
  border-color: var(--juwo-primary);
  color: var(--juwo-primary);
  background: var(--juwo-primary-50);
}

.option-btn.selected {
  background: var(--juwo-primary);
  border-color: var(--juwo-primary);
  color: white;
}

/* 自定义价格滑块 */
.custom-price {
  border-top: 1px solid var(--color-border-default);
  padding-top: 16px;
}

.price-slider-mini {
  margin: 8px 0;
}

.price-slider-mini :deep(.el-slider__runway) {
  background-color: var(--color-border-default);
}

.price-slider-mini :deep(.el-slider__bar) {
  background-color: var(--juwo-primary);
}

.price-slider-mini :deep(.el-slider__button) {
  border: 2px solid var(--juwo-primary);
  background-color: white;
  width: 16px;
  height: 16px;
}

.price-range-display {
  text-align: center;
  font-size: 12px;
  font-weight: 600;
  color: var(--juwo-primary);
}

/* 遮罩层 */
.dropdown-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 10000;  /* 提高以配合dropdown */
  background: transparent;
  pointer-events: auto;
}

/* 响应式设计 */
@media (max-width: 767px) {
  .filter-tabs {
    padding: 8px 4px;
    gap: 6px;
  }
  
  .filter-tab {
    padding: 8px 12px;
    font-size: 13px;
  }
  
  .quick-filter-dropdown {
    min-width: 200px;
    max-width: 240px;
    padding: 12px;
  }
  
  .filter-badge {
    top: -2px;
    right: -2px;
    font-size: 9px;
    padding: 1px 4px;
  }
}
</style>
