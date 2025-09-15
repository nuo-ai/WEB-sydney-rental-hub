<template>
  <div class="price-filter-panel">
    <!-- 面板内容 -->
    <div class="panel-content">
      <!-- 价格范围标题 -->
      <div class="price-range-header">
        <h4 class="price-range-title">Price Range</h4>
      </div>

      <!-- 价格选择器 - 水平布局 -->
      <div class="price-selectors-horizontal">
        <div class="price-selector-group">
          <label class="selector-label">Minimum</label>
          <el-select
            v-model="minPriceSelected"
            filterable
            allow-create
            placeholder="No Min"
            class="price-select"
          >
            <el-option label="No Min" value="0" />
            <el-option label="$200" value="200" />
            <el-option label="$400" value="400" />
            <el-option label="$600" value="600" />
            <el-option label="$800" value="800" />
            <el-option label="$1000" value="1000" />
            <el-option label="$1200" value="1200" />
            <el-option label="$1500" value="1500" />
            <el-option label="$2000" value="2000" />
            <el-option label="$2500" value="2500" />
            <el-option label="$3000" value="3000" />
          </el-select>
        </div>

        <div class="price-separator">—</div>

        <div class="price-selector-group">
          <label class="selector-label">Maximum</label>
          <el-select
            v-model="maxPriceSelected"
            filterable
            allow-create
            placeholder="No Max"
            class="price-select"
          >
            <el-option label="$200" value="200" />
            <el-option label="$400" value="400" />
            <el-option label="$600" value="600" />
            <el-option label="$800" value="800" />
            <el-option label="$1000" value="1000" />
            <el-option label="$1200" value="1200" />
            <el-option label="$1500" value="1500" />
            <el-option label="$2000" value="2000" />
            <el-option label="$2500" value="2500" />
            <el-option label="$3000" value="3000" />
            <el-option label="$4000" value="4000" />
            <el-option label="$5000" value="5000" />
            <el-option label="No Max" value="5000" />
          </el-select>
        </div>
      </div>
      <span class="sr-only" aria-live="polite">{{ priceRangeText }}</span>

      <!-- 底部操作按钮 -->
      <div class="panel-footer">
        <BaseButton variant="ghost" size="small" @click="clearAll">清除</BaseButton>
        <el-button class="cancel-btn" size="default" @click="$emit('close')">
          取消
        </el-button>
        <el-button
          type="primary"
          class="apply-btn"
          size="default"
          @click="applyFilters"
        >
          {{ applyText }}
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject, computed, watch, onMounted } from 'vue'
import { usePropertiesStore } from '@/stores/properties'
import { useRouter } from 'vue-router'
import { sanitizeQueryParams, isSameQuery } from '@/utils/query'
import BaseButton from '@/components/base/BaseButton.vue'
import { useFilterPreviewCount } from '@/composables/useFilterPreviewCount'

// 中文注释：价格筛选专用面板，拆分自原 FilterPanel

const emit = defineEmits(['close'])

// 路由：用于 URL Query 同步
const router = useRouter()

// 注入轻量 i18n（默认 zh-CN；若未提供则回退为 key）
const t = inject('t') || ((k) => k)

// 文案回退，避免显示未注册的 key

const anyPriceLabel = computed(() => {
  const v = t('filter.anyPrice')
  return v && v !== 'filter.anyPrice' ? v : '不限价格'
})

// 状态管理
const propertiesStore = usePropertiesStore()

// 从 store 中获取当前筛选状态（仅用于初始化本地状态）
const initialPriceRange = computed(() => {
  const currentFilters = propertiesStore.currentFilterParams || {}
  const min = parseInt(currentFilters.minPrice || 0)
  const max = parseInt(currentFilters.maxPrice || 5000)
  return [isNaN(min) ? 0 : min, isNaN(max) ? 5000 : max]
})

// 本地状态（用于保存用户选择，但不立即应用）
const localPriceRange = ref([...initialPriceRange.value])

// 中文注释：价格常量（周租 AUD）
const MIN_PRICE = 0
const MAX_PRICE = 5000

