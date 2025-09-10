<template>
  <div class="area-filter-panel">
    <!-- 面板头部 -->
    <div class="panel-header">
      <h3 class="panel-title chinese-text">{{ locationLabel }}</h3>
      <button class="close-btn" tabindex="-1" @click="$emit('close')" aria-label="关闭区域筛选面板">
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

    <!-- 已选区域展示 -->
    <div class="panel-content">
      <!-- 已选区域列表 -->
      <template v-if="selectedLocations.length">
        <div
          class="location-list"
          :class="{ collapsed: chipsCollapsed }"
          :style="chipsCollapsed ? chipsCollapsedStyle : null"
        >
          <BaseChip
            v-for="loc in displaySelectedLocations"
            :key="loc.id"
            class="location-chip"
            :removable="true"
            :remove-label="`移除 ${loc.fullName || loc.name}`"
            @remove="removeLocation(loc.id)"
          >
            {{ formatLocation(loc) }}
          </BaseChip>
        </div>
        <div class="location-actions">
          <button class="clear-all" type="button" @click="clearAllLocations">
            {{ clearAllLabel }}
          </button>
          <button
            class="toggle-chips"
            :class="{ expanded: !chipsCollapsed }"
            type="button"
            @click="chipsCollapsed = !chipsCollapsed"
          >
            {{ chipsCollapsed ? '展开' : '收起' }}
          </button>
        </div>
      </template>

      <!-- 空状态提示 -->
      <div v-else class="location-empty">
        <div class="empty-box" role="note" aria-live="polite">
          <span class="empty-text">{{ locationEmptyLabel }}</span>
        </div>
      </div>

      <!-- 区域选择器 -->
      <AreasSelector
        :selected="selectedLocations"
        @update:selected="onUpdateSelectedAreas"
        @requestCount="debouncedRequestCount"
      />

      <!-- 包含周边选项 -->
      <div class="nearby-toggle">
        <el-checkbox v-model="localIncludeNearby" @change="handleIncludeNearbyChange">
          {{ searchNearbyLabel }}
        </el-checkbox>
      </div>

      <!-- 底部操作按钮 -->
      <div class="panel-footer">
        <el-button class="cancel-btn" size="default" @click="$emit('close')">
          {{ $t('filter.cancel') }}
        </el-button>
        <el-button
          type="primary"
          class="apply-btn"
          size="default"
          :loading="countLoading"
          @click="applyFilters"
        >
          {{ applyText }}
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, inject, nextTick, onMounted } from 'vue'
import { usePropertiesStore } from '@/stores/properties'
import { useRouter } from 'vue-router'
import AreasSelector from '@/components/AreasSelector.vue'
import BaseChip from '@/components/base/BaseChip.vue'

// 中文注释：区域筛选专用面板，拆分自原 FilterPanel

const emit = defineEmits(['close'])

// 路由：用于 URL Query 同步
const router = useRouter()

// 注入轻量 i18n（默认 zh-CN；若未提供则回退为 key）
const t = inject('t') || ((k) => k)

// 状态管理
const propertiesStore = usePropertiesStore()

// 本地状态
const localIncludeNearby = ref(propertiesStore.includeNearby ?? true) // 包含周边区域

// 计算属性
const selectedLocations = computed(() => propertiesStore.selectedLocations || [])

// 预览计数（应用（N））
const previewCount = ref(null)
const countLoading = ref(false)
const applyText = computed(() =>
  typeof previewCount.value === 'number' ? `应用（${previewCount.value}）` : '应用',
)

// 统一预览计数：将“区域”草稿合入全局草稿，由 Store 统一计算
const computePreviewCount = async () => {
  try {
    countLoading.value = true
    const draft = buildFilterParams()
    propertiesStore.updatePreviewDraft('area', draft)
    const n = await propertiesStore.getPreviewCount()
    previewCount.value = Number.isFinite(n) ? n : 0
  } catch (e) {
    previewCount.value = null
    console.warn('获取区域预估数量失败', e)
  } finally {
    countLoading.value = false
  }
}

// 中文注释：显示层去重（相同 suburb 只显示一个 chip；postcode 原样保留）并统一仅显示 suburb 名称
const displaySelectedLocations = computed(() => {
  const map = new Map()
  for (const loc of selectedLocations.value) {
    if (!loc) continue
    if (loc.type === 'suburb') {
      const key = `suburb_${loc.name}`
      if (!map.has(key)) map.set(key, { ...loc, fullName: loc.name })
    } else {
      map.set(loc.id, loc)
    }
  }
  return Array.from(map.values())
})

