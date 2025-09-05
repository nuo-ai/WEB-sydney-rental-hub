<template>
  <!-- Domain风格筛选面板 -->
  <div v-if="visible" class="filter-panel-wrapper visible">
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

        <!-- 空出日期 -->
        <div class="filter-section">
          <h4 class="section-title chinese-text">空出日期</h4>
          <div class="date-picker-group">
            <el-date-picker
              v-model="filters.startDate"
              type="date"
              placeholder="开始日期"
              size="large"
              class="date-picker-start"
              @change="handleStartDateChange"
            />
            <span class="date-separator">至</span>
            <el-date-picker
              v-model="filters.endDate"
              type="date"
              placeholder="结束日期"
              size="large"
              class="date-picker-end"
              @change="handleEndDateChange"
            />
          </div>
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
import { ref, computed, watch, onMounted, nextTick } from 'vue'
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
  startDate: null,
  endDate: null,
  isFurnished: false
})

// 本地计算的筛选结果数量
const localFilteredCount = ref(0)

// 辅助函数：格式化日期为YYYY-MM-DD
const formatDateToYYYYMMDD = (date) => {
  if (!date) return null
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// 选项数据
const bedroomOptions = [
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
  // 如果还没有进行过筛选，返回总数
  if (localFilteredCount.value === 0 && !hasAppliedFilters.value) {
    return propertiesStore.totalCount || propertiesStore.allProperties.length
  }
  return localFilteredCount.value
})

// 检查是否应用了筛选
const hasAppliedFilters = computed(() => {
  return filters.value.priceRange[0] > 0 ||
         filters.value.priceRange[1] < 5000 ||
         filters.value.bedrooms.length > 0 ||
         filters.value.bathrooms.length > 0 ||
         filters.value.parking.length > 0 ||
         filters.value.startDate !== null ||
         filters.value.endDate !== null ||
         filters.value.isFurnished !== false
})

// 相邻多选逻辑
const isBedroomSelected = (value) => {
  return filters.value.bedrooms.includes(value)
}

const isBathroomSelected = (value) => {
  if (value === 'any') {
    // Any 按钮在没有任何选择时显示为选中
    return filters.value.bathrooms.length === 0
  }
  return filters.value.bathrooms.includes(value)
}

const isParkingSelected = (value) => {
  if (value === 'any') {
    // Any 按钮在没有任何选择时显示为选中
    return filters.value.parking.length === 0
  }
  return filters.value.parking.includes(value)
}

// 相邻选择验证
// 注：已改为单选逻辑，不再需要相邻检查

// 事件处理
const toggleBedroom = (value) => {
  // 单选逻辑：如果已选中则取消，否则选中
  if (filters.value.bedrooms.includes(value)) {
    filters.value.bedrooms = []
  } else {
    filters.value.bedrooms = [value]
  }
  updateFilteredCount()
}

const toggleBathroom = (value) => {
  // 单选逻辑：如果已选中则取消，否则选中
  if (value === 'any') {
    filters.value.bathrooms = []
  } else if (filters.value.bathrooms.includes(value)) {
    filters.value.bathrooms = []
  } else {
    filters.value.bathrooms = [value]
  }
  updateFilteredCount()
}

const toggleParking = (value) => {
  // 单选逻辑：如果已选中则取消，否则选中
  if (value === 'any') {
    filters.value.parking = []
  } else if (filters.value.parking.includes(value)) {
    filters.value.parking = []
  } else {
    filters.value.parking = [value]
  }
  updateFilteredCount()
}

