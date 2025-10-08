<template>
  <div v-if="visible" class="filter-panel-wrapper visible">
    <!-- 遮罩层 -->
    <div class="filter-overlay" @click="closePanel"></div>

    <!-- 筛选面板: 现在是“编排者”角色 -->
    <div ref="panelRef" class="domain-filter-panel" :class="{ visible: visible }" tabindex="-1">
      <!-- 1. 头部组件 -->
      <FilterPanelHeader @reset="resetFilters" @close="closePanel" />

      <!-- 滚动内容区 -->
      <div class="panel-content">
        <!-- 2. 位置筛选组件 -->
        <FilterSection :title="$t('filter.location')" ref="areaRef">
          <LocationFilter v-model:selected-locations="draftFilters.locations" />
        </FilterSection>

        <!-- 3. 价格范围筛选组件 -->
        <FilterSection :title="$t('filter.priceSection')" ref="priceRef">
          <PriceRangeFilter v-model:range="draftFilters.priceRange" />
        </FilterSection>

        <!-- 4. 卧室数量筛选组件 (可复用) -->
        <FilterSection :title="$t('filter.bedrooms')" ref="bedroomsRef">
          <SegmentedButtonFilter
            v-model:selected="draftFilters.bedrooms"
            :options="bedroomOptions"
            mode="single"
          />
        </FilterSection>

        <!-- 5. 更多筛选 (包含浴室/车位) -->
        <FilterSection :title="$t('filter.moreFilters')" ref="moreRef">
          <!-- 浴室 -->
          <h4 class="sub-section-title">{{ $t('filter.bathrooms') }}</h4>
          <SegmentedButtonFilter
            v-model:selected="draftFilters.bathrooms"
            :options="bathroomOptions"
            mode="single"
          />

          <!-- 车位 -->
          <h4 class="sub-section-title">{{ $t('filter.parking') }}</h4>
          <SegmentedButtonFilter
            v-model:selected="draftFilters.parking"
            :options="parkingOptions"
            mode="single"
          />
        </FilterSection>

        <!-- 6. 日期范围筛选组件 -->
        <FilterSection :title="$t('filter.date')" ref="availabilityRef">
          <DateRangeFilter
            v-model:start-date="draftFilters.startDate"
            v-model:end-date="draftFilters.endDate"
          />
        </FilterSection>

        <!-- 7. 家具筛选组件 -->
        <FilterSection :title="$t('filter.furniture')">
          <FurnishedFilter v-model:is-furnished="draftFilters.isFurnished" />
        </FilterSection>
      </div>

      <!-- 8. 底部操作组件 -->
      <FilterPanelFooter
        :count="previewCount"
        :is-loading="isPreviewLoading"
        :is-apply-disabled="!isDateRangeValid"
        @cancel="closePanel"
        @apply="applyFilters"
      />
    </div>
  </div>
</template>

<script setup>
import {
  ref,
  computed,
  watch,
  onUnmounted,
  nextTick,
  inject,
  defineComponent,
  reactive,
} from 'vue'
import { useDebounceFn } from '@vueuse/core'
import { usePropertiesStore } from '@/stores/properties'
import { ElMessage } from 'element-plus'
// 移除了 useRouter 和 useRoute，因为组件不再直接操作 URL
import AreasSelector from '@/components/AreasSelector.vue'
import { BaseChip } from '@sydney-rental-hub/ui'

// #################################################################
// # 1. COMPOSABLE 函数 (逻辑提取)
// #################################################################

/**
 * @description 管理画布外 (Off-canvas) 面板的通用副作用
 * @param {import('vue').Ref<boolean>} visible - 控制面板可见性的 ref
 */
function useOffCanvasPanel(visible) {
  const lockBodyScroll = () => {
    if (typeof document === 'undefined') return
    document.documentElement.style.overflow = 'hidden'
    document.body.style.overflow = 'hidden'
    document.body.style.position = 'fixed'
    document.body.style.width = '100%'
  }

  const unlockBodyScroll = () => {
    if (typeof document === 'undefined') return
    document.documentElement.style.overflow = ''
    document.body.style.overflow = ''
    document.body.style.position = ''
    document.body.style.width = ''
  }

  const handleKeyDown = (event) => {
    if (event.key === 'Escape') {
      visible.value = false
    }
  }

  watch(
    visible,
    (newValue) => {
      if (newValue) {
        lockBodyScroll()
        document.addEventListener('keydown', handleKeyDown)
      } else {
        unlockBodyScroll()
        document.removeEventListener('keydown', handleKeyDown)
      }
    },
    { immediate: true }
  )

  onUnmounted(() => {
    unlockBodyScroll()
    document.removeEventListener('keydown', handleKeyDown)
  })
}

