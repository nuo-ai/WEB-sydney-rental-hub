<template>
  <div v-if="visible" class="filter-wizard-wrapper">
    <!-- 遮罩层 -->
    <div class="filter-overlay" @click="closeWizard"></div>

    <!-- 筛选向导面板 -->
    <div ref="wizardRef" class="filter-wizard-panel" tabindex="-1">
      <!-- 头部 -->
      <div class="wizard-header">
        <div class="wizard-progress">
          <div
            v-for="step in 4"
            :key="step"
            class="progress-step"
            :class="{
              active: step === currentStep,
              completed: step < currentStep,
              disabled: step > currentStep && !canJumpToStep(step)
            }"
            @click="goToStep(step)"
          >
            <div class="step-number">{{ step }}</div>
            <div class="step-title">{{ stepTitles[step] }}</div>
          </div>
        </div>
        <button class="close-btn" @click="closeWizard" aria-label="关闭筛选向导">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M18 6 6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>

      <!-- 内容区域 -->
      <div class="wizard-content">
        <!-- 步骤1: 选择区域 -->
        <div v-if="currentStep === 1" class="step-content">
          <h3 class="step-heading">选择您感兴趣的区域</h3>
          <p class="step-description">请至少选择一个区域来开始搜索</p>

          <div class="selected-areas" v-if="filterState.areas.length > 0">
            <div class="area-chips">
              <div
                v-for="area in filterState.areas"
                :key="area.id"
                class="area-chip"
              >
                {{ area.name || area.suburb }}
                <button
                  class="remove-btn"
                  @click="removeArea(area.id)"
                  :aria-label="`移除 ${area.name || area.suburb}`"
                >
                  ×
                </button>
              </div>
            </div>
          </div>

          <AreasSelector
            :selected="filterState.areas"
            @update:selected="updateAreas"
            placeholder="搜索区域名称或邮编..."
          />

          <div class="step-preview" v-if="isStep1Valid">
            <div class="preview-count">
              <template v-if="isCountingLoading">
                <div class="loading-spinner"></div>
                <span>正在统计...</span>
              </template>
              <template v-else-if="countError">
                <span class="error-text">{{ countError }}</span>
              </template>
              <template v-else>
                <span class="count-number">{{ previewCount }}</span>
                <span>套房源在所选区域</span>
              </template>
            </div>
          </div>
        </div>

        <!-- 步骤2: 选择房型 -->
        <div v-if="currentStep === 2" class="step-content">
          <h3 class="step-heading">选择房型</h3>
          <p class="step-description">请选择您需要的房间数量</p>

          <div class="bedroom-options">
            <button
              v-for="option in bedroomOptions"
              :key="option.value"
              class="bedroom-btn"
              :class="{ active: filterState.bedrooms === option.value }"
              @click="selectBedroom(option.value)"
            >
              {{ option.label }}
            </button>
          </div>

          <div class="step-preview" v-if="isStep2Valid">
            <div class="preview-count">
              <template v-if="isCountingLoading">
                <div class="loading-spinner"></div>
                <span>正在统计...</span>
              </template>
              <template v-else-if="countError">
                <span class="error-text">{{ countError }}</span>
              </template>
              <template v-else>
                <span class="count-number">{{ previewCount }}</span>
                <span>套{{ getBedroomText(filterState.bedrooms) }}房源</span>
              </template>
            </div>
          </div>
        </div>

        <!-- 步骤3: 设置条件 -->
        <div v-if="currentStep === 3" class="step-content">
          <h3 class="step-heading">设置筛选条件</h3>
          <p class="step-description">根据您的需求调整以下条件（可选）</p>

          <!-- 价格范围 -->
          <div class="filter-group">
            <label class="group-label">周租金范围</label>
            <div class="price-display">
              ${{ filterState.priceRange[0] }} - ${{ filterState.priceRange[1] }}
              <span v-if="filterState.priceRange[1] >= 5000">+</span>
            </div>
            <el-slider
              v-model="filterState.priceRange"
              range
              :min="0"
              :max="5000"
              :step="50"
              class="price-slider"
            />
          </div>

          <!-- 浴室数量 -->
          <div class="filter-group">
            <label class="group-label">浴室数量</label>
            <div class="option-buttons">
              <button
                v-for="option in bathroomOptions"
                :key="option.value"
                class="option-btn"
                :class="{ active: filterState.bathrooms === option.value }"
                @click="selectBathroom(option.value)"
              >
                {{ option.label }}
              </button>
            </div>
          </div>

          <!-- 车位数量 -->
          <div class="filter-group">
            <label class="group-label">车位数量</label>
            <div class="option-buttons">
              <button
                v-for="option in parkingOptions"
                :key="option.value"
                class="option-btn"
                :class="{ active: filterState.parking === option.value }"
                @click="selectParking(option.value)"
              >
                {{ option.label }}
              </button>
            </div>
          </div>

          <!-- 家具 -->
          <div class="filter-group">
            <label class="group-label">家具要求</label>
            <div class="furnished-toggle">
              <span>仅显示有家具房源</span>
              <el-switch v-model="filterState.furnished" />
            </div>
          </div>
        </div>

        <!-- 步骤4: 确认搜索 -->
        <div v-if="currentStep === 4" class="step-content">
          <h3 class="step-heading">确认搜索条件</h3>
          <p class="step-description">请确认您的筛选条件，然后开始搜索</p>

          <!-- 日期选择 -->
          <div class="filter-group">
            <label class="group-label">入住时间（可选）</label>
            <div class="date-inputs">
              <el-date-picker
                v-model="filterState.dateFrom"
                type="date"
                placeholder="最早入住日期"
                size="large"
                class="date-picker"
              />
              <span class="date-separator">至</span>
              <el-date-picker
                v-model="filterState.dateTo"
                type="date"
                placeholder="最晚入住日期"
                size="large"
                class="date-picker"
              />
            </div>
          </div>

          <!-- 条件总结 -->
          <div class="conditions-summary">
            <h4>您的筛选条件：</h4>
            <div class="summary-items">
              <div class="summary-item">
                <span class="item-label">区域：</span>
                <span class="item-value">{{ getAreasSummary() }}</span>
              </div>
              <div class="summary-item">
                <span class="item-label">房型：</span>
                <span class="item-value">{{ getBedroomText(filterState.bedrooms) }}</span>
              </div>
              <div class="summary-item" v-if="hasPriceFilter">
                <span class="item-label">价格：</span>
                <span class="item-value">${{ filterState.priceRange[0] }} - ${{ filterState.priceRange[1] }}<span v-if="filterState.priceRange[1] >= 5000">+</span></span>
              </div>
              <div class="summary-item" v-if="filterState.bathrooms">
                <span class="item-label">浴室：</span>
                <span class="item-value">{{ getBathroomText(filterState.bathrooms) }}</span>
              </div>
              <div class="summary-item" v-if="filterState.parking">
                <span class="item-label">车位：</span>
                <span class="item-value">{{ getParkingText(filterState.parking) }}</span>
              </div>
              <div class="summary-item" v-if="filterState.furnished">
                <span class="item-label">家具：</span>
                <span class="item-value">有家具</span>
              </div>
              <div class="summary-item" v-if="filterState.dateFrom || filterState.dateTo">
                <span class="item-label">入住时间：</span>
                <span class="item-value">{{ getDateRangeSummary() }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 底部操作栏 -->
      <div class="wizard-footer">
        <button
          v-if="currentStep > 1"
          class="btn-secondary"
          @click="prevStep"
        >
          上一步
        </button>

        <div class="footer-spacer"></div>

        <button
          v-if="currentStep < 4"
          class="btn-primary"
          :disabled="!canProceedToNext"
          @click="nextStep"
        >
          下一步
        </button>

        <button
          v-if="currentStep === 4"
          class="btn-primary search-btn"
          @click="handleSearch"
          :disabled="!isStep1Valid || !isStep2Valid"
        >
          搜索房源
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onUnmounted } from 'vue'
import { useFilterWizard } from '@/composables/useFilterWizard'
import AreasSelector from '@/components/AreasSelector.vue'

