<template>
  <div class="price-filter-panel">
    <!-- 面板头部 -->
    <div class="panel-header">
      <h3 class="panel-title chinese-text">{{ priceLabel }}</h3>
      <button class="close-btn" @click="$emit('close')" aria-label="关闭价格筛选面板">
        <svg class="spec-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M18 6 6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </div>

    <!-- 面板内容 -->
    <div class="panel-content">
      <!-- 价格范围显示 -->
      <div class="price-display">{{ priceRangeText }}</div>

      <!-- 价格范围滑块 -->
      <el-slider
        v-model="localPriceRange"
        range
        :min="0"
        :max="5000"
        :step="50"
        :show-stops="false"
        class="price-slider"
        @change="handlePriceChange"
      />

      <!-- 底部操作按钮 -->
      <div class="panel-footer">
        <el-button class="cancel-btn" size="default" @click="$emit('close')">
          {{ cancelLabel }}
        </el-button>
        <el-button type="primary" class="apply-btn" size="default" @click="applyFilters">
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

// 中文注释：价格筛选专用面板，拆分自原 FilterPanel

const emit = defineEmits(['close'])

// 路由：用于 URL Query 同步
const router = useRouter()

// 注入轻量 i18n（默认 zh-CN；若未提供则回退为 key）
const t = inject('t') || ((k) => k)

// 文案回退，避免显示未注册的 key
const priceLabel = computed(() => {
  const v = t('filter.priceSection')
  return v && v !== 'filter.priceSection' ? v : '价格'
})

const applyLabel = computed(() => {
  const v = t('filter.apply')
  return v && v !== 'filter.apply' ? v : '应用'
})

const cancelLabel = computed(() => {
  const v = t('filter.cancel')
  return v && v !== 'filter.cancel' ? v : '取消'
})

const anyPriceLabel = computed(() => {
  const v = t('filter.anyPrice')
  return v && v !== 'filter.anyPrice' ? v : '任意价格'
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

// 价格范围文本显示
const priceRangeText = computed(() => {
  const [min, max] = localPriceRange.value
  if (min === 0 && max === 5000) {
    return anyPriceLabel.value
  } else if (max === 5000) {
    return `$${min}+`
  } else {
    return `$${min} - $${max}`
  }
})

// 价格变更处理
const handlePriceChange = () => {
  // 仅局部更新UI，不向服务器请求数据
}

// 构建筛选参数
const buildFilterParams = () => {
  const filterParams = {}

  // 价格范围
  const [min, max] = localPriceRange.value
  if (min > 0) {
    filterParams.minPrice = min.toString()
  }
  if (max < 5000) {
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

/* 价格显示 */
.price-display {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-secondary);
  margin-bottom: 16px;
  text-align: center;
}

/* 价格滑块 */
.price-slider {
  margin: 24px 0;
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
</style>
