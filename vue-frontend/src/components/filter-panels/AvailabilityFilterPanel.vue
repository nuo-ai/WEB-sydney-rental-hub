<template>
  <div class="availability-filter-panel">
    <!-- 面板内容 -->
    <div class="panel-content">
      <!-- 日期选择 -->
      <div class="date-picker-group">
        <el-date-picker
          v-model="localRange"
          type="daterange"
          :disabled-date="disableBeforeToday"
          :start-placeholder="startDateLabel"
          :end-placeholder="endDateLabel"
          :range-separator="toLabel"
          size="large"
          class="date-range filter-field"
          :editable="false"
          :input-attrs="{ inputmode: 'none' }"
          :teleported="true"
          placement="top-start"
          popper-class="availability-date-popper"
          :unlink-panels="false"
          @change="handleRangeChange"
          @visible-change="onPickerVisibleChange"
        />
      </div>

      <!-- 日期选择错误提示 -->
      <div v-if="!isDateRangeValid" class="date-error">
        {{ dateErrorLabel }}
      </div>

      <!-- 底部操作按钮 -->
      <div class="panel-footer">
        <BaseButton variant="ghost" size="small" @click="clearAll">清空</BaseButton>
        <el-button class="cancel-btn" size="default" @click="$emit('close')">
          {{ cancelLabel }}
        </el-button>
        <el-button
          type="primary"
          class="apply-btn"
          size="default"
          :disabled="!isDateRangeValid"
          @click="applyFilters"
        >
          {{ applyText }}
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject, computed, nextTick } from 'vue'
import { usePropertiesStore } from '@/stores/properties'
import BaseButton from '@/components/base/BaseButton.vue'

// 中文注释：空出时间筛选专用面板，拆分自原 FilterPanel

const emit = defineEmits(['close'])


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

/* 本地状态（daterange 模式） */
const localRange = ref(
  initialDates.value.startDate || initialDates.value.endDate
    ? [initialDates.value.startDate, initialDates.value.endDate]
    : null,
)
/* 为向后兼容保留 computed：原有逻辑仍读取 localStartDate/localEndDate */
const localStartDate = computed(() => (localRange.value?.[0] ? localRange.value[0] : null))
const localEndDate = computed(() => (localRange.value?.[1] ? localRange.value[1] : null))

/* PC：关闭面板级计数，按钮文案固定 */
const applyText = computed(() => '应用')

// 检查日期范围是否有效
const isDateRangeValid = computed(() => {
  if (localStartDate.value && localEndDate.value) {
    return new Date(localStartDate.value).getTime() <= new Date(localEndDate.value).getTime()
  }
  return true
})

/* 处理范围变更（保持 start ≤ end） */
const handleRangeChange = (range) => {
  // 中文注释：Element Plus 已基本保证范围合法，这里兜底交换异常输入
  if (!Array.isArray(range) || range.length < 2) {
    localRange.value = null
    return
  }
  const [start, end] = range
  if (start && end && new Date(start).getTime() > new Date(end).getTime()) {
    localRange.value = [end, start]
  } else {
    localRange.value = [start || null, end || null]
  }
}

const clearAll = () => {
  // 中文注释：清空本地日期范围；PC 关闭面板级计数，不触发预估
  localRange.value = null
}

/* daterange 模式不再需要独立结束日期处理函数 */

