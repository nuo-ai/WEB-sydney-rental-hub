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
        <div class="location-list">
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
        </div>
      </template>

      <!-- 空状态提示移除：不显示“未选择任何区域”提示 -->

      <!-- 区域选择器 -->
      <AreasSelector
        :selected="selectedLocations"
        @update:selected="onUpdateSelectedAreas"
        @requestCount="debouncedRequestCount"
      />

      <!-- 包含周边选项（特性开关控制） -->
      <div v-if="SHOW_INCLUDE_NEARBY" class="nearby-toggle">
        <el-checkbox v-model="localIncludeNearby" @change="handleIncludeNearbyChange">
          {{ searchNearbyLabel }}
        </el-checkbox>
      </div>

      <!-- 底部操作按钮 -->
      <div class="panel-footer">
        <el-button class="cancel-btn" size="default" @click="cancelAndClose">
          {{ $t('filter.cancel') }}
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
import { ref, computed, inject, nextTick, onMounted, onUnmounted } from 'vue'
import { usePropertiesStore } from '@/stores/properties'
import { useRouter } from 'vue-router'
import AreasSelector from '@/components/AreasSelector.vue'
import BaseChip from '@/components/base/BaseChip.vue'

 // 中文注释：区域筛选专用面板，拆分自原 FilterPanel
// 中文注释：特性开关——控制“包含周边区域”UI 与透传是否启用（隐藏但保留代码，便于以后启用）
const SHOW_INCLUDE_NEARBY = false

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
const selectedLocations = computed(() => propertiesStore.draftSelectedLocations || [])

// 预览计数（应用（N））
const previewCount = ref(null)
const countLoading = ref(false)
let _countSeq = 0 // 中文注释：计数请求序号；丢弃过期响应，避免“应用（N）”被旧结果回退
const applyText = computed(() =>
  typeof previewCount.value === 'number' ? `应用（${previewCount.value}）` : '应用',
)

// 统一预览计数：将“区域”草稿合入全局草稿，由 Store 统一计算
const computePreviewCount = async () => {
  const seq = ++_countSeq
  try {
    countLoading.value = true
    const draft = buildFilterParams()
    propertiesStore.updatePreviewDraft('area', draft)
    const n = await propertiesStore.getPreviewCount()
    if (seq === _countSeq) {
      previewCount.value = Number.isFinite(n) ? n : 0
    }
  } catch (e) {
    if (seq === _countSeq) {
      previewCount.value = null
    }
    console.warn('获取区域预估数量失败', e)
  } finally {
    if (seq === _countSeq) {
      countLoading.value = false
    }
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
    propertiesStore.setDraftSelectedLocations(tempLocations)
    try { propertiesStore.markPreviewSection('area') } catch (e) { void e /* ignore non-critical */ }
    nextTick(() => computePreviewCount())
  }
}

// 清空所有区域
const clearAllLocations = () => {
  propertiesStore.setDraftSelectedLocations([])
  try { propertiesStore.markPreviewSection('area') } catch (e) { void e /* ignore non-critical */ }
  nextTick(() => computePreviewCount())
}

// 包含周边区域变更
const handleIncludeNearbyChange = () => {
  try { propertiesStore.markPreviewSection('area') } catch (e) { void e /* ignore non-critical */ }
  nextTick(() => debouncedRequestCount())
}

// 更新区域列表
const onUpdateSelectedAreas = (newList) => {
  propertiesStore.setDraftSelectedLocations(Array.isArray(newList) ? newList : [])
  try { propertiesStore.markPreviewSection('area') } catch (e) { void e /* ignore non-critical */ }
  nextTick(() => computePreviewCount())
}

// 延迟请求筛选计数
const debouncedRequestCount = (() => {
  let tid = null
  return () => {
    if (tid) clearTimeout(tid)
    tid = setTimeout(() => {
      computePreviewCount()
      tid = null
    }, 200)
  }
})()

// 首次打开时初始化草稿并计算一次
onMounted(() => {
  try {
    propertiesStore.resetDraftSelectedLocations()
  } catch {
    /* 忽略非关键错误 */
  }
  computePreviewCount()
})