/**
 * @description 获取筛选结果预览数量的逻辑
 * @param {import('vue').Ref<object>} draftFiltersRef - 包含所有草稿筛选条件的 ref
 */
function useFilterPreviewCount(draftFiltersRef) {
  const propertiesStore = usePropertiesStore()
  const count = ref(null)
  const isLoading = ref(false)
  const error = ref(null)
  let requestSequence = 0

  const formatDateToYYYYMMDD = (date) => {
    if (!date) return null
    const d = new Date(date)
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(
      d.getDate()
    ).padStart(2, '0')}`
  }

  const fetchCount = async () => {
    const currentSequence = ++requestSequence
    isLoading.value = true
    error.value = null

    // 从草稿状态构建请求参数
    const draft = draftFiltersRef.value
    const params = {
      minPrice: draft.priceRange[0] > 0 ? draft.priceRange[0] : null,
      maxPrice: draft.priceRange[1] < 5000 ? draft.priceRange[1] : null,
      bedrooms: draft.bedrooms.length > 0 ? draft.bedrooms.join(',') : null,
      bathrooms: draft.bathrooms.length > 0 ? draft.bathrooms.join(',') : null,
      parking: draft.parking.length > 0 ? draft.parking.join(',') : null,
      date_from: formatDateToYYYYMMDD(draft.startDate),
      date_to: formatDateToYYYYMMDD(draft.endDate),
      isFurnished: draft.isFurnished || null,
      suburb: draft.locations
        .filter((l) => l.type === 'suburb')
        .map((l) => l.name)
        .join(','),
      postcodes: draft.locations
        .filter((l) => l.type === 'postcode')
        .map((l) => l.name)
        .join(','),
    }

    const finalParams = Object.fromEntries(
      Object.entries(params).filter(([, v]) => v !== null && v !== '')
    )

    if (Object.keys(finalParams).length === 0) {
      count.value = propertiesStore.totalCount || 0
      isLoading.value = false
      return
    }

    try {
      const total = await propertiesStore.getFilteredCount(finalParams)
      if (currentSequence === requestSequence) {
        count.value = total
      }
    } catch (e) {
      console.error('获取筛选计数失败:', e)
      if (currentSequence === requestSequence) {
        error.value = e
        count.value = null
      }
    } finally {
      if (currentSequence === requestSequence) {
        isLoading.value = false
      }
    }
  }

  const debouncedFetchCount = useDebounceFn(fetchCount, 300, { maxWait: 800 })

  // 监听草稿变化，自动触发计数
  watch(draftFiltersRef, debouncedFetchCount, { deep: true })

  // 也提供一个立即执行的方法，用于面板打开时
  const triggerImmediateFetch = () => {
    debouncedFetchCount.flush()
  }

  return {
    count,
    isLoading,
    error,
    triggerImmediateFetch,
  }
}

// #################################################################
// # 2. 子组件定义 (组件拆分)
// #################################################################

// -----------------------------------------------------------------
// # FilterPanelHeader.vue
// -----------------------------------------------------------------
const FilterPanelHeader = defineComponent({
  name: 'FilterPanelHeader',
  emits: ['reset', 'close'],
  setup(props, { emit }) {
    const t = inject('t', (key) => key)
    return { t, emit }
  },
  template: `
    <div class="panel-header">
      <h3 class="panel-title text-xl-semibold">{{ t('filter.title') }}</h3>
      <div class="header-actions">
        <button class="reset-link text-sm-semibold" @click="emit('reset')">
          {{ t('filter.reset') }}
        </button>
        <button
          class="close-btn"
          @click="emit('close')"
          :aria-label="t('filter.aria.closePanel')"
        >
          <svg
            class="spec-icon"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24"
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
    </div>
  `,
})

// -----------------------------------------------------------------
// # FilterSection.vue
// -----------------------------------------------------------------
const FilterSection = defineComponent({
  name: 'FilterSection',
  props: {
    title: { type: String, required: true },
  },
  template: `
    <div class="filter-section">
      <h4 class="section-title text-lg-semibold">{{ title }}</h4>
      <slot></slot>
    </div>
  `,
})

// -----------------------------------------------------------------
// # LocationFilter.vue
// -----------------------------------------------------------------
const LocationFilter = defineComponent({
  name: 'LocationFilter',
  components: { BaseChip, AreasSelector },
  props: {
    selectedLocations: { type: Array, default: () => [] },
  },
  emits: ['update:selectedLocations'],
  setup(props, { emit }) {
    const t = inject('t', (key) => key)

    const displayLocations = computed(() => {
      const map = new Map()
      for (const loc of props.selectedLocations) {
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

    const onUpdateSelected = (newList) => {
      emit('update:selectedLocations', newList)
    }
    const removeLocation = (id) => {
      const newList = props.selectedLocations.filter((loc) => String(loc?.id ?? '') !== String(id))
      emit('update:selectedLocations', newList)
    }
    const clearAll = () => {
      emit('update:selectedLocations', [])
    }

    return { t, displayLocations, onUpdateSelected, removeLocation, clearAll }
  },
  template: `
    <div>
      <div v-if="selectedLocations.length > 0" class="location-list-wrapper">
        <div class="location-list">
          <BaseChip
            v-for="loc in displayLocations"
            :key="loc.id"
            class="location-chip"
            :removable="true"
            :remove-label="t('filter.aria.remove') + ' ' + (loc.fullName || loc.name)"
            @remove="removeLocation(loc.id)"
          >
            {{ loc.name || '' }}
          </BaseChip>
        </div>
        <div class="location-actions">
          <button class="clear-all-btn text-sm-semibold" type="button" @click="clearAll">
            {{ t('filter.clearAll') }}
          </button>
        </div>
      </div>
      <AreasSelector :selected="selectedLocations" @update:selected="onUpdateSelected" />
    </div>
  `,
})

// -----------------------------------------------------------------
// # PriceRangeFilter.vue
// -----------------------------------------------------------------
const PriceRangeFilter = defineComponent({
  name: 'PriceRangeFilter',
  props: {
    range: { type: Array, default: () => [0, 5000] },
  },
  emits: ['update:range'],
  setup(props, { emit }) {
    const t = inject('t', (key) => key)
    const onUpdate = (value) => {
      emit('update:range', value)
    }

    const priceRangeText = computed(() => {
      const [min, max] = props.range
      if (min === 0 && max === 5000) return t('filter.anyPrice')
      if (max === 5000) return `$${min}+`
      return `$${min} - $${max}`
    })

    return { t, onUpdate, priceRangeText }
  },
  template: `
    <div>
      <div class="section-header">
        <span class="price-display text-md-semibold">{{ priceRangeText }}</span>
      </div>
      <el-slider
        :model-value="range"
        @update:modelValue="onUpdate"
        range
        :min="0"
        :max="5000"
        :step="50"
        :show-stops="false"
        class="price-slider"
      />
    </div>
  `,
})

// -----------------------------------------------------------------
// # SegmentedButtonFilter.vue (可复用)
// -----------------------------------------------------------------
const SegmentedButtonFilter = defineComponent({
  name: 'SegmentedButtonFilter',
  props: {
    selected: { type: Array, default: () => [] },
    options: { type: Array, required: true },
    mode: { type: String, default: 'single' }, // 'single' or 'multiple'
  },
  emits: ['update:selected'],
  setup(props, { emit }) {
    const isSelected = (value) => {
      if (value === 'any') return props.selected.length === 0
      return props.selected.includes(value)
    }
    const toggleSelection = (value) => {
      if (props.mode === 'single') {
        if (value === 'any' || isSelected(value)) {
          emit('update:selected', [])
        } else {
          emit('update:selected', [value])
        }
      } else {
        const newSelection = [...props.selected]
        const index = newSelection.indexOf(value)
        if (index > -1) newSelection.splice(index, 1)
        else newSelection.push(value)
        emit('update:selected', newSelection)
      }
    }
    return { isSelected, toggleSelection }
  },
  template: `
    <div class="filter-buttons-group segmented">
      <button
        v-for="option in options"
        :key="option.value"
        :class="['filter-btn', { active: isSelected(option.value) }]"
        @click="toggleSelection(option.value)"
      >
        {{ option.label }}
      </button>
    </div>
  `,
})

// -----------------------------------------------------------------
// # DateRangeFilter.vue
// -----------------------------------------------------------------
const DateRangeFilter = defineComponent({
  name: 'DateRangeFilter',
  props: {
    startDate: { type: [Date, String, null], default: null },
    endDate: { type: [Date, String, null], default: null },
  },
  emits: ['update:startDate', 'update:endDate'],
  setup(props, { emit }) {
    const t = inject('t', (key) => key)
    const handleStartDateChange = (date) => {
      emit('update:startDate', date)
      if (date && props.endDate && new Date(date) > new Date(props.endDate)) {
        emit('update:endDate', date)
      }
    }
    const handleEndDateChange = (date) => {
      emit('update:endDate', date)
      if (date && props.startDate && new Date(date) < new Date(props.startDate)) {
        emit('update:startDate', date)
      }
    }
    return { t, handleStartDateChange, handleEndDateChange }
  },
  template: `
    <div class="date-picker-group">
      <el-date-picker
        :model-value="startDate"
        @update:modelValue="handleStartDateChange"
        type="date"
        :placeholder="t('filter.dateStart')"
        size="large"
        class="date-picker-start filter-field"
        :editable="false"
        :teleported="true"
      />
      <span class="date-separator">{{ t('filter.to') }}</span>
      <el-date-picker
        :model-value="endDate"
        @update:modelValue="handleEndDateChange"
        type="date"
        :placeholder="t('filter.dateEnd')"
        size="large"
        class="date-picker-end filter-field"
        :editable="false"
        :teleported="true"
      />
    </div>
  `,
})

// -----------------------------------------------------------------
// # FurnishedFilter.vue
// -----------------------------------------------------------------
const FurnishedFilter = defineComponent({
  name: 'FurnishedFilter',
  props: {
    isFurnished: { type: Boolean, default: false },
  },
  emits: ['update:isFurnished'],
  setup(props, { emit }) {
    const t = inject('t', (key) => key)
    const onUpdate = (value) => {
      emit('update:isFurnished', value)
    }
    return { t, onUpdate }
  },
  template: `
    <div class="furnished-toggle">
      <span class="toggle-label text-md-medium">{{ t('filter.furnishedOnly') }}</span>
      <el-switch
        :model-value="isFurnished"
        @update:modelValue="onUpdate"
        size="large"
      />
    </div>
  `,
})

// -----------------------------------------------------------------
// # FilterPanelFooter.vue
// -----------------------------------------------------------------
const FilterPanelFooter = defineComponent({
  name: 'FilterPanelFooter',
  props: {
    count: { type: [Number, null], default: null },
    isLoading: { type: Boolean, default: false },
    isApplyDisabled: { type: Boolean, default: false },
  },
  emits: ['cancel', 'apply'],
  setup(props, { emit }) {
    const t = inject('t', (key) => key)
    const applyButtonText = computed(() => {
      if (props.isLoading) return t('filter.loading')
      if (props.count !== null) return t('filter.applyWithCount', { count: props.count })
      return t('filter.apply')
    })
    return { t, emit, applyButtonText }
  },
  template: `
    <div class="panel-footer">
      <el-button class="cancel-btn" size="default" @click="emit('cancel')">
        {{ t('filter.cancel') }}
      </el-button>
      <el-button
        type="primary"
        class="apply-btn"
        size="default"
        @click="emit('apply')"
        :disabled="isApplyDisabled || isLoading"
        :aria-label="applyButtonText"
      >
        {{ applyButtonText }}
      </el-button>
    </div>
  `,
})

// #################################################################
// # 3. 主组件 (FilterPanel.vue)
// #################################################################

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  focusSection: { type: String, default: null },
})
const emit = defineEmits(['update:modelValue', 'filtersChanged'])

// 依赖注入
const t = inject('t', (key) => key)
const propertiesStore = usePropertiesStore()

// --- 状态管理 ---
const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value),
})

const defaultFilters = () => ({
  locations: [],
  priceRange: [0, 5000],
  bedrooms: [],
  bathrooms: [],
  parking: [],
  startDate: null,
  endDate: null,
  isFurnished: false,
})

// 草稿状态: 这是面板内部唯一的状态源
const draftFilters = reactive(defaultFilters())

// --- 逻辑与副作用 (通过 Composables) ---
useOffCanvasPanel(visible)
const {
  count: previewCount,
  isLoading: isPreviewLoading,
  triggerImmediateFetch,
} = useFilterPreviewCount(computed(() => draftFilters))

// --- 数据与计算属性 ---
const bedroomOptions = [
  { value: '0', label: t('filter.bedrooms.studio') },
  { value: '1', label: '1' },
  { value: '2', label: '2' },
  { value: '3', label: '3' },
  { value: '4+', label: '4+' },
]
const bathroomOptions = [
  { value: 'any', label: t('filter.any') },
  { value: '1', label: '1' },
  { value: '2', label: '2' },
  { value: '3+', label: '3+' },
]
const parkingOptions = [
  { value: 'any', label: t('filter.any') },
  { value: '1', label: '1' },
  { value: '2', label: '2' },
  { value: '3+', label: '3+' },
]

const isDateRangeValid = computed(() => {
  const { startDate, endDate } = draftFilters
  if (startDate && endDate) {
    return new Date(startDate).getTime() <= new Date(endDate).getTime()
  }
  return true
})

// --- 事件处理 ---
const closePanel = () => {
  visible.value = false
}

const applyFilters = async () => {
  if (!isDateRangeValid.value) {
    ElMessage.error(t('filter.error.dateInvalid'))
    return
  }
  // 职责简化：只调用 store 的 action，不再关心 URL
  await propertiesStore.applyFiltersFromDraft(draftFilters)
  emit('filtersChanged', draftFilters)
  closePanel()
}

const resetFilters = () => {
  Object.assign(draftFilters, defaultFilters())
}

// 关键改进：当面板打开时，用 Store 的当前状态来初始化草稿
const initializeDraftState = () => {
  // 1. 从 Store 获取当前已应用的筛选条件
  const appliedFilters = propertiesStore.currentFilters
  const appliedLocations = propertiesStore.selectedLocations

  // 2. 将它们同步到草稿状态
  draftFilters.locations = JSON.parse(JSON.stringify(appliedLocations || [])) // 深拷贝
  draftFilters.priceRange = [appliedFilters.minPrice || 0, appliedFilters.maxPrice || 5000]
  draftFilters.bedrooms = appliedFilters.bedrooms ? String(appliedFilters.bedrooms).split(',') : []
  draftFilters.bathrooms = appliedFilters.bathrooms ? String(appliedFilters.bathrooms).split(',') : []
  draftFilters.parking = appliedFilters.parking ? String(appliedFilters.parking).split(',') : []
  draftFilters.startDate = appliedFilters.date_from ? new Date(appliedFilters.date_from) : null
  draftFilters.endDate = appliedFilters.date_to ? new Date(appliedFilters.date_to) : null
  draftFilters.isFurnished = !!appliedFilters.isFurnished
}

// --- 副作用 ---
watch(visible, (isOpening) => {
  if (isOpening) {
    // 关键：初始化状态，确保面板反映当前已应用的筛选
    initializeDraftState()
    // 预加载区域数据
    propertiesStore.getAllAreas?.()
    // 聚焦与滚动
    focusAndScroll()
    // 立即获取一次初始预览计数
    nextTick(() => {
      triggerImmediateFetch()
    })
  }
})

// --- 锚点滚动 ---
const panelRef = ref(null)
const areaRef = ref(null)
const priceRef = ref(null)
const bedroomsRef = ref(null)
const availabilityRef = ref(null)
const moreRef = ref(null)

const focusAndScroll = async () => {
  await nextTick()
  if (!props.focusSection) {
    panelRef.value?.focus?.()
    return
  }
  const map = {
    area: areaRef,
    price: priceRef,
    bedrooms: bedroomsRef,
    availability: availabilityRef,
    more: moreRef,
  }
  const targetRef = map[props.focusSection]?.value
  if (targetRef) {
    // Vue3 中 ref 指向组件实例，需要访问 $el
    const element = targetRef.$el || targetRef
    element?.scrollIntoView({ behavior: 'smooth' })
  }
}
</script>

<style scoped>
/* 使用 CSS 变量 (设计令牌) 替代硬编码值 */

.filter-panel-wrapper {
  position: fixed;
  inset: 0;
  z-index: var(--z-index-panel);
  pointer-events: none;
}
.filter-panel-wrapper.visible {
  pointer-events: auto;
}
.filter-overlay {
  position: absolute;
  inset: 0;
  background: var(--color-overlay-bg);
  transition: opacity 0.3s ease;
}
.domain-filter-panel {
  position: absolute;
  top: 0;
  right: 0;
  width: var(--panel-width-desktop);
  height: 100vh; /* 移动端应使用 100dvh */
  background: var(--color-bg-panel);
  box-shadow: var(--shadow-lg);
  transform: translateX(100%);
  transition: transform 0.3s ease;
  display: flex;
  flex-direction: column;
  z-index: var(--z-index-panel-foreground);
}
.domain-filter-panel.visible {
  transform: translateX(0);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-md) var(--space-lg);
  border-bottom: 1px solid var(--color-border-default);
  flex-shrink: 0;
}
.panel-title {
  color: var(--color-text-primary);
  margin: 0;
}
.header-actions {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}
.reset-link {
  background: none;
  border: none;
  color: var(--color-text-link);
  cursor: pointer;
  text-decoration: underline;
  padding: var(--space-xs) var(--space-sm);
  border-radius: var(--radius-sm);
}
.reset-link:hover {
  background: var(--color-surface-hover);
  text-decoration: none;
}
.close-btn {
  background: none;
  border: none;
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: var(--space-sm);
  border-radius: var(--radius-full);
  width: 40px;
  height: 40px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.close-btn:hover {
  background: var(--color-surface-hover);
  color: var(--color-text-primary);
}

.panel-content {
  flex: 1;
  padding: var(--space-lg);
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}
.filter-section {
  margin-bottom: var(--space-xl);
}
.section-title {
  color: var(--color-text-primary);
  margin: 0 0 var(--space-md);
}
.sub-section-title {
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  margin: var(--space-lg) 0 var(--space-sm);
}

.location-list-wrapper {
  margin-bottom: var(--space-md);
}
.location-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-sm);
  background: var(--color-surface-muted);
  border: 1px solid var(--color-border-default);
  border-radius: var(--radius-md);
  padding: var(--space-sm);
}
.location-actions {
  margin-top: var(--space-xs);
}
.clear-all-btn {
  /* 与 .reset-link 样式一致 */
  background: none;
  border: none;
  color: var(--color-text-link);
  cursor: pointer;
  text-decoration: underline;
}

.section-header {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-bottom: var(--space-sm);
}
.price-display {
  color: var(--color-text-secondary);
}
.price-slider {
  margin: 0 var(--space-xs);
}

.filter-buttons-group.segmented {
  display: inline-flex;
  flex-wrap: nowrap;
  gap: 0;
  overflow: hidden;
  border: 1px solid var(--color-border-default);
  border-radius: var(--radius-sm);
}
.filter-buttons-group.segmented .filter-btn {
  border: none;
  border-right: 1px solid var(--color-border-default);
  padding: var(--space-sm) var(--space-md);
  background: var(--color-bg-primary);
  color: var(--color-text-primary);
  cursor: pointer;
  min-width: 60px;
  text-align: center;
}
.filter-buttons-group.segmented .filter-btn:last-child {
  border-right: none;
}
.filter-buttons-group.segmented .filter-btn:hover {
  background: var(--color-surface-hover);
}
.filter-buttons-group.segmented .filter-btn.active {
  background: var(--color-surface-selected);
  color: var(--color-text-primary);
  font-weight: var(--font-weight-semibold);
}

.date-picker-group {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}
.date-picker-start,
.date-picker-end {
  flex: 1;
}

.furnished-toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-md);
  background: var(--color-surface-muted);
  border-radius: var(--radius-md);
}
.toggle-label {
  color: var(--color-text-primary);
}

.panel-footer {
  display: flex;
  gap: var(--space-md);
  padding: var(--space-md) var(--space-lg);
  border-top: 1px solid var(--color-border-default);
  background: var(--color-bg-panel);
  flex-shrink: 0;
  padding-bottom: calc(var(--space-md) + env(safe-area-inset-bottom));
}
.cancel-btn {
  flex: 1;
}
.apply-btn {
  flex: 2;
}

@media (max-width: 767px) {
  .domain-filter-panel {
    width: 100%;
    height: 100dvh;
  }
  .panel-content {
    padding: var(--space-md);
  }
}
</style>
