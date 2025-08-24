<template>
  <!-- Domain风格筛选面板 -->
  <div v-if="visible" class="filter-panel-wrapper">
    <!-- 遮罩层 -->
    <div class="filter-overlay" @click="closePanel"></div>
    
    <!-- 筛选面板 -->
    <div class="domain-filter-panel" :class="{ 'visible': visible }">
      <!-- 面板头部 -->
      <div class="panel-header">
        <h3 class="panel-title chinese-text">筛选</h3>
        <div class="header-actions">
          <button class="reset-link" @click="resetFilters">重置筛选</button>
          <button class="close-btn" @click="closePanel">
            <i class="fa-solid fa-xmark"></i>
          </button>
        </div>
      </div>
      
      <!-- 筛选内容 -->
      <div class="panel-content">
        <!-- 价格范围滑块 -->
        <div class="filter-section">
          <div class="section-header">
            <h4 class="section-title chinese-text">价格范围 (周租, AUD)</h4>
            <span class="price-display">{{ priceRangeText }}</span>
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

        <!-- 卧室数量 -->
        <div class="filter-section">
          <h4 class="section-title chinese-text">卧室</h4>
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

        <!-- 浴室数量 -->
        <div class="filter-section">
          <h4 class="section-title chinese-text">浴室</h4>
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

        <!-- 车位数量 -->
        <div class="filter-section">
          <h4 class="section-title chinese-text">车位</h4>
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
          <h4 class="section-title chinese-text">入住时间</h4>
          <el-date-picker
            v-model="filters.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            size="large"
            class="date-picker"
            @change="handleDateChange"
          />
        </div>

        <!-- 家具选项 -->
        <div class="filter-section">
          <h4 class="section-title chinese-text">家具</h4>
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
      <div class="panel-footer">
        <el-button class="cancel-btn" size="large" @click="closePanel">
          取消
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
    </div>
  </div>
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
  dateRange: [],
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
      applyFiltersToStore()
      return
    }
    
    if (currentBedrooms.includes('any')) {
      filters.value.bedrooms = [value]
      applyFiltersToStore()
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
  applyFiltersToStore()
}

