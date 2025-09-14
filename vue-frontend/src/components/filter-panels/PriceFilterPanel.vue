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
import { ref, inject, computed, watch, onMounted } from 'vue'
import { usePropertiesStore } from '@/stores/properties'
import { useRouter } from 'vue-router'
import BaseButton from '@/components/base/BaseButton.vue'

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

// 中文注释：价格常量与步长（周租 AUD）
const MIN_PRICE = 0
const MAX_PRICE = 5000
const STEP = 25

/* 极简：无输入框/直方图，仅展示两枚数字卡片 + 滑轨 + 清除/应用（N） */
const minDisplay = computed(() => `$${Number(localPriceRange.value[0]).toLocaleString()}`)
const maxDisplay = computed(() => `$${Number(localPriceRange.value[1]).toLocaleString()}`)

/* 实时计数：应用（N） */
const previewCount = ref(null)
const countLoading = ref(false)
let _countTimer = null
let _countSeq = 0 // 中文注释：计数请求序号，用于丢弃过期响应，避免“应用（N）”回退
const applyText = computed(() => {
  if (typeof previewCount.value === 'number') return `应用（${previewCount.value}）`
  return '应用'
})

const computePreviewCount = async () => {
  const seq = ++_countSeq
  try {
    countLoading.value = true
    const params = buildFilterParams()
    // 中文注释：当价格回到“不限范围”时，也要从 base 中剔除旧价位键：clear → mark，再计算预览
    if (Object.keys(params).length === 0) {
      propertiesStore.clearPreviewDraft('price')
      propertiesStore.markPreviewSection('price')
    } else {
      propertiesStore.updatePreviewDraft('price', params)
    }
    const n = await propertiesStore.getPreviewCount()
    if (seq === _countSeq) {
      previewCount.value = Number.isFinite(n) ? n : 0
    }
  } catch (err) {
    if (seq === _countSeq) {
      previewCount.value = null
    }
    console.warn('获取价格预估数量失败', err)
  } finally {
    if (seq === _countSeq) {
      countLoading.value = false
    }
  }
}

/* 监听滑轨，防抖触发计数 */
watch(localPriceRange, () => {
  if (_countTimer) clearTimeout(_countTimer)
  _countTimer = setTimeout(() => computePreviewCount(), 300)
})

onMounted(() => {
  computePreviewCount()
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

// 价格变更处理
const handlePriceChange = () => {
  // 中文注释：滑轨已通过 watch 同步输入框，此处无需网络请求
}

const clearAll = () => {
  localPriceRange.value = [MIN_PRICE, MAX_PRICE]
  // 中文注释：清理并标记该分组参与预览（即便草稿为空也删除 base 中旧键）
  propertiesStore.clearPreviewDraft('price')
  propertiesStore.markPreviewSection('price')
  if (_countTimer) clearTimeout(_countTimer)
  _countTimer = setTimeout(() => computePreviewCount(), 300)
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
    const currentQuery = { ...router.currentRoute.value.query }
    const newQuery = { ...currentQuery }

    // 更新价格参数
    if (filterParams.minPrice) {
      newQuery.minPrice = filterParams.minPrice
    } else {
      delete newQuery.minPrice
    }

    if (filterParams.maxPrice) {
      newQuery.maxPrice = filterParams.maxPrice
    } else {
      delete newQuery.maxPrice
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