// 实时更新筛选数量（不立即应用到store）
const updateFilteredCount = async () => {
  // 准备筛选参数，与后端API保持一致
  const filterParams = {
    minPrice: filters.value.priceRange[0] > 0 ? filters.value.priceRange[0] : null,
    maxPrice: filters.value.priceRange[1] < 5000 ? filters.value.priceRange[1] : null,
    bedrooms: filters.value.bedrooms.length > 0 ? filters.value.bedrooms.join(',') : null,
    bathrooms: filters.value.bathrooms.length > 0 ? filters.value.bathrooms.join(',') : null,
    parking: filters.value.parking.length > 0 ? filters.value.parking.join(',') : null,
    date_from: filters.value.startDate ? formatDateToYYYYMMDD(filters.value.startDate) : null,
    date_to: filters.value.endDate ? formatDateToYYYYMMDD(filters.value.endDate) : null,
    isFurnished: filters.value.isFurnished || null
  }

  // 添加已选择的区域
  const selectedSuburbs = propertiesStore.selectedLocations.map(loc => loc.name)
  if (selectedSuburbs.length > 0) {
    filterParams.suburb = selectedSuburbs.join(',')
  }

  // 移除 null 值
  Object.keys(filterParams).forEach(key => {
    if (filterParams[key] === null || filterParams[key] === '') {
      delete filterParams[key]
    }
  })

  // 如果没有任何筛选条件（包括区域），显示总数
  if (Object.keys(filterParams).length === 0) {
    localFilteredCount.value = 3456
    return
  }

  try {
    // 调用API获取实际的筛选结果数量
    const response = await fetch(`/api/properties?page=1&page_size=1&${new URLSearchParams(filterParams)}`)
    const data = await response.json()
    if (data.status === 'success' && data.pagination) {
      localFilteredCount.value = data.pagination.total
    } else {
      // 如果API调用失败，使用估算
      calculateLocalCount()
    }
  } catch (error) {
    console.error('获取筛选计数失败:', error)
    // 使用估算作为备用方案
    calculateLocalCount()
  }
}


// 本地计算备用方案 - 基于总数进行估算
const calculateLocalCount = () => {
  // 基于区域筛选后的总数进行估算
  let totalProperties = 3456

  // 如果有选中区域，使用区域筛选后的基数
  const selectedSuburbs = propertiesStore.selectedLocations
  if (selectedSuburbs.length > 0) {
    // 使用当前store中的totalCount（如果有）或估算值
    totalProperties = propertiesStore.totalCount || Math.floor(3456 * (selectedSuburbs.length / 10))
  }

  // 如果没有其他筛选条件（除了区域）
  if (!hasAppliedFilters.value && selectedSuburbs.length === 0) {
    localFilteredCount.value = totalProperties
    return
  }

  // 根据筛选条件估算
  let estimate = totalProperties

      // 卧室筛选估算
      const allBedroomOpts = ['1', '2', '3', '4+']
      const isAllBeds = allBedroomOpts.every(opt => filters.value.bedrooms.includes(opt))
      if (filters.value.bedrooms.length > 0 && !isAllBeds) {
        const bedroomCount = filters.value.bedrooms.length
        estimate = Math.floor(estimate * (bedroomCount / 4))
      }

      // 价格筛选估算
      const [minPrice, maxPrice] = filters.value.priceRange
      if (minPrice > 0 || maxPrice < 5000) {
        const priceRange = maxPrice - minPrice
        estimate = Math.floor(estimate * (priceRange / 5000))
      }

      // 浴室筛选估算
      const allBathOpts = ['1', '2', '3+']
      const isAllBaths = allBathOpts.every(opt => filters.value.bathrooms.includes(opt))
      if (filters.value.bathrooms.length > 0 && !isAllBaths) {
        estimate = Math.floor(estimate * 0.7)
      }

      // 车位筛选估算
      const allParkOpts = ['0', '1', '2+']
      const isAllParks = allParkOpts.every(opt => filters.value.parking.includes(opt))
      if (filters.value.parking.length > 0 && !isAllParks) {
        estimate = Math.floor(estimate * 0.6)
      }

      // 家具筛选估算
      if (filters.value.isFurnished) {
        estimate = Math.floor(estimate * 0.4)
      }

      // 空出日期筛选估算
      if (filters.value.startDate || filters.value.endDate) {
        estimate = Math.floor(estimate * 0.8)  // 大约80%的房源在指定时间可用
      }


  // 保证估算值合理
  localFilteredCount.value = Math.max(1, Math.min(estimate, totalProperties))
}

const handlePriceChange = () => {
  nextTick(() => updateFilteredCount())
}

const handleStartDateChange = (date) => {
  filters.value.startDate = date
  nextTick(() => updateFilteredCount())
}

const handleEndDateChange = (date) => {
  filters.value.endDate = date
  nextTick(() => updateFilteredCount())
}

const handleFurnishedChange = () => {
  nextTick(() => updateFilteredCount())
}

// 关闭面板方法
const closePanel = () => {
  visible.value = false
}

