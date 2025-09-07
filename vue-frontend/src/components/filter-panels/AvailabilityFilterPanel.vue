<template>
  <div class="availability-filter-panel">
    <!-- 面板头部 -->
    <div class="panel-header">
      <h3 class="panel-title chinese-text">{{ availabilityLabel }}</h3>
      <button class="close-btn" @click="$emit('close')" aria-label="关闭空出时间筛选面板">
        <svg class="spec-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M18 6 6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </div>

    <!-- 面板内容 -->
    <div class="panel-content">
      <!-- 日期选择 -->
      <div class="date-picker-group">
        <el-date-picker
          v-model="localStartDate"
          type="date"
          :placeholder="startDateLabel"
          size="large"
          class="date-picker-start"
          :editable="false"
          :input-attrs="{ inputmode: 'none' }"
          :teleported="true"
          placement="top-start"
          @change="handleStartDateChange"
        />
        <span class="date-separator">{{ toLabel }}</span>
        <el-date-picker
          v-model="localEndDate"
          type="date"
          :placeholder="endDateLabel"
          size="large"
          class="date-picker-end"
          :editable="false"
          :input-attrs="{ inputmode: 'none' }"
          :teleported="true"
          placement="top-start"
          @change="handleEndDateChange"
        />
      </div>

      <!-- 日期选择错误提示 -->
      <div v-if="!isDateRangeValid" class="date-error">
        {{ dateErrorLabel }}
      </div>

      <!-- 底部操作按钮 -->
      <div class="panel-footer">
        <el-button class="cancel-btn" size="default" @click="$emit('close')">
          {{ cancelLabel }}
        </el-button>
        <el-button type="primary" class="apply-btn" size="default" @click="applyFilters" :disabled="!isDateRangeValid">
          {{ applyLabel }}
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject, computed } from 'vue'
import { usePropertiesStore } from '@/stores/properties'
import { useRouter } from 'vue-router'

// 中文注释：空出时间筛选专用面板，拆分自原 FilterPanel

const emit = defineEmits(['close'])

// 路由：用于 URL Query 同步
const router = useRouter()

// 注入轻量 i18n（默认 zh-CN；若未提供则回退为 key）
const t = inject('t') || ((k) => k)

// 文案回退，避免显示未注册的 key
const availabilityLabel = computed(() => {
  const v = t('filter.date')
  return v && v !== 'filter.date' ? v : '空出时间'
})

const startDateLabel = computed(() => {
  const v = t('filter.dateStart')
  return v && v !== 'filter.dateStart' ? v : '开始日期'
})

const endDateLabel = computed(() => {
  const v = t('filter.dateEnd')
  return v && v !== 'filter.dateEnd' ? v : '结束日期'
})

const toLabel = computed(() => {
  const v = t('filter.to')
  return v && v !== 'filter.to' ? v : '至'
})

const applyLabel = computed(() => {
  const v = t('filter.apply')
  return v && v !== 'filter.apply' ? v : '应用'
})

const cancelLabel = computed(() => {
  const v = t('filter.cancel')
  return v && v !== 'filter.cancel' ? v : '取消'
})

const dateErrorLabel = computed(() => {
  return '开始日期不能晚于结束日期'
})

// 状态管理
const propertiesStore = usePropertiesStore()

// 从 store 中获取当前筛选状态（仅用于初始化本地状态）
const initialDates = computed(() => {
  const currentFilters = propertiesStore.currentFilterParams || {}
  let startDate = null
  let endDate = null

  // 解析开始日期
  if (currentFilters.date_from) {
    try {
      startDate = new Date(currentFilters.date_from)
      if (isNaN(startDate.getTime())) startDate = null
    } catch {
      startDate = null
    }
  }

  // 解析结束日期
  if (currentFilters.date_to) {
    try {
      endDate = new Date(currentFilters.date_to)
      if (isNaN(endDate.getTime())) endDate = null
    } catch {
      endDate = null
    }
  }

  return { startDate, endDate }
})

// 本地状态（用于保存用户选择，但不立即应用）
const localStartDate = ref(initialDates.value.startDate)
const localEndDate = ref(initialDates.value.endDate)

