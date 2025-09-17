<template>
  <div class="search-result-header">
    <h1 class="result-title">{{ resultDescription }}</h1>
    <div class="result-meta" v-if="showMeta">
      <div class="filter-summary">
        <span class="filter-count">{{ activeFiltersCount }} 个筛选条件</span>
        <button
          v-if="activeFiltersCount > 0"
          class="clear-filters-btn"
          @click="$emit('clearFilters')"
        >
          清除全部
        </button>
      </div>
      <div class="sort-options" v-if="showSort">
        <label class="sort-label">排序：</label>
        <select
          :value="currentSort"
          @change="$emit('sortChange', $event.target.value)"
          class="sort-select"
        >
          <option value="">默认排序</option>
          <option value="rentPw">价格从低到高</option>
          <option value="rentPw_desc">价格从高到低</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// 组件属性
const props = defineProps({
  // 搜索结果总数
  totalCount: {
    type: Number,
    default: 0
  },
  // 筛选条件
  filters: {
    type: Object,
    default: () => ({})
  },
  // 是否显示元信息
  showMeta: {
    type: Boolean,
    default: true
  },
  // 是否显示排序
  showSort: {
    type: Boolean,
    default: true
  },
  // 当前排序
  currentSort: {
    type: String,
    default: ''
  }
})

// 组件事件
defineEmits(['clearFilters', 'sortChange'])

// 计算活跃筛选条件数量
const activeFiltersCount = computed(() => {
  const filters = props.filters
  let count = 0

  // 区域
  if (filters.areas && filters.areas.length > 0) count++

  // 房型
  if (filters.bedrooms) count++

  // 价格
  if (filters.priceRange) {
    const [min, max] = filters.priceRange
    if (min > 0 || max < 5000) count++
  }

  // 浴室
  if (filters.bathrooms) count++

  // 车位
  if (filters.parking) count++

  // 家具
  if (filters.furnished) count++

  // 日期
  if (filters.dateFrom || filters.dateTo) count++

  return count
})

// 生成智能的结果描述
const resultDescription = computed(() => {
  const { totalCount, filters } = props

  // 如果没有筛选条件，显示简单描述
  if (activeFiltersCount.value === 0) {
    return `共找到 ${totalCount} 套房源`
  }

  // 构建智能描述
  let description = ''

  // 区域部分
  if (filters.areas && filters.areas.length > 0) {
    const areaNames = filters.areas.map(area => area.name || area.suburb || area)
    let areaText = ''

    if (areaNames.length === 1) {
      areaText = areaNames[0]
    } else if (areaNames.length === 2) {
      areaText = areaNames.join('、')
    } else if (areaNames.length <= 4) {
      areaText = `${areaNames.slice(0, 2).join('、')} 等 ${areaNames.length} 个区域`
    } else {
      areaText = `${areaNames.slice(0, 2).join('、')} 等多个区域`
    }

    description = `在 ${areaText}`
  }

  // 房型部分
  if (filters.bedrooms) {
    const bedroomText = getBedroomText(filters.bedrooms)
    if (description) {
      description += ` 找到 ${totalCount} 套 ${bedroomText} 房源`
    } else {
      description = `找到 ${totalCount} 套 ${bedroomText} 房源`
    }
  } else {
    if (description) {
      description += ` 找到 ${totalCount} 套房源`
    } else {
      description = `找到 ${totalCount} 套房源`
    }
  }

  // 添加价格信息（如果有）
  if (filters.priceRange) {
    const [min, max] = filters.priceRange
    if (min > 0 || max < 5000) {
      let priceText = ''
      if (min > 0 && max < 5000) {
        priceText = `，周租金 $${min}-$${max}`
      } else if (min > 0) {
        priceText = `，周租金 $${min} 以上`
      } else if (max < 5000) {
        priceText = `，周租金 $${max} 以下`
      }
      description += priceText
    }
  }

  // 添加其他条件
  const otherConditions = []

  if (filters.bathrooms) {
    otherConditions.push(`${getBathroomText(filters.bathrooms)}浴室`)
  }

  if (filters.parking) {
    otherConditions.push(`${getParkingText(filters.parking)}车位`)
  }

  if (filters.furnished) {
    otherConditions.push('有家具')
  }

  if (otherConditions.length > 0) {
    description += `，${otherConditions.join('、')}`
  }

  return description
})

// 辅助函数
const getBedroomText = (bedrooms) => {
  if (!bedrooms) return ''
  if (bedrooms === '0') return 'Studio'
  if (bedrooms === '4+') return '4房及以上'
  return `${bedrooms}房`
}

const getBathroomText = (bathrooms) => {
  if (!bathrooms || bathrooms === 'any') return ''
  if (bathrooms === '3+') return '3个及以上'
  return `${bathrooms}个`
}

const getParkingText = (parking) => {
  if (!parking || parking === 'any') return ''
  if (parking === '3+') return '3个及以上'
  return `${parking}个`
}
</script>

<style scoped>
.search-result-header {
  padding: 24px 0;
  border-bottom: 1px solid var(--color-border-default);
  margin-bottom: 24px;
}

.result-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 16px;
  line-height: 1.3;
}

.result-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  flex-wrap: wrap;
}

.filter-summary {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-count {
  font-size: 14px;
  color: var(--color-text-secondary);
  font-weight: 500;
}

.clear-filters-btn {
  background: none;
  border: 1px solid var(--color-border-default);
  color: var(--color-text-secondary);
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-filters-btn:hover {
  border-color: var(--color-border-strong);
  color: var(--color-text-primary);
  background: var(--color-bg-hover);
}

.sort-options {
  display: flex;
  align-items: center;
  gap: 8px;
}

.sort-label {
  font-size: 14px;
  color: var(--color-text-secondary);
  font-weight: 500;
}

.sort-select {
  padding: 6px 12px;
  border: 1px solid var(--color-border-default);
  border-radius: 4px;
  background: white;
  color: var(--color-text-primary);
  font-size: 14px;
  cursor: pointer;
  transition: border-color 0.2s ease;
}

.sort-select:hover {
  border-color: var(--color-border-strong);
}

.sort-select:focus {
  outline: none;
  border-color: var(--juwo-primary);
  box-shadow: 0 0 0 2px rgba(var(--juwo-primary-rgb), 0.1);
}

/* 移动端适配 */
@media (max-width: 768px) {
  .search-result-header {
    padding: 16px 0;
  }

  .result-title {
    font-size: 22px;
    margin-bottom: 12px;
  }

  .result-meta {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }

  .filter-summary {
    justify-content: space-between;
  }

  .sort-options {
    justify-content: space-between;
  }
}

/* 响应式字体大小 */
@media (max-width: 480px) {
  .result-title {
    font-size: 20px;
    line-height: 1.4;
  }
}
</style>