// 中文注释：PC 收起2行、Mobile 收起1行；用近似像素高度控制，避免复杂测量
const isMobile = typeof window !== 'undefined' ? window.innerWidth <= 767 : false
const chipsCollapsed = ref(true)
const chipsCollapsedStyle = computed(() => ({
  maxHeight: isMobile ? '36px' : '64px',
  overflow: 'hidden',
}))

// 文案回退，避免显示未注册的 key
const searchNearbyLabel = computed(() => {
  const v = t('filter.searchNearby')
  return v && v !== 'filter.searchNearby' ? v : '包含周边区域'
})

const locationLabel = computed(() => {
  const v = t('filter.location')
  return v && v !== 'filter.location' ? v : '区域'
})

const clearAllLabel = computed(() => {
  const v = t('filter.clearAll')
  return v && v !== 'filter.clearAll' ? v : '清空全部'
})

const locationEmptyLabel = computed(() => {
  const v = t('filter.locationEmpty')
  return v && v !== 'filter.locationEmpty' ? v : '未选择任何区域'
})

// 格式化区域显示（仅展示 suburb 名称；postcode 仅显示自身）
const formatLocation = (loc) => {
  if (!loc) return ''
  return loc.type === 'suburb' ? String(loc.name || '') : String(loc.name || '')
}

// 移除单个区域
const removeLocation = (id) => {
  const tempLocations = [...selectedLocations.value]
  const index = tempLocations.findIndex((loc) => loc.id === id)
  if (index !== -1) {
    tempLocations.splice(index, 1)
    propertiesStore.setSelectedLocations(tempLocations)
    nextTick(() => debouncedRequestCount())
  }
}

// 清空所有区域
const clearAllLocations = () => {
  propertiesStore.setSelectedLocations([])
  // 中文注释：清理“区域”分组的全局草稿，避免残留影响其它面板的预览口径
  propertiesStore.clearPreviewDraft('area')
  nextTick(() => debouncedRequestCount())
}

// 包含周边区域变更
const handleIncludeNearbyChange = () => {
  nextTick(() => debouncedRequestCount())
}

// 更新区域列表
const onUpdateSelectedAreas = (newList) => {
  propertiesStore.setSelectedLocations(Array.isArray(newList) ? newList : [])
  nextTick(() => debouncedRequestCount())
}

// 延迟请求筛选计数
const debouncedRequestCount = (() => {
  let tid = null
  return () => {
    if (tid) clearTimeout(tid)
    tid = setTimeout(() => {
      computePreviewCount()
      tid = null
    }, 250)
  }
})()

// 首次打开时计算一次
onMounted(() => computePreviewCount())

// 构建筛选参数
const buildFilterParams = () => {
  const filterParams = {}

  // 添加已选择的区域
  const selectedSuburbs = selectedLocations.value
    .filter((loc) => loc.type === 'suburb')
    .map((loc) => loc.name)
  if (selectedSuburbs.length > 0) {
    filterParams.suburb = selectedSuburbs.join(',')
  }

  // 支持 postcodes（与 suburbs 区分；CSV）
  const selectedPostcodes = selectedLocations.value
    .filter((loc) => loc.type === 'postcode')
    .map((loc) => loc.name)
  if (selectedPostcodes.length > 0) {
    filterParams.postcodes = selectedPostcodes.join(',')
  }

  // include_nearby 作为透传参数
  filterParams.include_nearby = localIncludeNearby.value ? '1' : '0'

  return filterParams
}