// 组件属性
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

// 组件事件
const emit = defineEmits(['update:modelValue', 'search'])

// 使用筛选向导
const {
  currentStep,
  filterState,
  previewCount,
  isCountingLoading,
  countError,
  isStep1Valid,
  isStep2Valid,
  canProceedToNext,
  goToStep,
  nextStep,
  prevStep,
  applyFilters,
  generateResultDescription
} = useFilterWizard()

// 面板引用
const wizardRef = ref(null)

// 显示状态
const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 步骤标题
const stepTitles = {
  1: '选择区域',
  2: '选择房型',
  3: '设置条件',
  4: '确认搜索'
}

// 选项数据
const bedroomOptions = [
  { value: '0', label: 'Studio' },
  { value: '1', label: '1房' },
  { value: '2', label: '2房' },
  { value: '3', label: '3房' },
  { value: '4+', label: '4房+' }
]

const bathroomOptions = [
  { value: null, label: '不限' },
  { value: '1', label: '1个' },
  { value: '2', label: '2个' },
  { value: '3+', label: '3个+' }
]

const parkingOptions = [
  { value: null, label: '不限' },
  { value: '1', label: '1个' },
  { value: '2', label: '2个' },
  { value: '3+', label: '3个+' }
]

// 计算属性
const hasPriceFilter = computed(() => {
  const [min, max] = filterState.value.priceRange
  return min > 0 || max < 5000
})

