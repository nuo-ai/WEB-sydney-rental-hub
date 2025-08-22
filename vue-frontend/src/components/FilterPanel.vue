<template>
  <el-drawer
    v-model="visible"
    title="筛选条件"
    :size="drawerSize"
    direction="btt"
    class="filter-drawer"
  >
    <div class="filter-content">
      <!-- 价格范围滑块 -->
      <div class="filter-section">
        <div class="filter-header">
          <h3 class="filter-title chinese-text">价格范围 (周租, AUD)</h3>
          <p class="price-display">{{ priceRangeText }}</p>
        </div>
        <el-slider
          v-model="filters.priceRange"
          range
          :min="0"
          :max="5000"
          :step="50"
          :show-stops="false"
          class="price-slider"
          @change="handlePriceChange"
        />
      </div>

      <!-- 卧室数量 - 相邻多选 -->
      <div class="filter-section">
        <h3 class="filter-title chinese-text">卧室</h3>
        <div class="filter-buttons-group">
          <button
            v-for="option in bedroomOptions"
            :key="option.value"
            class="filter-btn"
            :class="{ 'active': isBedroomSelected(option.value) }"
            @click="toggleBedroom(option.value)"
          >
            {{ option.label }}
          </button>
        </div>
      </div>

      <!-- 浴室数量 - 相邻多选 -->
      <div class="filter-section">
        <h3 class="filter-title chinese-text">浴室</h3>
        <div class="filter-buttons-group">
          <button
            v-for="option in bathroomOptions"
            :key="option.value"
            class="filter-btn"
            :class="{ 'active': isBathroomSelected(option.value) }"
            @click="toggleBathroom(option.value)"
          >
            {{ option.label }}
          </button>
        </div>
      </div>

      <!-- 车位数量 - 相邻多选 -->
      <div class="filter-section">
        <h3 class="filter-title chinese-text">车位</h3>
        <div class="filter-buttons-group">
          <button
            v-for="option in parkingOptions"
            :key="option.value"
            class="filter-btn"
            :class="{ 'active': isParkingSelected(option.value) }"
            @click="toggleParking(option.value)"
          >
            {{ option.label }}
          </button>
        </div>
      </div>

      <!-- 入住时间 -->
      <div class="filter-section">
        <h3 class="filter-title chinese-text">入住时间</h3>
        <el-date-picker
          v-model="filters.availableDate"
          type="date"
          placeholder="选择入住日期"
          size="large"
          class="date-picker"
          @change="handleDateChange"
        />
      </div>

      <!-- 区域选择 -->
      <div class="filter-section">
        <h3 class="filter-title chinese-text">区域</h3>
        <el-select
          v-model="filters.selectedArea"
          placeholder="选择区域"
          size="large"
          clearable
          filterable
          class="area-select"
          @change="handleAreaChange"
        >
          <el-option
            v-for="area in areaOptions"
            :key="area.value"
            :label="area.label"
            :value="area.value"
          />
        </el-select>
      </div>

      <!-- 家具选项 -->
      <div class="filter-section">
        <h3 class="filter-title chinese-text">家具</h3>
        <div class="furnished-toggle">
          <span class="toggle-label chinese-text">只显示带家具的房源</span>
          <el-switch
            v-model="filters.isFurnished"
            size="large"
            @change="handleFurnishedChange"
          />
        </div>
      </div>
    </div>

    <!-- 底部操作按钮 -->
    <template #footer>
      <div class="filter-actions">
        <el-button 
          class="reset-btn" 
          size="large"
          @click="resetFilters"
        >
          重置
        </el-button>
        <el-button 
          type="primary" 
          class="apply-btn" 
          size="large"
          @click="applyFilters"
        >
          显示结果 ({{ filteredCount }})
        </el-button>
      </div>
    </template>
  </el-drawer>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { usePropertiesStore } from '@/stores/properties'

// 组件属性
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

// 组件事件
const emit = defineEmits(['update:modelValue', 'filtersChanged'])

// 状态管理
const propertiesStore = usePropertiesStore()

// 响应式数据
const filters = ref({
  priceRange: [0, 5000],
  bedrooms: [],
  bathrooms: [],
  parking: [],
  availableDate: null,
  selectedArea: '',
  isFurnished: false
})

// 选项数据
const bedroomOptions = [
  { value: 'any', label: 'Any' },
  { value: '1', label: '1' },
  { value: '2', label: '2' },
  { value: '3', label: '3' },
  { value: '4+', label: '4+' }
]

const bathroomOptions = [
  { value: 'any', label: 'Any' },
  { value: '1', label: '1' },
  { value: '2', label: '2' },
  { value: '3+', label: '3+' }
]

const parkingOptions = [
  { value: 'any', label: 'Any' },
  { value: '0', label: '0' },
  { value: '1', label: '1' },
  { value: '2+', label: '2+' }
]

// 计算属性
const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const drawerSize = computed(() => {
  return window.innerWidth <= 768 ? '85%' : '60%'
})

