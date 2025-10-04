<template>
  <div class="bedrooms-filter-panel">
    <!-- 面板头部 -->
    <div class="panel-header">
      <h3 class="panel-title chinese-text">{{ bedroomsLabel }}</h3>
      <button class="close-btn" tabindex="-1" @click="$emit('close')" aria-label="关闭卧室筛选面板">
        <svg
          class="spec-icon"
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          aria-hidden="true"
        >
          <path
            d="M18 6 6 18M6 6l12 12"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </button>
    </div>

    <!-- 面板内容 -->
    <div class="panel-content">
      <!-- 卧室数量选择 -->
      <div class="filter-buttons-group segmented">
        <button
          v-for="option in bedroomOptions"
          :key="option.value"
          class="filter-btn"
          :class="{ active: isBedroomSelected(option.value) }"
          :aria-pressed="isBedroomSelected(option.value)"
          @click="toggleBedroom(option.value)"
        >
          {{ option.label }}
        </button>
      </div>

      <!-- 浴室 -->
      <div class="section">
        <div class="section-label chinese-text">浴室</div>
        <div class="filter-buttons-group segmented">
          <button
            v-for="option in bathroomOptions"
            :key="option.value"
            class="filter-btn"
            :class="{ active: isBathroomSelected(option.value) }"
            :aria-pressed="isBathroomSelected(option.value)"
            @click="toggleBathroom(option.value)"
          >
            {{ option.label }}
          </button>
        </div>
      </div>

      <!-- 车位 -->
      <div class="section">
        <div class="section-label chinese-text">车位</div>
        <div class="filter-buttons-group segmented">
          <button
            v-for="option in parkingOptions"
            :key="option.value"
            class="filter-btn"
            :class="{ active: isParkingSelected(option.value) }"
            :aria-pressed="isParkingSelected(option.value)"
            @click="toggleParking(option.value)"
          >
            {{ option.label }}
          </button>
        </div>
      </div>

      <!-- 底部操作按钮 -->
      <div class="panel-footer">
        <BaseButton variant="ghost" size="small" @click="clearAll">{{ anyLabel }}</BaseButton>
        <el-button class="cancel-btn" size="default" @click="$emit('close')">
          {{ cancelLabel }}
        </el-button>
        <el-button
          type="primary"
          class="apply-btn"
          size="default"
          @click="applyFilters"
        >
          {{ applyText }}
        </el-button>
        <!-- a11y：数量变化通过 aria-live 播报 -->
        <span class="sr-only" aria-live="polite">
          {{ previewCount !== null ? '可用结果 ' + previewCount + ' 条' : '' }}
        </span>
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
// “不限”/清空 文案
const anyLabel = computed(() => {
  const v = t('filter.any')
  return v && v !== 'filter.any' ? v : '清空'
})

const cancelLabel = computed(() => {
  const v = t('filter.cancel')
  return v && v !== 'filter.cancel' ? v : '取消'
})

// 状态管理
const propertiesStore = usePropertiesStore()

// 选项数据
const bedroomOptions = [
  // 中文注释：Studio（开间）对应 bedrooms=0
  { value: '0', label: 'Studio' },
  { value: '1', label: '1' },
  { value: '2', label: '2' },
  { value: '3', label: '3' },
  { value: '4+', label: '4+' },
]

// 浴室与车位的选项（最少 N 语义）
const bathroomOptions = [
  { value: 'any', label: 'Any' },
  { value: '1', label: '1' },
  { value: '2', label: '2' },
  { value: '3+', label: '3+' },
]
const parkingOptions = [
  { value: 'any', label: 'Any' },
  { value: '1', label: '1' },
  { value: '2', label: '2' },
  { value: '3+', label: '3+' },
]