const toggleBathroom = (value) => {
  const currentBathrooms = [...filters.value.bathrooms]
  const index = currentBathrooms.indexOf(value)
  
  if (index > -1) {
    currentBathrooms.splice(index, 1)
  } else {
    if (value === 'any') {
      filters.value.bathrooms = ['any']
      applyFiltersToStore()
      return
    }
    
    if (currentBathrooms.includes('any')) {
      filters.value.bathrooms = [value]
      applyFiltersToStore()
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
  applyFiltersToStore()
}

const toggleParking = (value) => {
  const currentParking = [...filters.value.parking]
  const index = currentParking.indexOf(value)
  
  if (index > -1) {
    currentParking.splice(index, 1)
  } else {
    if (value === 'any') {
      filters.value.parking = ['any']
      applyFiltersToStore()
      return
    }
    
    if (currentParking.includes('any')) {
      filters.value.parking = [value]
      applyFiltersToStore()
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
  applyFiltersToStore()
}

const handlePriceChange = () => {
  applyFiltersToStore()
}

const handleDateChange = () => {
  applyFiltersToStore()
}

const handleFurnishedChange = () => {
  applyFiltersToStore()
}

// 关闭面板方法
const closePanel = () => {
  visible.value = false
}

const applyFiltersToStore = () => {
  const filterParams = {
    minPrice: filters.value.priceRange[0] > 0 ? filters.value.priceRange[0] : null,
    maxPrice: filters.value.priceRange[1] < 5000 ? filters.value.priceRange[1] : null,
    bedrooms: filters.value.bedrooms.includes('any') ? 'any' : filters.value.bedrooms.join(','),
    bathrooms: filters.value.bathrooms.includes('any') ? 'any' : filters.value.bathrooms.join(','),
    parking: filters.value.parking.includes('any') ? 'any' : filters.value.parking.join(','),
    date_from: filters.value.dateRange ? filters.value.dateRange[0] : null,
    date_to: filters.value.dateRange ? filters.value.dateRange[1] : null,
    isFurnished: filters.value.isFurnished
  }
  
  propertiesStore.applyFilters(filterParams)
  emit('filtersChanged', filterParams)
}

const applyFilters = () => {
  applyFiltersToStore()
  closePanel()
}

const resetFilters = () => {
  filters.value = {
    priceRange: [0, 5000],
    bedrooms: ['any'],
    bathrooms: ['any'],
    parking: ['any'],
    dateRange: [],
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
/* Domain风格筛选面板包装器 */
.filter-panel-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 2000;
}

/* 遮罩层 */
.filter-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  transition: opacity 0.3s ease;
}

/* Domain风格筛选面板 */
.domain-filter-panel {
  position: absolute;
  top: 0;
  right: 0;
  width: 420px;
  height: 100vh;
  background: white;
  box-shadow: -4px 0 20px rgba(0, 0, 0, 0.15);
  transform: translateX(100%);
  transition: transform 0.3s ease;
  display: flex;
  flex-direction: column;
}

.domain-filter-panel.visible {
  transform: translateX(0);
}

/* 面板头部 */
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--color-border-default);
  background: white;
}

.panel-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.reset-link {
  background: none;
  border: none;
  color: var(--juwo-primary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  text-decoration: underline;
  padding: 4px;
}

.reset-link:hover {
  color: var(--juwo-primary-dark);
}

.close-btn {
  background: none;
  border: none;
  color: var(--color-text-secondary);
  font-size: 20px;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: #f5f5f5;
  color: var(--color-text-primary);
}

/* 面板内容 */
.panel-content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

/* 筛选区块 */
.filter-section {
  margin-bottom: 32px;
}

.filter-section:last-child {
  margin-bottom: 0;
}

/* 区块标题 */
.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 16px 0;
}

/* 价格区块头部 */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.price-display {
  font-size: 14px;
  font-weight: 600;
  color: var(--juwo-primary);
}

/* 价格滑块 */
.price-slider {
  margin: 8px 0;
}

.price-slider :deep(.el-slider__runway) {
  background-color: #e5e7eb;
  height: 6px;
}

.price-slider :deep(.el-slider__bar) {
  background-color: var(--juwo-primary);
  height: 6px;
}

.price-slider :deep(.el-slider__button) {
  border: 3px solid var(--juwo-primary);
  background-color: white;
  width: 20px;
  height: 20px;
}

.price-slider :deep(.el-slider__button:hover) {
  border-color: var(--juwo-primary-light);
}

/* 筛选按钮组 */
.filter-buttons-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.filter-btn {
  padding: 12px 18px;
  border: 1px solid var(--color-border-default);
  border-radius: 8px;
  background: white;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 60px;
}

.filter-btn:hover {
  border-color: var(--juwo-primary);
  color: var(--juwo-primary);
  background: var(--juwo-primary-50);
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
  border-radius: 8px;
  border: 1px solid var(--color-border-default);
}

.date-picker :deep(.el-input__wrapper):hover {
  border-color: var(--juwo-primary);
}

.date-picker :deep(.el-input__wrapper.is-focus) {
  border-color: var(--juwo-primary);
  box-shadow: 0 0 0 3px rgba(255, 88, 36, 0.1);
}

/* 家具开关 */
.furnished-toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  background: #f8f9fa;
  border: 1px solid var(--color-border-default);
  border-radius: 8px;
}

.toggle-label {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
}

.furnished-toggle :deep(.el-switch__core) {
  background-color: var(--color-border-default);
}

.furnished-toggle :deep(.el-switch.is-checked .el-switch__core) {
  background-color: var(--juwo-primary);
}

/* 面板底部 */
.panel-footer {
  display: flex;
  gap: 12px;
  padding: 24px;
  border-top: 1px solid var(--color-border-default);
  background: white;
}

.cancel-btn {
  flex: 1;
  background: white;
  border: 1px solid var(--color-border-default);
  color: var(--color-text-secondary);
}

.cancel-btn:hover {
  border-color: var(--juwo-primary);
  color: var(--juwo-primary);
}

.apply-btn {
  flex: 2;
  background-color: var(--juwo-primary);
  border-color: var(--juwo-primary);
}

.apply-btn:hover {
  background-color: var(--juwo-primary-light);
  border-color: var(--juwo-primary-light);
}

/* 移动端全屏模式 */
@media (max-width: 767px) {
  .domain-filter-panel {
    width: 100%;
    transform: translateY(100%);
  }
  
  .domain-filter-panel.visible {
    transform: translateY(0);
  }
  
  .panel-content {
    padding: 20px;
  }
  
  .filter-section {
    margin-bottom: 24px;
  }
  
  .filter-btn {
    padding: 10px 16px;
    font-size: 13px;
    min-width: 55px;
  }
  
  .panel-footer {
    padding: 20px;
  }
}
</style>