const priceRangeText = computed(() => {
  const [min, max] = filters.value.priceRange
  if (min === 0 && max === 5000) {
    return 'Any Price'
  } else if (max === 5000) {
    return `$${min}+`
  } else {
    return `$${min} - $${max}`
  }
})

const areaOptions = computed(() => {
  return propertiesStore.locationSuggestions
    .filter(location => location.type === 'suburb')
    .map(location => ({
      value: location.id,
      label: location.fullName
    }))
})

const filteredCount = computed(() => {
  return propertiesStore.filteredProperties.length
})

// 相邻多选逻辑
const isBedroomSelected = (value) => {
  return filters.value.bedrooms.includes(value)
}

const isBathroomSelected = (value) => {
  return filters.value.bathrooms.includes(value)
}

const isParkingSelected = (value) => {
  return filters.value.parking.includes(value)
}

// 相邻选择验证
const getNumericValue = (value) => {
  if (value === 'any') return -1
  if (value.includes('+')) return parseInt(value)
  return parseInt(value)
}

const areAdjacent = (arr, newValue) => {
  if (arr.length === 0) return true
  if (arr.includes('any')) return newValue === 'any'
  if (newValue === 'any') return arr.length === 0
  
  const numericValues = arr.map(getNumericValue).filter(v => v >= 0)
  const newNumeric = getNumericValue(newValue)
  
  if (newNumeric < 0) return false
  
  // 检查是否相邻
  const allValues = [...numericValues, newNumeric].sort((a, b) => a - b)
  
  for (let i = 1; i < allValues.length; i++) {
    if (allValues[i] - allValues[i-1] > 1) {
      return false
    }
  }
  
  return allValues.length <= 2 // 最多选择2个相邻值
}

// 事件处理
const toggleBedroom = (value) => {
  const currentBedrooms = [...filters.value.bedrooms]
  const index = currentBedrooms.indexOf(value)
  
  if (index > -1) {
    // 移除选择
    currentBedrooms.splice(index, 1)
  } else {
    // 添加选择
    if (value === 'any') {
      filters.value.bedrooms = ['any']
      return
    }
    
    if (currentBedrooms.includes('any')) {
      filters.value.bedrooms = [value]
      return
    }
    
    if (areAdjacent(currentBedrooms, value)) {
      currentBedrooms.push(value)
      filters.value.bedrooms = currentBedrooms
    } else {
      // 不相邻，替换选择
      filters.value.bedrooms = [value]
    }
  }
  
  filters.value.bedrooms = currentBedrooms
}

const toggleBathroom = (value) => {
  const currentBathrooms = [...filters.value.bathrooms]
  const index = currentBathrooms.indexOf(value)
  
  if (index > -1) {
    currentBathrooms.splice(index, 1)
  } else {
    if (value === 'any') {
      filters.value.bathrooms = ['any']
      return
    }
    
    if (currentBathrooms.includes('any')) {
      filters.value.bathrooms = [value]
      return
    }
    
    if (areAdjacent(currentBathrooms, value)) {
      currentBathrooms.push(value)
      filters.value.bathrooms = currentBathrooms
    } else {
      filters.value.bathrooms = [value]
    }
  }
  
  filters.value.bathrooms = currentBathrooms
}

const toggleParking = (value) => {
  const currentParking = [...filters.value.parking]
  const index = currentParking.indexOf(value)
  
  if (index > -1) {
    currentParking.splice(index, 1)
  } else {
    if (value === 'any') {
      filters.value.parking = ['any']
      return
    }
    
    if (currentParking.includes('any')) {
      filters.value.parking = [value]
      return
    }
    
    if (areAdjacent(currentParking, value)) {
      currentParking.push(value)
      filters.value.parking = currentParking
    } else {
      filters.value.parking = [value]
    }
  }
  
  filters.value.parking = currentParking
}

const handlePriceChange = () => {
  applyFiltersToStore()
}

const handleDateChange = () => {
  applyFiltersToStore()
}

const handleAreaChange = () => {
  applyFiltersToStore()
}

const handleFurnishedChange = () => {
  applyFiltersToStore()
}

const applyFiltersToStore = () => {
  const filterParams = {
    minPrice: filters.value.priceRange[0] > 0 ? filters.value.priceRange[0] : null,
    maxPrice: filters.value.priceRange[1] < 5000 ? filters.value.priceRange[1] : null,
    bedrooms: filters.value.bedrooms.includes('any') ? 'any' : filters.value.bedrooms.join(','),
    bathrooms: filters.value.bathrooms.includes('any') ? 'any' : filters.value.bathrooms.join(','),
    parking: filters.value.parking.includes('any') ? 'any' : filters.value.parking.join(','),
    availableDate: filters.value.availableDate || 'any',
    isFurnished: filters.value.isFurnished
  }
  
  propertiesStore.applyFilters(filterParams)
  emit('filtersChanged', filterParams)
}

const applyFilters = () => {
  applyFiltersToStore()
  visible.value = false
}

const resetFilters = () => {
  filters.value = {
    priceRange: [0, 5000],
    bedrooms: ['any'],
    bathrooms: ['any'],
    parking: ['any'],
    availableDate: null,
    selectedArea: '',
    isFurnished: false
  }
  
  propertiesStore.resetFilters()
  emit('filtersChanged', null)
}