// 辅助函数：格式化日期为YYYY-MM-DD
const formatDateToYYYYMMDD = (date) => {
  if (!date) return null
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

/* 禁用今天以前的日期（PC 分离式专用）
   说明：以“今天 00:00:00”为比较基线，严格禁用过去日期；
   前端表现：过去日期不可点击/选择；不影响 URL 幂等与仅写非空键逻辑。 */
const disableBeforeToday = (date) => {
  if (!date) return false
  const now = new Date()
  const base = new Date(now.getFullYear(), now.getMonth(), now.getDate()).getTime()
  const cand = new Date(date.getFullYear(), date.getMonth(), date.getDate()).getTime()
  return cand < base
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



/* 面板打开时对日历单元格做轻量级标注：今天之前/之后
   说明（中文注释，解释“为什么”）：
   - Element Plus 单日历不暴露 cell-class-name，无法仅用 props 精确区分“今天之前/之后”
   - 这里在弹层打开后读取“当前面板的年/月”和单元格“日”文本，构造日期并与今天比较
   - 仅添加类名 is-before-today / is-after-today，纯样式区分，不改变选择能力，避免破坏现有功能
   - 通过 MutationObserver 监听面板内部变更（切换月份/年份）后重新标注，保持一致性
*/
const observers = new WeakMap()

const onPickerVisibleChange = async (visible) => {
  await nextTick()
  const poppers = document.querySelectorAll('.availability-date-popper')
  poppers.forEach((popper) => {
    if (visible) {
      setupPopperObserver(popper)
      classifyCells(popper)
    } else {
      teardownPopperObserver(popper)
    }
  })
}

function setupPopperObserver(popper) {
  if (observers.has(popper)) return
  const observer = new MutationObserver(() => classifyCells(popper))
  observer.observe(popper, { childList: true, subtree: true })
  observers.set(popper, observer)
}

function teardownPopperObserver(popper) {
  const ob = observers.get(popper)
  if (ob) {
    ob.disconnect()
    observers.delete(popper)
  }
}


function classifyCells(rootEl) {
  const today = new Date()
  const base = new Date(today.getFullYear(), today.getMonth(), today.getDate()).getTime()

  const tds = rootEl.querySelectorAll('.el-date-table td')
  tds.forEach((td) => {
    td.classList.remove('is-before-today', 'is-after-today')

    // 跳过禁用/跨月/今天，避免与 today 样式冲突
    if (
      td.classList.contains('prev-month') ||
      td.classList.contains('next-month') ||
      td.classList.contains('disabled') ||
      td.classList.contains('today')
    ) {
      return
    }

    // 优先读取 aria-label 或 data-date（Element Plus 单元格通常携带 YYYY-MM-DD）
    const raw =
      td.getAttribute('aria-label') ||
      td.getAttribute('data-date') ||
      td.dataset?.date ||
      ''

    const ts = raw ? new Date(raw).getTime() : NaN
    if (Number.isNaN(ts)) return

    const cellBase = new Date(new Date(ts).getFullYear(), new Date(ts).getMonth(), new Date(ts).getDate()).getTime()

    if (cellBase > base) {
      td.classList.add('is-after-today')
    } else if (cellBase < base) {
      td.classList.add('is-before-today')
    }
  })
}


/* PC：仅写入全局草稿，不触发查询/不改 URL；由“Save search”统一应用 */
const applyFilters = async () => {
  if (!isDateRangeValid.value) return
  try {
    const filterParams = buildFilterParams()
    // 写入全局 draftFilters；空值代表删除键
    if (propertiesStore?.setDraftFilters) {
      propertiesStore.setDraftFilters({
        date_from: filterParams.date_from,
        date_to: filterParams.date_to,
      })
    }
    // 清理本分组预览草稿
    if (propertiesStore?.clearPreviewDraft) {
      propertiesStore.clearPreviewDraft('availability')
    }
    emit('close')
  } catch (error) {
    console.error('写入日期草稿失败:', error)
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
  gap: 12px;
  margin-top: 24px;
  position: sticky;
  bottom: 0;
  background: var(--color-bg-card);
  padding-top: 12px;
  border-top: 1px solid var(--color-border-default);
  z-index: 5;
}
/* 对齐“区域”面板的按钮样式 */
.cancel-btn {
  flex: 1;
  background: var(--color-bg-card);
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
  transition: none !important;
}
.apply-btn:hover {
  background-color: var(--juwo-primary-light);
  border-color: var(--juwo-primary-light);
}
/* 日期面板主题覆盖：今天高亮、选中主色、上下月弱化 */
/* 中文注释：仅覆盖日期面板内部元素，避免影响其他组件 */
:deep(.el-date-table td .el-date-table-cell__text) {
  border-radius: 8px;
}

/* 今天：主色描边 + 淡色背景 + 小圆点标记，便于首次打开快速定位 */
:deep(.el-date-table td.today .el-date-table-cell__text) {
  position: relative;
  border: 2px solid var(--juwo-primary); /* 设计令牌：主色描边 */
  /* 设计令牌：主色浅混合作为背景，提高辨识度且不抢选中态 */
  background-color: color-mix(in oklab, var(--juwo-primary) 12%, transparent);
  color: var(--color-text-primary); /* 设计令牌：主文案色 */
}
:deep(.el-date-table td.today .el-date-table-cell__text)::after {
  content: '';
  position: absolute;
  bottom: 6px;
  right: 6px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: var(--juwo-primary);
}

/* 选中：使用设计系统主色，文字白色，前端表现“已选中特别明确” */
:deep(.el-date-table td.current .el-date-table-cell__text),
:deep(.el-date-table td.is-selected .el-date-table-cell__text) {
  background-color: transparent !important;
  color: var(--juwo-primary) !important; /* 设计令牌：主色 */
  font-weight: var(--font-weight-bold) !important;
  border-color: transparent !important;
  box-shadow: none !important;
}

/* 范围选择（daterange）：起止主色、区间浅主色 */
:deep(.el-date-table td.start-date .el-date-table-cell__text),
:deep(.el-date-table td.end-date .el-date-table-cell__text) {
  background-color: transparent !important;
  color: var(--juwo-primary) !important; /* 设计令牌：主色 */
  font-weight: var(--font-weight-bold) !important;
  border-color: transparent !important;
  box-shadow: none !important;
}
:deep(.el-date-table td.in-range .el-date-table-cell__text) {
  /* 设计令牌：使用主色系的浅色衍生（保持与系统一致）；文字使用主文案色 */
  background-color: color-mix(in oklab, var(--juwo-primary) 12%, transparent) !important;
  color: var(--color-text-primary) !important;
}

/* 悬停/聚焦：主色浅色衍生，保证层级感 */
:deep(.el-date-table td.available:not(.current):hover .el-date-table-cell__text),
:deep(.el-date-table td:hover .el-date-table-cell__text) {
  background-color: color-mix(in oklab, var(--juwo-primary) 10%, transparent);
}

/* 上/下月弱化：对比更明确（虽非“过去/未来”，但能显著降低非当前月干扰） */
:deep(.el-date-table td.prev-month .el-date-table-cell__text),
:deep(.el-date-table td.next-month .el-date-table-cell__text) {
  color: var(--color-text-disabled);
  opacity: 0.6;
}

/* 禁用态（若业务设置了 disabled-date）：进一步降低对比，防误触 */
:deep(.el-date-table td.disabled .el-date-table-cell__text) {
  color: var(--color-text-disabled);
  opacity: 0.35;
}

/* 今天之前/之后：提升时间方向可读性（不改变可选性，仅视觉区分） */
:deep(.availability-date-popper .el-date-table td.is-before-today .el-date-table-cell__text) {
  color: var(--color-text-secondary) !important;
  opacity: 0.8 !important;
}
:deep(.availability-date-popper .el-date-table td.is-after-today .el-date-table-cell__text) {
  /* 设计令牌：主文案色 + 加粗（若无加粗令牌，则后续在全局补充） */
  color: var(--color-text-primary) !important;
  font-weight: var(--font-weight-bold) !important;
}

/* 弹出层自定义类：与筛选面板层级对齐，避免被遮住或遮错对象 */
:deep(.availability-date-popper) {
  z-index: 10002;
}

/* 移动端年份/月份切换触控增强：增大图标按钮与标题热区，便于点击 */
@media (max-width: 768px) {
  :deep(.el-date-picker__header) {
    padding: 8px 12px;
  }
  :deep(.el-date-picker__header .el-picker-panel__icon-btn) {
    width: 44px;
    height: 44px;
    border-radius: 8px;
    margin: 0 2px;
  }
  :deep(.el-date-picker__header-label) {
    padding: 6px 10px;
    min-height: 36px;
    font-size: 16px;
    border-radius: 8px;
  }
  :deep(.el-year-table td .cell),
  :deep(.el-month-table td .cell) {
    min-width: 44px;
    min-height: 36px;
    line-height: 36px;
    border-radius: 8px;
  }
}
</style>