// 初始值（从已应用参数恢复），兼容 V1（字符串）与 V2（*_min）
const initialBathrooms = computed(() => {
  const cur = propertiesStore.currentFilterParams || {}
  if (cur.bathrooms) return String(cur.bathrooms).split(',')
  if (cur.bathrooms_min != null) {
    const n = Number(cur.bathrooms_min)
    if (!Number.isNaN(n)) return [n >= 3 ? '3+' : String(n)]
  }
  return []
})
const initialParking = computed(() => {
  const cur = propertiesStore.currentFilterParams || {}
  if (cur.parking) return String(cur.parking).split(',')
  if (cur.parking_min != null) {
    const n = Number(cur.parking_min)
    if (!Number.isNaN(n)) return [n >= 2 ? '2+' : String(n)]
  }
  return []
})

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
const localBathrooms = ref([...initialBathrooms.value])
const localParking = ref([...initialParking.value])

/* 结果数量预估（用于“应用（N）”）- 使用通用 composable（并发守卫 + 防抖 + 卸载清理） */
const { previewCount, scheduleCompute, computeNow } = useFilterPreviewCount(
  'bedrooms',
  () => buildFilterParamsBedroomsOnly(),
  { debounceMs: 300 },
)
const applyText = computed(() =>
  typeof previewCount.value === 'number' ? `${applyLabel.value}（${previewCount.value}）` : applyLabel.value,
)

// 清空选择（不限）
const clearAll = () => {
  // 中文注释：清空“卧室”面板所管理的全部键（卧室/浴室/车位），符合“清空仅影响当前分组”
  localBedrooms.value = []
  localBathrooms.value = []
  localParking.value = []
  propertiesStore.clearPreviewDraft('bedrooms')
  propertiesStore.markPreviewSection('bedrooms')
  scheduleCompute()
}

// 触发计数（统一经由 composable）
watch(localBedrooms, () => scheduleCompute())
watch(localBathrooms, () => scheduleCompute())
watch(localParking, () => scheduleCompute())

// 初次打开时计算一次
onMounted(() => {
  void computeNow()
})

// 判断卧室选项是否被选中
const isBedroomSelected = (value) => {
  return localBedrooms.value.includes(value)
}

// 切换卧室选择（单选逻辑）
const toggleBedroom = (value) => {
  if (localBedrooms.value.includes(value)) {
    localBedrooms.value = []
  } else {
    localBedrooms.value = [value]
  }
}

// 判断/切换 浴室
const isBathroomSelected = (value) => {
  return localBathrooms.value.includes(value)
}
const toggleBathroom = (value) => {
  if (localBathrooms.value.includes(value)) {
    localBathrooms.value = []
  } else {
    localBathrooms.value = [value]
  }
}

// 判断/切换 车位
const isParkingSelected = (value) => {
  return localParking.value.includes(value)
}
const toggleParking = (value) => {
  if (localParking.value.includes(value)) {
    localParking.value = []
  } else {
    localParking.value = [value]
  }
}


// 仅构建“卧室”分组的筛选参数（用于 per-panel 应用与预览）
const buildFilterParamsBedroomsOnly = () => {
  const filterParams = {}
  // 卧室
  if (localBedrooms.value.length > 0) {
    filterParams.bedrooms = localBedrooms.value.join(',')
  }
  // 浴室（'any' 将由 Store 映射忽略，不写 bathrooms_min）
  if (localBathrooms.value.length > 0) {
    filterParams.bathrooms = localBathrooms.value.join(',')
  }
  // 车位（'any' 将由 Store 映射忽略；'0' 如有则保留为有效值）
  if (localParking.value.length > 0) {
    filterParams.parking = localParking.value.join(',')
  }
  return filterParams
}

