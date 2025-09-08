<template>
  <div class="availability-filter-panel">

    <!-- 面板内容 -->
    <div class="panel-content">
      <!-- 日期选择 -->
      <div class="date-picker-group">
        <el-date-picker
          v-model="localStartDate"
          type="date"
          :placeholder="startDateLabel"
          size="large"
          class="date-picker-start filter-field"
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
          class="date-picker-end filter-field"
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
        <BaseButton variant="secondary" @click="$emit('close')">
          {{ cancelLabel }}
        </BaseButton>
        <BaseButton
          variant="primary"
          :loading="countLoading"
          :disabled="!isDateRangeValid"
          @click="applyFilters"
        >
          {{ applyText }}
        </BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject, computed, watch, onMounted } from 'vue'
import { usePropertiesStore } from '@/stores/properties'
import { useRouter } from 'vue-router'
import BaseButton from '@/components/base/BaseButton.vue'

// 中文注释：空出时间筛选专用面板，拆分自原 FilterPanel

const emit = defineEmits(['close'])

// 路由：用于 URL Query 同步
const router = useRouter()

// 注入轻量 i18n（默认 zh-CN；若未提供则回退为 key）
const t = inject('t') || ((k) => k)

// 文案回退，避免显示未注册的 key

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

/* 实时计数：应用（N） */
const previewCount = ref(null)
const countLoading = ref(false)
let _countTimer = null
const applyText = computed(() => {
  // 中文注释：当有计数结果时展示“应用（N）”，否则显示“应用”
  if (typeof previewCount.value === 'number') return `应用（${previewCount.value}）`
  return '应用'
})

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

/* 构建筛选参数（仅空出时间草稿） */
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

/* 计算预估数量：与当前已应用条件合并，然后覆盖空出时间为草稿值 */
const computePreviewCount = async () => {
  try {
    countLoading.value = true
    const draft = buildFilterParams()
    // 中文注释：将“空出时间”面板草稿合入全局草稿，由 Store 统一计算预览计数（与其它面板口径一致）
    propertiesStore.updatePreviewDraft('availability', draft)
    const n = await propertiesStore.getPreviewCount()
    previewCount.value = Number.isFinite(n) ? n : 0
  } catch (err) {
    previewCount.value = null
    console.warn('获取空出时间预估数量失败', err)
  } finally {
    countLoading.value = false
  }
}

/* 监听日期变化，300ms 防抖后触发计数；挂载后也计算一次 */
watch([localStartDate, localEndDate], () => {
  if (_countTimer) clearTimeout(_countTimer)
  _countTimer = setTimeout(() => computePreviewCount(), 300)
})
onMounted(() => {
  computePreviewCount()
})

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

    // 中文注释：应用成功后清理“空出时间”分组的预览草稿，防止下次打开显示过期草稿计数
    propertiesStore.clearPreviewDraft('availability')

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
  background: var(--filter-panel-bg);
  border-radius: var(--filter-panel-radius);
}

/* 面板内容 */
.panel-content {
  padding: var(--filter-panel-padding);
}

/* 日期选择器 */
.date-picker-group {
  display: flex;
  align-items: center;
  gap: var(--filter-space-md);
  margin-bottom: var(--filter-space-xl);
}

.date-picker-start,
.date-picker-end {
  flex: 1;
}

.date-separator {
  color: var(--filter-color-text-secondary);
  margin: 0 var(--filter-space-xs);
  font-weight: var(--filter-font-weight-medium);
}

/* 焦点态：中性灰细边框，移除黑色外框 */
:deep(.el-input.is-focus .el-input__wrapper) {
  outline: none !important;
  box-shadow: 0 0 0 1px var(--color-border-default) !important;
}

/* 收紧日期输入右侧内边距，避免右侧空白过大（改用 Filter Field 令牌，PC 作用域可被局部变量覆盖） */
:deep(.el-date-editor .el-input__wrapper) {
  padding-right: calc(
    var(--filter-suffix-right, var(--search-suffix-right, 12px)) +
    var(--filter-suffix-hit, var(--search-suffix-hit, 28px))
  ) !important;
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
  color: var(--filter-color-danger);
  font-size: var(--filter-font-size-md);
  margin-top: var(--filter-space-md);
  margin-bottom: var(--filter-space-xl);
  font-weight: var(--filter-font-weight-medium);
}

/* 底部操作按钮 */
.panel-footer {
  display: flex;
  gap: var(--filter-space-lg);
  margin-top: var(--filter-space-3xl);
}
</style>