// 下拉选择器的状态 - 初始化时考虑边界值的显示
const minPriceSelected = ref(localPriceRange.value[0] === MIN_PRICE ? '0' : localPriceRange.value[0].toString())
const maxPriceSelected = ref(localPriceRange.value[1] === MAX_PRICE ? '5000' : localPriceRange.value[1].toString())

/* 实时计数：应用（N） - 使用通用 composable 统一管理（防抖 + 并发守卫 + 卸载清理） */
const { previewCount, scheduleCompute, computeNow } = useFilterPreviewCount(
  'price',
  () => buildFilterParams(),
  { debounceMs: 300 },
)
const applyText = computed(() =>
  typeof previewCount.value === 'number' ? `应用（${previewCount.value}）` : '应用',
)


/* 监听价格范围变化，防抖触发计数（统一经由 composable） */
watch(localPriceRange, () => {
  scheduleCompute()
})

/* 监听下拉选择器的值变化，同步到 localPriceRange */
watch(minPriceSelected, (newValue) => {
  const validatedMin = validatePriceInput(newValue)
  const currentMax = localPriceRange.value[1]

  // 确保最小值不大于最大值
  if (validatedMin > currentMax) {
    localPriceRange.value = [validatedMin, validatedMin]
    maxPriceSelected.value = validatedMin.toString()
  } else {
    localPriceRange.value = [validatedMin, currentMax]
  }
})

watch(maxPriceSelected, (newValue) => {
  const validatedMax = validatePriceInput(newValue)
  const currentMin = localPriceRange.value[0]

  // 确保最大值不小于最小值
  if (validatedMax < currentMin) {
    localPriceRange.value = [validatedMax, validatedMax]
    minPriceSelected.value = validatedMax.toString()
  } else {
    localPriceRange.value = [currentMin, validatedMax]
  }
})

onMounted(() => {
  // 初次打开计算一次预估数
  void computeNow()
})

// 价格范围文本显示
const priceRangeText = computed(() => {
  const [min, max] = localPriceRange.value
  const fmt = (n) => Number(n).toLocaleString()
  const isAny = min === MIN_PRICE && max === MAX_PRICE
  if (isAny) return anyPriceLabel.value
  if (min === MIN_PRICE) return `≤$${fmt(max)}/周`
  if (max === MAX_PRICE) return `≥$${fmt(min)}/周`
  return `$${fmt(min)} - $${fmt(max)}/周`
})

// 输入验证和格式化函数
const validatePriceInput = (value) => {
  // 移除非数字字符，保留数字
  const numStr = String(value).replace(/[^\d]/g, '')
  const num = parseInt(numStr) || 0
  // 限制在合理范围内
  return Math.max(0, Math.min(num, 10000))
}


const clearAll = () => {
  localPriceRange.value = [MIN_PRICE, MAX_PRICE]
  minPriceSelected.value = MIN_PRICE.toString()
  maxPriceSelected.value = MAX_PRICE.toString()
  // 交由 composable 清理/标记与触发（空草稿会自动从 base 中剔除旧键）
  scheduleCompute()
}

// 构建筛选参数
const buildFilterParams = () => {
  const filterParams = {}

  // 价格范围
  const [min, max] = localPriceRange.value
  if (min > MIN_PRICE) {
    filterParams.minPrice = min.toString()
  }
  if (max < MAX_PRICE) {
    filterParams.maxPrice = max.toString()
  }

  return filterParams
}

// 将筛选参数添加到 URL
const updateUrlQuery = async (filterParams) => {
  try {
    const currentQuery = { ...(router.currentRoute.value.query || {}) }
    const merged = { ...currentQuery }

    // 更新价格参数（仅保留非空键）
    if (filterParams.minPrice) {
      merged.minPrice = filterParams.minPrice
    } else {
      delete merged.minPrice
    }

    if (filterParams.maxPrice) {
      merged.maxPrice = filterParams.maxPrice
    } else {
      delete merged.maxPrice
    }

    // 写入前做 sanitize，并与当前对比；相同则不写，避免无意义 replace 循环
    const nextQuery = sanitizeQueryParams(merged)
    const currQuery = sanitizeQueryParams(currentQuery)
    if (!isSameQuery(currQuery, nextQuery)) {
      await router.replace({ query: nextQuery })
    }
  } catch (e) {
    console.warn('同步 URL 查询参数失败:', e)
  }
}