// 组件卸载时清理“区域”分组草稿，避免小蓝点残留
onUnmounted(() => {
  try {
    propertiesStore.clearPreviewDraft('area')
    propertiesStore.resetDraftSelectedLocations()
  } catch {
    /* 忽略非关键错误 */
  }
})

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

  // include_nearby 作为透传参数（特性开关：隐藏则不透传）
  if (SHOW_INCLUDE_NEARBY) {
    filterParams.include_nearby = localIncludeNearby.value ? '1' : '0'
  }

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

    // include_nearby（特性开关控制）
    if (SHOW_INCLUDE_NEARBY) {
      if (filterParams.include_nearby === '1') {
        newQuery.include_nearby = '1'
      } else {
        delete newQuery.include_nearby
      }
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
const cancelAndClose = () => {
  try {
    propertiesStore.clearPreviewDraft('area')
    propertiesStore.resetDraftSelectedLocations()
  } catch {
    /* 忽略非关键错误 */
  }
  emit('close')
}

// 应用筛选
const applyFilters = async () => {
  try {
    const filterParams = buildFilterParams()

    // 更新全局状态（仅在特性开关启用时回写）
    if (SHOW_INCLUDE_NEARBY) {
      propertiesStore.includeNearby = localIncludeNearby.value
    }

    // 先应用草稿为已应用（仅区域）
    try {
      propertiesStore.applySelectedLocations()
    } catch {
      /* 忽略非关键错误 */
    }

    // 应用筛选（仅 area 分组）
    await propertiesStore.applyFilters(filterParams, { sections: ['area'] })

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
  padding-bottom: 96px; /* 中文注释：为吸底按钮预留滚动空间，避免内容被覆盖或“差一点点看不全” */
  /* 中文注释：滚动由外层 FilterDropdown 的 .filter-dropdown-content 承担，避免嵌套滚动导致 sticky 裁切 */
}

/* 中文注释：为外层滚动容器预留底部空间，确保 sticky 底部按钮完全可见，不被裁切 */
:deep(.filter-dropdown-content) {
  padding-bottom: 80px; /* 约等于按钮区高度 + 间距；若按钮尺寸有调整可微调该值 */
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
/* 默认态加固：使用设计令牌并阻断父级/UA 覆盖（消除浅蓝底） */
.location-chip :deep(.base-chip__remove) {
  background: var(--filter-chip-remove-bg) !important;
  background-color: var(--filter-chip-remove-bg) !important;
  background-image: none !important;
  border: none !important;
  color: var(--filter-chip-remove-color) !important;
  width: var(--filter-chip-remove-size);
  height: var(--filter-chip-remove-size);
  border-radius: var(--filter-chip-remove-radius);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  line-height: 1;
  padding: 0;
  cursor: pointer;
  transition: var(--filter-transition-fast);
  box-shadow: none !important;
  -webkit-appearance: none;
  appearance: none;
  -webkit-tap-highlight-color: transparent;
  flex-shrink: 0;
}

.location-chip .chip-remove:hover {
  background: var(--bg-hover);
  color: var(--color-text-primary);
}
/* 兼容 BaseChip 子元素命名，保持现有样式生效 */
/* Hover/Active 采用移除态危险色 */
.location-chip :deep(.base-chip__remove:hover),
.location-chip :deep(.base-chip__remove:active) {
  background: var(--filter-chip-remove-hover-bg) !important;
  color: var(--filter-chip-remove-hover-color) !important;
}

/* 选中/焦点保持中性 remove 背景，彻底移除浅蓝底 */
.location-chip :deep(.base-chip--selected .base-chip__remove),
.location-chip :deep(.base-chip__remove:focus),
.location-chip :deep(.base-chip__remove:focus-visible) {
  background: var(--filter-chip-remove-bg) !important;
  color: var(--filter-chip-remove-color) !important;
  outline: none !important;
  box-shadow: none !important;
  border: none !important;
  -webkit-appearance: none;
  appearance: none;
  -webkit-tap-highlight-color: transparent;
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
  z-index: 5; /* 中文注释：确保吸底按钮浮于内容之上，避免文本透出 */
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
  transition: none !important; /* 中文注释：去掉多余动效（不做渐变/过渡） */
}

.apply-btn:hover {
  background-color: var(--juwo-primary-light);
  border-color: var(--juwo-primary-light);
}
</style>
