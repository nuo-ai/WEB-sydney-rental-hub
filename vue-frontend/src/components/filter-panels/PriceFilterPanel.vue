<template>
  <div class="price-filter-panel">
    <!-- 面板内容 -->
    <div class="panel-content">
      <!-- 数字展示（只读） -->
      <div class="price-cards">
        <div class="price-card">
          <div class="card-label chinese-text">最低价格</div>
          <div class="card-value">{{ minDisplay }}<span class="unit">/周</span></div>
        </div>
        <div class="dash">—</div>
        <div class="price-card">
          <div class="card-label chinese-text">最高价格</div>
          <div class="card-value">{{ maxDisplay }}<span class="unit">/周</span></div>
        </div>
      </div>
      <span class="sr-only" aria-live="polite">{{ priceRangeText }}</span>

      <!-- 价格范围滑块 -->
      <el-slider
        v-model="localPriceRange"
        range
        :min="MIN_PRICE"
        :max="MAX_PRICE"
        :step="STEP"
        :show-stops="false"
        class="price-slider"
        @change="handlePriceChange"
      />

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
import { ref, inject, computed } from 'vue'
import { usePropertiesStore } from '@/stores/properties'
import BaseButton from '@/components/base/BaseButton.vue'

// 中文注释：价格筛选专用面板，拆分自原 FilterPanel

const emit = defineEmits(['close'])


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

// 中文注释：价格常量与步长（周租 AUD）
const MIN_PRICE = 0
const MAX_PRICE = 5000
const STEP = 25

/* 极简：无输入框/直方图，仅展示两枚数字卡片 + 滑轨 + 清除/应用（N） */
const minDisplay = computed(() => `$${Number(localPriceRange.value[0]).toLocaleString()}`)
const maxDisplay = computed(() => `$${Number(localPriceRange.value[1]).toLocaleString()}`)

/* PC：关闭面板级计数，按钮文案固定 */
const applyText = computed(() => '应用')




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

// 价格变更处理
const handlePriceChange = () => {
  // 中文注释：滑轨已通过 watch 同步输入框，此处无需网络请求
}

const clearAll = () => {
  localPriceRange.value = [MIN_PRICE, MAX_PRICE]
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


/* PC：仅写入全局草稿，不触发查询/不改 URL；由“Save search”统一应用 */
const applyFilters = async () => {
  try {
    const filterParams = buildFilterParams()
    propertiesStore.setDraftFilters({
      minPrice: filterParams.minPrice,
      maxPrice: filterParams.maxPrice,
    })
    // 可选：清理旧的分组草稿
    if (propertiesStore?.clearPreviewDraft) {
      propertiesStore.clearPreviewDraft('price')
    }
    emit('close')
  } catch (error) {
    console.error('写入价格草稿失败:', error)
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

/* 价格显示（保留用于 aria-live 文案，不再单独居中显示） */
.price-display {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-secondary);
  margin: 0;
}

/* 数字展示卡片 */
.price-cards {
  display: flex;
  align-items: center;
  gap: var(--filter-space-lg);
  margin-bottom: var(--filter-space-md);
}

.price-card {
  flex: 1 1 0%;
  border: 1px solid var(--filter-color-border-default);
  border-radius: var(--filter-radius-lg);
  background: var(--filter-color-bg-primary);
  padding: var(--filter-space-md) var(--filter-space-lg);
  box-sizing: border-box;
}

.card-label {
  font-size: var(--filter-font-size-xs);
  color: var(--filter-color-text-secondary);
  margin-bottom: var(--filter-space-xs);
}

.card-value {
  font-size: var(--filter-font-size-lg);
  font-weight: var(--filter-font-weight-semibold);
  color: var(--filter-color-text-primary);
}

.card-value .unit {
  margin-left: var(--filter-space-xs);
  font-size: var(--filter-font-size-xs);
  color: var(--filter-color-text-secondary);
}

/* 价格滑块 */
.price-slider {
  margin: var(--filter-space-xl) 0 var(--filter-space-md) 0;
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

/* 已统一到下方 token 化样式，删除重复与硬编码块 */

/* 已统一到下方 token 化样式，删除重复与硬编码块 */

/* 已统一到下方 token 化样式，删除重复与硬编码块 */

/* 已统一到下方 token 化样式，删除重复与硬编码块 */

/* 中间连字符 */
.dash {
  color: var(--filter-color-text-secondary);
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

/* 滑块样式使用设计令牌 */
.price-slider :deep(.el-slider__runway) {
  background-color: var(--filter-color-neutral-200);
  height: 6px;
}

.price-slider :deep(.el-slider__bar) {
  background-color: var(--filter-color-neutral-500);
  height: 6px;
}

.price-slider :deep(.el-slider__button) {
  border: 3px solid var(--filter-color-neutral-500);
  background-color: var(--filter-color-bg-primary);
  width: 20px;
  height: 20px;
}

.price-slider :deep(.el-slider__button:hover) {
  border-color: var(--filter-color-neutral-600);
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