// 检查日期范围是否有效
const isDateRangeValid = computed(() => {
  if (localStartDate.value && localEndDate.value) {
    return new Date(localStartDate.value).getTime() <= new Date(localEndDate.value).getTime()
  }
  return true
})

// 处理开始日期变更
const handleStartDateChange = (date) => {
  // 若选中的开始日期晚于当前结束日期，立即"交换两端"，保持 start ≤ end
  const currentEnd = localEndDate.value
  localStartDate.value = date
  if (date && currentEnd && new Date(date).getTime() > new Date(currentEnd).getTime()) {
    localStartDate.value = currentEnd
    localEndDate.value = date
  }
}

// 处理结束日期变更
const handleEndDateChange = (date) => {
  // 若选中的结束日期早于当前开始日期，立即"交换两端"，保持 start ≤ end
  const currentStart = localStartDate.value
  localEndDate.value = date
  if (date && currentStart && new Date(date).getTime() < new Date(currentStart).getTime()) {
    localEndDate.value = currentStart
    localStartDate.value = date
  }
}

// 辅助函数：格式化日期为YYYY-MM-DD
const formatDateToYYYYMMDD = (date) => {
  if (!date) return null
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// 构建筛选参数
const buildFilterParams = () => {
  const filterParams = {}

  // 日期范围
  if (localStartDate.value) {
    filterParams.date_from = formatDateToYYYYMMDD(localStartDate.value)
  }
  if (localEndDate.value) {
    filterParams.date_to = formatDateToYYYYMMDD(localEndDate.value)
  }

  return filterParams
}

// 将筛选参数添加到 URL
const updateUrlQuery = async (filterParams) => {
  try {
    const currentQuery = { ...router.currentRoute.value.query }
    const newQuery = { ...currentQuery }

    // 更新日期参数
    if (filterParams.date_from) {
      newQuery.date_from = filterParams.date_from
    } else {
      delete newQuery.date_from
    }

    if (filterParams.date_to) {
      newQuery.date_to = filterParams.date_to
    } else {
      delete newQuery.date_to
    }

    // 仅当查询参数发生变化时才更新 URL
    if (JSON.stringify(newQuery) !== JSON.stringify(currentQuery)) {
      await router.replace({ query: newQuery })
    }
  } catch (e) {
    console.warn('同步 URL 查询参数失败:', e)
  }
}

// 应用筛选
const applyFilters = async () => {
  // 日期范围有效性检查
  if (!isDateRangeValid.value) return

  try {
    const filterParams = buildFilterParams()

    // 应用筛选
    await propertiesStore.applyFilters(filterParams)

    // 更新 URL
    await updateUrlQuery(filterParams)

    // 关闭面板
    emit('close')
  } catch (error) {
    console.error('应用日期筛选失败:', error)
  }
}
</script>

<style scoped>
.availability-filter-panel {
  width: 100%;
  background: white;
  border-radius: 8px;
}

/* 面板头部 */
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid var(--color-border-default);
}

.panel-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  background: #f5f5f5;
  color: var(--color-text-primary);
}

.spec-icon {
  width: 20px;
  height: 20px;
}

/* 面板内容 */
.panel-content {
  padding: 16px;
}

/* 日期选择器 */
.date-picker-group {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.date-picker-start,
.date-picker-end {
  flex: 1;
}

.date-separator {
  color: var(--color-text-secondary);
}

:deep(.el-date-picker__popper) {
  z-index: 10002 !important; /* 高于筛选面板 */
}

:deep(.el-popper) {
  z-index: 10002 !important;
}

:deep(.el-picker__popper) {
  z-index: 10002 !important;
}

/* 日期错误提示 */
.date-error {
  color: #f56c6c;
  font-size: 14px;
  margin-top: 8px;
  margin-bottom: 16px;
}

/* 底部操作按钮 */
.panel-footer {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.cancel-btn {
  flex: 1;
  background: white;
  border: 1px solid var(--color-border-default);
  color: var(--color-text-secondary);
}

.cancel-btn:hover {
  border-color: var(--color-border-strong);
  color: var(--color-text-primary);
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

.apply-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
