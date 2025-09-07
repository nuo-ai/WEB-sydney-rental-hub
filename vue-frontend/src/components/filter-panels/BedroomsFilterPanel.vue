<template>
  <div class="bedrooms-filter-panel">
    <!-- 面板头部 -->
    <div class="panel-header">
      <h3 class="panel-title chinese-text">{{ bedroomsLabel }}</h3>
      <button class="close-btn" @click="$emit('close')" aria-label="关闭卧室筛选面板">
        <svg class="spec-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M18 6 6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </div>

    <!-- 面板内容 -->
    <div class="panel-content">
      <!-- 卧室数量选择 -->
      <div class="filter-buttons-group">
        <button
          v-for="option in bedroomOptions"
          :key="option.value"
          class="filter-btn"
          :class="{ active: isBedroomSelected(option.value) }"
          @click="toggleBedroom(option.value)"
        >
          {{ option.label }}
        </button>
      </div>

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

// 中文注释：卧室筛选专用面板，拆分自原 FilterPanel

const emit = defineEmits(['close'])

// 路由：用于 URL Query 同步
const router = useRouter()

// 注入轻量 i18n（默认 zh-CN；若未提供则回退为 key）
const t = inject('t') || ((k) => k)

// 文案回退，避免显示未注册的 key
const bedroomsLabel = computed(() => {
  const v = t('filter.bedrooms')
  return v && v !== 'filter.bedrooms' ? v : '卧室'
})

const applyLabel = computed(() => {
  const v = t('filter.apply')
  return v && v !== 'filter.apply' ? v : '应用'
})

const cancelLabel = computed(() => {
  const v = t('filter.cancel')
  return v && v !== 'filter.cancel' ? v : '取消'
})

// 状态管理
const propertiesStore = usePropertiesStore()

// 选项数据
const bedroomOptions = [
  { value: '1', label: '1' },
  { value: '2', label: '2' },
  { value: '3', label: '3' },
  { value: '4+', label: '4+' },
]

// 从 store 中获取当前筛选状态（仅用于初始化本地状态）
const initialBedrooms = computed(() => {
  const currentFilters = propertiesStore.currentFilterParams || {}
  if (currentFilters.bedrooms) {
    return currentFilters.bedrooms.split(',')
  }
  return []
})

// 本地状态（用于保存用户选择，但不立即应用）
const localBedrooms = ref([...initialBedrooms.value])

// 判断卧室选项是否被选中
const isBedroomSelected = (value) => {
  return localBedrooms.value.includes(value)
}

// 切换卧室选择（单选逻辑）
const toggleBedroom = (value) => {
  if (localBedrooms.value.includes(value)) {
    // 如果已选中，则取消选择
    localBedrooms.value = []
  } else {
    // 如果未选中，则选中（单选）
    localBedrooms.value = [value]
  }
}

// 构建筛选参数
const buildFilterParams = () => {
  const filterParams = {}

  // 卧室数量
  if (localBedrooms.value.length > 0) {
    filterParams.bedrooms = localBedrooms.value.join(',')
  }

  return filterParams
}

// 将筛选参数添加到 URL
const updateUrlQuery = async (filterParams) => {
  try {
    const currentQuery = { ...router.currentRoute.value.query }
    const newQuery = { ...currentQuery }

    // 更新卧室参数
    if (filterParams.bedrooms) {
      newQuery.bedrooms = filterParams.bedrooms
    } else {
      delete newQuery.bedrooms
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
    console.error('应用卧室筛选失败:', error)
  }
}
</script>

<style scoped>
.bedrooms-filter-panel {
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

/* 筛选按钮组 */
.filter-buttons-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 24px;
}

.filter-btn {
  padding: 12px 18px;
  border: 1px solid var(--color-border-default);
  border-radius: 0;
  background: white;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 60px;
}

.filter-btn:hover {
  border-color: var(--color-border-strong);
  color: var(--color-text-primary);
  background: #f7f8fa;
}

.filter-btn.active {
  background: #ffefe9; /* 极弱浅橙，非品牌强底色 */
  border-color: var(--color-border-strong);
  color: var(--color-text-primary);
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
