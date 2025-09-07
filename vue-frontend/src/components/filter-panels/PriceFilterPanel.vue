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
        <button type="button" class="link-clear" @click="clearAll">清除</button>
        <el-button type="primary" class="apply-btn" size="default" :loading="countLoading" @click="applyFilters">
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
const applyText = computed(() => {
  if (typeof previewCount.value === 'number') return `应用（${previewCount.value}）`
  return '应用'
})

const computePreviewCount = async () => {
  try {
    countLoading.value = true
    const params = buildFilterParams()
    const n = await propertiesStore.getFilteredCount(params)
    previewCount.value = Number.isFinite(n) ? n : 0
  } catch (err) {
    previewCount.value = null
    console.warn('获取价格预估数量失败', err)
  } finally {
    countLoading.value = false
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
    await propertiesStore.applyFilters(filterParams)

    // 更新 URL
    await updateUrlQuery(filterParams)

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
  gap: 12px;
  margin-bottom: 8px;
}
.price-card {
  flex: 1 1 0%;
  border: 1px solid var(--color-border-default);
  border-radius: 6px;
  background: #fff;
  padding: 8px 10px;
  box-sizing: border-box;
}
.card-label {
  font-size: 12px;
  color: var(--color-text-secondary);
  margin-bottom: 4px;
}
.card-value {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
}
.card-value .unit {
  margin-left: 4px;
  font-size: 12px;
  color: var(--color-text-secondary);
}

/* 价格滑块 */
.price-slider {
  margin: 16px 0 8px 0;
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

.price-slider :deep(.el-slider__runway) {
  background-color: #e5e7eb;
  height: 6px;
}

.price-slider :deep(.el-slider__bar) {
  background-color: var(--color-border-strong);
  height: 6px;
}

.price-slider :deep(.el-slider__button) {
  border: 3px solid var(--color-border-strong);
  background-color: white;
  width: 20px;
  height: 20px;
}

.price-slider :deep(.el-slider__button:hover) {
  border-color: var(--color-border-strong);
}

/* 中间连字符 */
.dash {
  color: var(--color-text-secondary);
}

/* 底部操作按钮 */
.panel-footer {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}
.link-clear {
  background: transparent;
  border: none;
  color: var(--color-text-secondary);
  text-decoration: underline;
  cursor: pointer;
  padding: 0;
  margin-right: auto;
}
.link-clear:hover {
  color: var(--color-text-primary);
}

/* 取消按钮已移除，保留样式以兼容回滚 */

.apply-btn {
  flex: 2;
  background-color: var(--juwo-primary);
  border-color: var(--juwo-primary);
}

.apply-btn:hover {
  background-color: var(--juwo-primary-light);
  border-color: var(--juwo-primary-light);
}
</style>