// 应用筛选
const applyFilters = async () => {
  try {
    const filterParams = buildFilterParams()

    // 应用筛选
    await propertiesStore.applyFilters(filterParams, { sections: ['price'] })

    // 更新 URL
    await updateUrlQuery(filterParams)

    // 中文注释：应用成功后清理“价格”分组的预览草稿，防止下次打开显示过期草稿计数
    propertiesStore.clearPreviewDraft('price')

    // 关闭面板
    emit('close')
  } catch (error) {
    console.error('应用价格筛选失败:', error)
  }
}
</script>

<style scoped>
.price-filter-panel {
  width: 100%;
  background: var(--filter-panel-bg);
  border-radius: var(--filter-panel-radius);
}

/* 面板头部 */
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--filter-panel-padding);
  border-bottom: 1px solid var(--filter-panel-header-border);
}

.panel-title {
  font-size: var(--filter-panel-title-font-size);
  font-weight: var(--filter-panel-title-font-weight);
  color: var(--filter-panel-title-color);
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: var(--filter-close-btn-color);
  cursor: pointer;
  padding: var(--filter-close-btn-padding);
  border-radius: var(--filter-close-btn-radius);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--filter-transition-fast);
}

.close-btn:hover {
  background: var(--filter-close-btn-hover-bg);
  color: var(--filter-close-btn-hover-color);
}

.spec-icon {
  width: var(--filter-close-btn-size);
  height: var(--filter-close-btn-size);
}

/* 面板内容 */
.panel-content {
  padding: var(--filter-panel-padding);
}

/* 价格范围标题 */
.price-range-header {
  margin-bottom: var(--filter-space-lg);
}

.price-range-title {
  font-size: var(--filter-font-size-md);
  font-weight: var(--filter-font-weight-semibold);
  color: var(--filter-color-text-primary);
  margin: 0;
}

/* 水平布局的价格选择器容器 */
.price-selectors-horizontal {
  display: flex;
  align-items: flex-end;
  gap: var(--filter-space-md);
  margin-bottom: var(--filter-space-xl);
}

.price-selector-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--filter-space-sm);
}

.selector-label {
  font-size: var(--filter-font-size-sm);
  font-weight: var(--filter-font-weight-medium);
  color: var(--filter-color-text-secondary);
  margin-bottom: var(--filter-space-xs);
}

.price-select {
  width: 100%;
}

/* 价格分隔符 */
.price-separator {
  color: var(--filter-color-text-secondary);
  font-size: var(--filter-font-size-md);
  font-weight: var(--filter-font-weight-medium);
  padding: 0 var(--filter-space-xs);
  margin-bottom: var(--filter-space-xs);
  display: flex;
  align-items: center;
  height: 40px; /* 与下拉框高度对齐 */
}

/* Element Plus 下拉选择器样式定制 */
.price-select :deep(.el-input__wrapper) {
  border: 1px solid var(--filter-color-border-default);
  border-radius: var(--filter-radius-md);
  background: var(--filter-color-bg-primary);
  transition: var(--filter-transition-normal);
}

.price-select :deep(.el-input__wrapper:hover) {
  border-color: var(--filter-color-hover-border);
}

.price-select :deep(.el-input__wrapper.is-focus) {
  border-color: var(--juwo-primary);
  box-shadow: 0 0 0 2px rgba(var(--juwo-primary-rgb), 0.1);
}

.price-select :deep(.el-input__inner) {
  color: var(--filter-color-text-primary);
  font-size: var(--filter-font-size-md);
}

.price-select :deep(.el-input__inner::placeholder) {
  color: var(--filter-color-text-secondary);
}

/* 价格显示区域 */
.price-display {
  margin: var(--filter-space-md) 0;
  padding: var(--filter-space-md);
  background: var(--filter-color-bg-secondary);
  border-radius: var(--filter-radius-md);
  border: 1px solid var(--filter-color-border-default);
}

.price-range-text {
  font-size: var(--filter-font-size-md);
  font-weight: var(--filter-font-weight-medium);
  color: var(--filter-color-text-primary);
}

/* sr-only 用于无障碍播报 */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
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
</style>