// 将筛选参数添加到 URL
const updateUrlQuery = async (filterParams) => {
  try {
    const currentQuery = { ...router.currentRoute.value.query }
    const newQuery = { ...currentQuery }

    // 更新区域相关参数
    if (filterParams.suburb) {
      newQuery.suburb = filterParams.suburb
    } else {
      delete newQuery.suburb
    }

    if (filterParams.postcodes) {
      newQuery.postcodes = filterParams.postcodes
    } else {
      delete newQuery.postcodes
    }

    if (filterParams.include_nearby === '1') {
      newQuery.include_nearby = '1'
    } else {
      delete newQuery.include_nearby
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

    // 更新全局状态
    propertiesStore.includeNearby = localIncludeNearby.value

    // 应用筛选
    await propertiesStore.applyFilters(filterParams)

    // 更新 URL
    await updateUrlQuery(filterParams)

    // 应用成功后清理“区域”分组的预览草稿，防止下次打开显示过期草稿计数
    propertiesStore.clearPreviewDraft('area')

    // 关闭面板
    emit('close')
  } catch (error) {
    console.error('应用区域筛选失败:', error)
  }
}
</script>

<style scoped>
.area-filter-panel {
  width: 100%;
  background: var(--color-bg-card);
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
  background: var(--bg-hover);
  color: var(--color-text-primary);
}

.spec-icon {
  width: 20px;
  height: 20px;
}

/* 面板内容 */
.panel-content {
  padding: 16px;

  /* 中文注释：主体可滚动，底部按钮 sticky 常驻 */
  max-height: calc(100vh - 160px);
  overflow: auto;
  overscroll-behavior: contain;
}

/* 区域列表样式 */
.location-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;

  /* 新增：白底容器外观，贴近截图 */
  background: var(--color-bg-card);
  border: 1px solid var(--color-border-default);
  border-radius: 8px;
  padding: 12px;
}

.location-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  border: 1px solid var(--color-border-default);
  border-radius: 4px;
  background: var(--chip-bg);
  max-width: 200px;
  transition: all 0.15s ease;
}

.location-chip:hover {
  border-color: var(--color-border-strong);
  background: var(--chip-bg-hover);
}

.location-chip .chip-text {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}
/* 兼容 BaseChip 子元素命名，保持现有样式生效 */
.location-chip :deep(.base-chip__text) {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

.location-chip .chip-remove {
  background: var(--bg-secondary);
  border: none;
  color: var(--color-text-secondary);
  width: 16px;
  height: 16px;
  border-radius: 2px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  line-height: 1;
  padding: 0;
  cursor: pointer;
  transition: all 0.15s ease;
  flex-shrink: 0;
}
/* 兼容 BaseChip 子元素命名，保持现有样式生效 */
.location-chip :deep(.base-chip__remove) {
  background: var(--bg-secondary);
  border: none;
  color: var(--color-text-secondary);
  width: 16px;
  height: 16px;
  border-radius: 2px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  line-height: 1;
  padding: 0;
  cursor: pointer;
  transition: all 0.15s ease;
  flex-shrink: 0;
}

.location-chip .chip-remove:hover {
  background: var(--bg-hover);
  color: var(--color-text-primary);
}
/* 兼容 BaseChip 子元素命名，保持现有样式生效 */
.location-chip :deep(.base-chip__remove:hover) {
  background: var(--bg-hover);
  color: var(--color-text-primary);
}

.location-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  padding-top: 8px;
  border-top: 1px solid var(--color-border-default);
}

.clear-all {
  background: none;
  border: none;
  color: var(--color-text-secondary);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 6px;
  transition: all 0.2s ease;
  text-decoration: none;
}

.clear-all:hover {
  background: var(--bg-hover);
  color: var(--color-text-primary);
}

.toggle-chips {
  background: none;
  border: none;
  color: var(--color-text-secondary);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 6px;
  transition: all 0.2s ease;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 4px;
}

.toggle-chips:hover {
  background: var(--bg-hover);
  color: var(--color-text-primary);
}

.toggle-chips::after {
  content: '';
  width: 0;
  height: 0;
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-top: 4px solid currentcolor;
  transition: transform 0.2s ease;
}

.toggle-chips.expanded::after {
  transform: rotate(180deg);
}

/* 空态提示 */
.location-empty {
  margin-bottom: 16px;
}

.location-empty .empty-box {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: 1px solid var(--color-border-default);
  background: var(--bg-secondary);
  border-radius: 8px;
  padding: 20px 16px;
  text-align: center;
}

.location-empty .empty-text {
  font-size: 14px;
  color: var(--color-text-secondary);
  font-weight: 500;
}

/* 包含周边选项 */
.nearby-toggle {
  margin-top: 16px;
  margin-bottom: 16px;
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
}

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
}

.apply-btn:hover {
  background-color: var(--juwo-primary-light);
  border-color: var(--juwo-primary-light);
}
</style>