// 方法
const canJumpToStep = (step) => {
  if (step <= currentStep.value) return true
  if (step === 2) return isStep1Valid.value
  if (step === 3) return isStep1Valid.value && isStep2Valid.value
  if (step === 4) return isStep1Valid.value && isStep2Valid.value
  return false
}

const updateAreas = (areas) => {
  filterState.value.areas = areas
}

const removeArea = (areaId) => {
  filterState.value.areas = filterState.value.areas.filter(area => area.id !== areaId)
}

const selectBedroom = (value) => {
  filterState.value.bedrooms = filterState.value.bedrooms === value ? null : value
}

const selectBathroom = (value) => {
  filterState.value.bathrooms = filterState.value.bathrooms === value ? null : value
}

const selectParking = (value) => {
  filterState.value.parking = filterState.value.parking === value ? null : value
}

const getBedroomText = (bedrooms) => {
  if (!bedrooms) return ''
  if (bedrooms === '0') return 'Studio'
  if (bedrooms === '4+') return '4房及以上'
  return `${bedrooms}房`
}

const getBathroomText = (bathrooms) => {
  if (!bathrooms) return '不限'
  if (bathrooms === '3+') return '3个及以上'
  return `${bathrooms}个`
}

const getParkingText = (parking) => {
  if (!parking) return '不限'
  if (parking === '3+') return '3个及以上'
  return `${parking}个`
}

const getAreasSummary = () => {
  const areas = filterState.value.areas
  if (areas.length === 0) return '未选择'
  if (areas.length <= 2) {
    return areas.map(a => a.name || a.suburb).join('、')
  }
  return `${areas[0].name || areas[0].suburb} 等 ${areas.length} 个区域`
}

const getDateRangeSummary = () => {
  const { dateFrom, dateTo } = filterState.value
  if (dateFrom && dateTo) {
    return `${formatDate(dateFrom)} 至 ${formatDate(dateTo)}`
  }
  if (dateFrom) {
    return `${formatDate(dateFrom)} 之后`
  }
  if (dateTo) {
    return `${formatDate(dateTo)} 之前`
  }
  return '未设置'
}