// 将筛选参数添加到 URL
const updateUrlQuery = async (filterParams) => {
  try {
    const currentQuery = { ...(router.currentRoute.value.query || {}) }
    const merged = { ...currentQuery }

    // 卧室
    if (filterParams.bedrooms) {
      merged.bedrooms = filterParams.bedrooms
    } else {
      delete merged.bedrooms
    }

    // 浴室：忽略 'any'
    if (filterParams.bathrooms && filterParams.bathrooms !== 'any') {
      merged.bathrooms = filterParams.bathrooms
    } else {
      delete merged.bathrooms
    }

    // 车位：忽略 'any'，保留 '0'（如存在）
    if (filterParams.parking && filterParams.parking !== 'any') {
      merged.parking = filterParams.parking
    } else {
      delete merged.parking
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
    // 中文注释：卧室面板仅提交 bedrooms，避免误改“更多”分组（浴室/车位）
    const filterParams = buildFilterParamsBedroomsOnly()

    // 应用筛选（仅 bedrooms 分组）
    await propertiesStore.applyFilters(filterParams, { sections: ['bedrooms'] })

    // 更新 URL（仅写入已应用的 bedrooms）
    await updateUrlQuery(filterParams)

    // 中文注释：应用成功后清理“卧室”分组的预览草稿
    propertiesStore.clearPreviewDraft('bedrooms')

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
  background: var(--panel-bg);
  border-radius: var(--panel-radius);
}

/* 面板头部 */
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--panel-padding);
  border-bottom: 1px solid var(--panel-header-border);
}

.panel-title {
  font-size: var(--panel-title-font-size);
  font-weight: var(--panel-title-font-weight);
  color: var(--panel-title-color);
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: var(--panel-close-color);
  cursor: pointer;
  padding: var(--panel-close-padding);
  border-radius: var(--panel-close-radius);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition-fast);
}

.close-btn:hover {
  background: var(--panel-close-hover-bg);
  color: var(--panel-close-hover-color);
}

.spec-icon {
  width: var(--panel-close-size);
  height: var(--panel-close-size);
}

/* 面板内容 */
.panel-content {
  padding: var(--space-md); /* 使用设计令牌 */
}

/* 筛选按钮组 */
.filter-buttons-group {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-sm);
  margin-bottom: var(--space-lg);
}

.filter-btn {
  padding: var(--space-md) var(--space-lg);
  border: 1px solid var(--color-border-default);
  border-radius: var(--radius-xs);
  background: var(--color-bg-primary);
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-primary);
  cursor: pointer;
  transition: var(--transition-normal);
  min-width: 60px;
}

.filter-btn:hover {
  border-color: var(--color-border-hover);
  color: var(--color-text-primary);
  background: var(--color-surface-hover);
}

.filter-btn.active {
  background: var(--color-selected-bg);
  border-color: var(--color-selected-border);
  color: var(--color-text-primary);
  font-weight: var(--font-weight-semibold);
}

/* 连体分段样式：保留现有颜色/描边/填充，仅处理连体与圆角 */
.filter-buttons-group.segmented {
  display: inline-flex;
  flex-wrap: nowrap;
  gap: 0;
  overflow: hidden;
}

.filter-buttons-group.segmented .filter-btn {
  border-radius: 0; /* 中间段无圆角 */
}

.filter-buttons-group.segmented .filter-btn + .filter-btn {
  margin-left: -1px; /* 折叠相邻边框，避免中缝变粗 */
}

/* 左右端圆角 2px */
.filter-buttons-group.segmented .filter-btn:first-child {
  border-top-left-radius: 2px;
  border-bottom-left-radius: 2px;
}

.filter-buttons-group.segmented .filter-btn:last-child {
  border-top-right-radius: 2px;
  border-bottom-right-radius: 2px;
}

/* 移动端保持连体不换行，如需可水平滚动 */
@media (width <= 767px) {
  .filter-buttons-group.segmented {
    overflow-x: auto;
  }
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

/* 小节标题 */
.section {
  margin-top: var(--space-2xs);
}

.section-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-sm);
  font-weight: var(--font-weight-medium);
}

/* 屏幕阅读器可见性辅助 */
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