// 初始化
const initializeFilters = () => {
  filters.value.bedrooms = ['any']
  filters.value.bathrooms = ['any']
  filters.value.parking = ['any']
}

// 生命周期
watch(visible, (newValue) => {
  if (newValue) {
    initializeFilters()
  }
})
</script>

<style scoped>
/* 筛选抽屉样式 */
.filter-drawer :deep(.el-drawer__header) {
  background: var(--color-bg-card);
  border-bottom: 1px solid var(--color-border-default);
  padding: 20px 24px;
  margin-bottom: 0;
}

.filter-drawer :deep(.el-drawer__title) {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text-primary);
}

.filter-drawer :deep(.el-drawer__body) {
  padding: 0;
}

.filter-drawer :deep(.el-drawer__footer) {
  background: var(--color-bg-card);
  border-top: 1px solid var(--color-border-default);
  padding: 20px 24px;
}

/* 筛选内容区域 */
.filter-content {
  padding: 24px;
  max-height: calc(85vh - 140px);
  overflow-y: auto;
}

/* 筛选区块 */
.filter-section {
  margin-bottom: 32px;
}

.filter-section:last-child {
  margin-bottom: 0;
}

/* 筛选标题 */
.filter-header {
  display: flex;
  justify-content: between;
  align-items: center;
  margin-bottom: 16px;
}

.filter-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.price-display {
  font-size: 16px;
  font-weight: 600;
  color: var(--juwo-primary);
  margin: 0;
}

/* 价格滑块 */
.price-slider {
  margin: 16px 8px;
}

.price-slider :deep(.el-slider__runway) {
  background-color: var(--color-border-default);
}

.price-slider :deep(.el-slider__bar) {
  background-color: var(--juwo-primary);
}

.price-slider :deep(.el-slider__button) {
  border: 3px solid var(--juwo-primary);
  background-color: white;
}

.price-slider :deep(.el-slider__button:hover) {
  border-color: var(--juwo-primary-light);
}

/* 筛选按钮组 */
.filter-buttons-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.filter-btn {
  padding: 10px 20px;
  border: 2px solid var(--color-border-default);
  border-radius: var(--radius-sm);
  background: white;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 60px;
}

.filter-btn:hover {
  border-color: var(--juwo-primary);
  color: var(--juwo-primary);
}

.filter-btn.active {
  background: var(--juwo-primary);
  border-color: var(--juwo-primary);
  color: white;
}

/* 日期选择器 */
.date-picker {
  width: 100%;
}

.date-picker :deep(.el-input__wrapper) {
  border-radius: var(--radius-lg);
  border: 2px solid var(--color-border-default);
}

.date-picker :deep(.el-input__wrapper):hover {
  border-color: var(--juwo-primary);
}

.date-picker :deep(.el-input__wrapper.is-focus) {
  border-color: var(--juwo-primary);
  box-shadow: 0 0 0 4px rgba(255, 88, 36, 0.1);
}

/* 区域选择器 */
.area-select {
  width: 100%;
}

.area-select :deep(.el-input__wrapper) {
  border-radius: var(--radius-lg);
  border: 2px solid var(--color-border-default);
}

.area-select :deep(.el-input__wrapper):hover {
  border-color: var(--juwo-primary);
}

.area-select :deep(.el-input__wrapper.is-focus) {
  border-color: var(--juwo-primary);
  box-shadow: 0 0 0 4px rgba(255, 88, 36, 0.1);
}

/* 家具开关 */
.furnished-toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  background: white;
  border: 2px solid var(--color-border-default);
  border-radius: var(--radius-lg);
}

.toggle-label {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
}

/* 开关组件定制 */
.furnished-toggle :deep(.el-switch__core) {
  background-color: var(--color-border-default);
}

.furnished-toggle :deep(.el-switch.is-checked .el-switch__core) {
  background-color: var(--juwo-primary);
}

/* 底部操作按钮 */
.filter-actions {
  display: flex;
  gap: 16px;
  width: 100%;
}

.reset-btn {
  flex: 1;
  background: #f5f5f5;
  border-color: #d9d9d9;
  color: var(--color-text-secondary);
  font-weight: 600;
}

.reset-btn:hover {
  background: #e8e8e8;
  border-color: #bfbfbf;
}

.apply-btn {
  flex: 2;
  background-color: var(--juwo-primary);
  border-color: var(--juwo-primary);
  font-weight: 600;
}

.apply-btn:hover {
  background-color: var(--juwo-primary-light);
  border-color: var(--juwo-primary-light);
}

/* 响应式适配 */
@media (max-width: 767px) {
  .filter-content {
    padding: 20px;
  }
  
  .filter-section {
    margin-bottom: 24px;
  }
  
  .filter-buttons-group {
    gap: 6px;
  }
  
  .filter-btn {
    padding: 8px 16px;
    font-size: 13px;
    min-width: 50px;
  }
  
  .filter-actions {
    flex-direction: column;
    gap: 12px;
  }
  
  .reset-btn,
  .apply-btn {
    flex: none;
  }
}
</style>