const applyFiltersToStore = async () => {
  try {
    // 准备筛选参数，直接传递选中的值
    const filterParams = {
      minPrice: filters.value.priceRange[0] > 0 ? filters.value.priceRange[0] : null,
      maxPrice: filters.value.priceRange[1] < 5000 ? filters.value.priceRange[1] : null,
      bedrooms: filters.value.bedrooms.length > 0 ? filters.value.bedrooms.join(',') : null,
      bathrooms: filters.value.bathrooms.length > 0 ? filters.value.bathrooms.join(',') : null,
      parking: filters.value.parking.length > 0 ? filters.value.parking.join(',') : null,
      date_from: filters.value.startDate ? formatDateToYYYYMMDD(filters.value.startDate) : null,
      date_to: filters.value.endDate ? formatDateToYYYYMMDD(filters.value.endDate) : null,
      isFurnished: filters.value.isFurnished || null
    }

    // 添加已选择的区域
    const selectedSuburbs = propertiesStore.selectedLocations.map(loc => loc.name)
    if (selectedSuburbs.length > 0) {
      filterParams.suburb = selectedSuburbs.join(',')
    }

    await propertiesStore.applyFilters(filterParams)
    emit('filtersChanged', filterParams)
  } catch (error) {
    console.error('筛选应用失败:', error)
  }
}

const applyFilters = async () => {
  await applyFiltersToStore()
  // 应用后更新计数为实际结果
  localFilteredCount.value = propertiesStore.totalCount
  closePanel()
}

const resetFilters = () => {
  filters.value = {
    priceRange: [0, 5000],
    bedrooms: [],
    bathrooms: [],
    parking: [],
    startDate: null,
    endDate: null,
    isFurnished: false
  }

  // 如果有选中的区域，基于区域更新计数；否则显示总数
  if (propertiesStore.selectedLocations.length > 0) {
    updateFilteredCount()
  } else {
    localFilteredCount.value = propertiesStore.totalCount || 3456
  }
}


// 暴露方法给父组件以同步状态
defineExpose({
  setFilters: (newFilters) => {
    if (newFilters.priceRange) filters.value.priceRange = newFilters.priceRange
    if (newFilters.bedrooms) filters.value.bedrooms = newFilters.bedrooms
    if (newFilters.bathrooms) filters.value.bathrooms = newFilters.bathrooms
    if (newFilters.parking) filters.value.parking = newFilters.parking
  }
})

// 生命周期
watch(visible, (newValue) => {
  if (newValue) {
    // 打开面板时，更新筛选计数
    updateFilteredCount()
  }
})

// 初始化时设置默认计数
onMounted(() => {
  // 如果有选中的区域，更新计数；否则显示总数
  if (propertiesStore.selectedLocations.length > 0) {
    updateFilteredCount()
  } else {
    localFilteredCount.value = propertiesStore.totalCount || 3456
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
  z-index: 2000;  /* 降低z-index，让日期选择器能显示在上面 */
  pointer-events: none;  /* 默认不捕获事件，只在visible时才捕获 */
}

.filter-panel-wrapper.visible {
  pointer-events: auto;  /* 只在显示时捕获点击事件 */
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
  pointer-events: auto;  /* 确保遮罩层可点击 */
}

/* 移动端遮罩层 */
@media (max-width: 767px) {
  .filter-overlay {
    background: rgba(0, 0, 0, 0.5); /* 移动端加深背景 */
  }
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
  z-index: 2001;  /* 确保面板在遮罩层之上 */
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

/* 移动端按钮组 */
@media (max-width: 767px) {
  .filter-buttons-group {
    gap: 8px;
  }
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
.date-picker-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.date-picker-start,
.date-picker-end {
  flex: 1;
}

.date-separator {
  color: var(--color-text-secondary);
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

/* 确保日期选择器弹出层在最上层 */
:deep(.el-date-picker__popper) {
  z-index: 10002 !important;  /* 高于筛选面板的9999 */
}

:deep(.el-popper) {
  z-index: 10002 !important;
}

:deep(.el-picker__popper) {
  z-index: 10002 !important;
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
    height: 100vh;
    max-height: 100vh;
    top: 0;
    right: 0;
    bottom: auto;
    transform: translateX(100%);
    transition: transform 0.3s ease;
  }

  .domain-filter-panel.visible {
    transform: translateX(0);
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

  /* 移动端滚动优化 */
  .panel-content {
    -webkit-overflow-scrolling: touch;
    overscroll-behavior: contain;
  }

  .panel-footer {
    padding: 20px;
  }
}
</style>