const formatDate = (date) => {
  if (!date) return ''
  const d = new Date(date)
  return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`
}

const handleSearch = async () => {
  try {
    const success = await applyFilters()
    if (success) {
      emit('search', {
        filters: filterState.value,
        description: generateResultDescription(previewCount.value, filterState.value)
      })
      closeWizard()
    }
  } catch (error) {
    console.error('搜索失败:', error)
  }
}

const closeWizard = () => {
  visible.value = false
}

// 键盘事件处理
const handleKeyDown = (event) => {
  if (event.key === 'Escape') {
    closeWizard()
  }
}

// 生命周期
watch(visible, (newValue) => {
  if (newValue) {
    // 打开时聚焦到面板
    nextTick(() => {
      wizardRef.value?.focus()
    })
    // 添加键盘监听
    document.addEventListener('keydown', handleKeyDown)
  } else {
    // 关闭时移除监听
    document.removeEventListener('keydown', handleKeyDown)
  }
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyDown)
})
</script>

<style scoped>
/* 筛选向导样式 */
.filter-wizard-wrapper {
  position: fixed;
  inset: 0;
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.filter-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
}

.filter-wizard-panel {
  position: relative;
  width: 90vw;
  max-width: 800px;
  max-height: 90vh;
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 头部样式 */
.wizard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px;
  border-bottom: 1px solid var(--color-border-default);
  background: var(--color-bg-card);
}

.wizard-progress {
  display: flex;
  gap: 32px;
}

.progress-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.progress-step.disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.step-number {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  border: 2px solid var(--color-border-default);
  background: white;
  color: var(--color-text-secondary);
  transition: all 0.2s ease;
}

.progress-step.active .step-number {
  background: var(--juwo-primary);
  border-color: var(--juwo-primary);
  color: white;
}

.progress-step.completed .step-number {
  background: var(--color-success);
  border-color: var(--color-success);
  color: white;
}

.step-title {
  font-size: 12px;
  color: var(--color-text-secondary);
  font-weight: 500;
}

.progress-step.active .step-title {
  color: var(--juwo-primary);
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: var(--color-bg-hover);
  color: var(--color-text-primary);
}

/* 内容区域 */
.wizard-content {
  flex: 1;
  padding: 32px;
  overflow-y: auto;
}

.step-content {
  max-width: 600px;
  margin: 0 auto;
}

.step-heading {
  font-size: 24px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 8px;
}

.step-description {
  font-size: 16px;
  color: var(--color-text-secondary);
  margin: 0 0 32px;
}

/* 已选区域 */
.selected-areas {
  margin-bottom: 24px;
}

.area-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 16px;
  background: var(--color-bg-card);
  border: 1px solid var(--color-border-default);
  border-radius: 8px;
}

.area-chip {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: var(--juwo-primary);
  color: white;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
}

.remove-btn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
  padding: 0;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.2s ease;
}

.remove-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* 房型选择 */
.bedroom-options {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 32px;
}

.bedroom-btn {
  padding: 16px 24px;
  border: 2px solid var(--color-border-default);
  border-radius: 8px;
  background: white;
  color: var(--color-text-primary);
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 80px;
}

.bedroom-btn:hover {
  border-color: var(--juwo-primary);
  color: var(--juwo-primary);
}

.bedroom-btn.active {
  background: var(--juwo-primary);
  border-color: var(--juwo-primary);
  color: white;
}

/* 筛选组 */
.filter-group {
  margin-bottom: 32px;
}

.group-label {
  display: block;
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 16px;
}

.price-display {
  font-size: 18px;
  font-weight: 600;
  color: var(--juwo-primary);
  margin-bottom: 16px;
}

.price-slider {
  margin: 16px 0;
}

.option-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.option-btn {
  padding: 12px 20px;
  border: 1px solid var(--color-border-default);
  border-radius: 6px;
  background: white;
  color: var(--color-text-primary);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.option-btn:hover {
  border-color: var(--juwo-primary);
  color: var(--juwo-primary);
}

.option-btn.active {
  background: var(--juwo-primary);
  border-color: var(--juwo-primary);
  color: white;
}

.furnished-toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  background: var(--color-bg-card);
  border: 1px solid var(--color-border-default);
  border-radius: 8px;
}

/* 日期选择 */
.date-inputs {
  display: flex;
  align-items: center;
  gap: 16px;
}

.date-picker {
  flex: 1;
}

.date-separator {
  color: var(--color-text-secondary);
  font-weight: 500;
}

/* 条件总结 */
.conditions-summary {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border-default);
  border-radius: 8px;
  padding: 24px;
  margin-top: 32px;
}

.conditions-summary h4 {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 16px;
}

.summary-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.summary-item {
  display: flex;
  align-items: center;
}

.item-label {
  font-weight: 500;
  color: var(--color-text-secondary);
  min-width: 80px;
}

.item-value {
  color: var(--color-text-primary);
  font-weight: 500;
}

/* 预览计数 */
.step-preview {
  margin-top: 32px;
  padding: 20px;
  background: var(--color-bg-card);
  border: 1px solid var(--color-border-default);
  border-radius: 8px;
  text-align: center;
}

.preview-count {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 16px;
}

.count-number {
  font-size: 24px;
  font-weight: 700;
  color: var(--juwo-primary);
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid var(--color-border-default);
  border-top: 2px solid var(--juwo-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.error-text {
  color: var(--color-error);
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 底部操作栏 */
.wizard-footer {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px;
  border-top: 1px solid var(--color-border-default);
  background: var(--color-bg-card);
}

.footer-spacer {
  flex: 1;
}

.btn-secondary {
  padding: 12px 24px;
  border: 1px solid var(--color-border-default);
  border-radius: 6px;
  background: white;
  color: var(--color-text-primary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  border-color: var(--color-border-strong);
  background: var(--color-bg-hover);
}

.btn-primary {
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  background: var(--juwo-primary);
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover:not(:disabled) {
  background: var(--juwo-primary-light);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.search-btn {
  padding: 14px 32px;
  font-size: 16px;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .filter-wizard-panel {
    width: 95vw;
    max-height: 95vh;
  }

  .wizard-header {
    padding: 16px;
  }

  .wizard-progress {
    gap: 16px;
  }

  .step-number {
    width: 28px;
    height: 28px;
    font-size: 12px;
  }

  .step-title {
    font-size: 11px;
  }

  .wizard-content {
    padding: 20px;
  }

  .step-heading {
    font-size: 20px;
  }

  .bedroom-options {
    gap: 8px;
  }

  .bedroom-btn {
    padding: 12px 16px;
    font-size: 14px;
    min-width: 60px;
  }

  .date-inputs {
    flex-direction: column;
    align-items: stretch;
  }

  .date-separator {
    text-align: center;
  }
}
</style>
