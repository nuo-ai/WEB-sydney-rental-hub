<template>
  <!-- Domain风格筛选面板 -->
  <div v-if="visible" class="filter-panel-wrapper visible">
    <!-- 遮罩层 -->
    <div class="filter-overlay" @click="closePanel"></div>

    <!-- 筛选面板 -->
    <div ref="panelRef" class="domain-filter-panel" :class="{ visible: visible }" tabindex="-1">
      <!-- 面板头部 -->
      <div class="panel-header">
        <h3 class="panel-title chinese-text">{{ $t('filter.title') }}</h3>
        <div class="header-actions">
          <button class="reset-link" @click="resetFilters">{{ $t('filter.reset') }}</button>
          <button class="close-btn" @click="closePanel" aria-label="关闭筛选面板">
            <!-- 使用内联SVG替代 Font Awesome，符合“SVG组件化图标”与统一风格要求；避免新增依赖 -->
            <svg
              class="spec-icon"
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
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
      </div>

      <!-- 筛选内容 -->
      <div class="panel-content">
        <!-- Location（已选区域回显 + 清空 + 附近勾选） -->
        <div class="filter-section location-section" ref="areaRef">
          <h4 class="section-title chinese-text">{{ locationLabel }}</h4>

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

          <!-- 空态提示移除：按要求不显示“未选择任何区域”提示 -->

          <AreasSelector
            :selected="selectedLocations"
            @update:selected="onUpdateSelectedAreas"
            @requestCount="debouncedRequestCount"
          />
          <div v-if="SHOW_INCLUDE_NEARBY" class="nearby-toggle">
            <el-checkbox v-model="includeNearby" @change="handleIncludeNearbyChange">
              {{ searchNearbyLabel }}
            </el-checkbox>
          </div>
        </div>

        <!-- 价格范围滑块 -->
        <div class="filter-section" ref="priceRef">
          <div class="section-header">
            <h4 class="section-title chinese-text">{{ $t('filter.priceSection') }}</h4>
            <span class="price-display">{{ priceRangeText }}</span>
          </div>
          <el-slider
            v-model="filters.priceRange"
            range
            :min="0"
            :max="5000"
            :step="50"
            :show-stops="false"
            class="price-slider"
            @change="handlePriceChange"
          />
        </div>

        <!-- 卧室数量 -->
        <div class="filter-section" ref="bedroomsRef">
          <h4 class="section-title chinese-text">{{ $t('filter.bedrooms') }}</h4>
          <div class="filter-buttons-group segmented">
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
        </div>

        <!-- 浴室数量 -->
        <div class="filter-section" ref="moreRef">
          <h4 class="section-title chinese-text">{{ $t('filter.bathrooms') }}</h4>
          <div class="filter-buttons-group segmented">
            <button
              v-for="option in bathroomOptions"
              :key="option.value"
              class="filter-btn"
              :class="{ active: isBathroomSelected(option.value) }"
              @click="toggleBathroom(option.value)"
            >
              {{ option.label }}
            </button>
          </div>
        </div>

        <!-- 车位数量 -->
        <div class="filter-section">
          <h4 class="section-title chinese-text">{{ $t('filter.parking') }}</h4>
          <div class="filter-buttons-group segmented">
            <button
              v-for="option in parkingOptions"
              :key="option.value"
              class="filter-btn"
              :class="{ active: isParkingSelected(option.value) }"
              @click="toggleParking(option.value)"
            >
              {{ option.label }}
            </button>
          </div>
        </div>

        <!-- 空出日期 -->
        <div class="filter-section" ref="availabilityRef">
          <h4 class="section-title chinese-text">{{ $t('filter.date') }}</h4>
          <div class="date-picker-group">
            <el-date-picker
              v-model="filters.startDate"
              type="date"
              :placeholder="$t('filter.dateStart')"
              size="large"
              class="date-picker-start filter-field"
              :editable="false"
              :input-attrs="{ inputmode: 'none' }"
              :teleported="true"
              placement="top-start"
              @change="handleStartDateChange"
            />
            <span class="date-separator">{{ $t('filter.to') }}</span>
            <el-date-picker
              v-model="filters.endDate"
              type="date"
              :placeholder="$t('filter.dateEnd')"
              size="large"
              class="date-picker-end filter-field"
              :editable="false"
              :input-attrs="{ inputmode: 'none' }"
              :teleported="true"
              placement="top-start"
              @change="handleEndDateChange"
            />
          </div>
        </div>

        <!-- 家具选项 -->
        <div class="filter-section">
          <h4 class="section-title chinese-text">{{ $t('filter.furniture') }}</h4>
          <div class="furnished-toggle">
            <span class="toggle-label chinese-text">{{ $t('filter.furnishedOnly') }}</span>
            <el-switch v-model="filters.isFurnished" size="large" @change="handleFurnishedChange" />
          </div>
        </div>
      </div>

      <!-- 底部操作按钮 -->
      <div class="panel-footer">
        <el-button class="cancel-btn" size="default" @click="closePanel">
          {{ $t('filter.cancel') }}
        </el-button>
        <el-button
          type="primary"
          class="apply-btn"
          size="default"
          @click="applyFilters"
          :disabled="!isDateRangeValid"
          :aria-label="`确定（${filteredCount} 条结果）`"
        >
          确定（{{ filteredCount }} 条结果）
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick, inject } from 'vue'
import { usePropertiesStore } from '@/stores/properties'
import { ElMessage } from 'element-plus'
import { useRouter, useRoute } from 'vue-router'
import { sanitizeQueryParams, isSameQuery } from '@/utils/query'
import AreasSelector from '@/components/AreasSelector.vue'
import BaseChip from '@/components/base/BaseChip.vue'

// 中文注释：特性开关——控制“包含周边区域”UI 与透传是否启用（隐藏但保留代码，便于以后启用）
const SHOW_INCLUDE_NEARBY = false

// 组件属性
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  // 中文注释：用于从外部（如 FilterTabs/Chips）指定打开面板后的聚焦分组，仅PC使用
  focusSection: {
    type: String,
    default: null,
    validator: (v) => ['area', 'bedrooms', 'price', 'availability', 'more', null].includes(v),
  },
})

// 组件事件
const emit = defineEmits(['update:modelValue', 'filtersChanged'])

/* 路由：用于 URL Query 同步（P1-5） */
const router = useRouter()
const route = useRoute()

// 注入轻量 i18n（默认 zh-CN；若未提供则回退为 key）
const t = inject('t') || ((k) => k)

/* 状态管理 */
const propertiesStore = usePropertiesStore()
/* 面板容器引用：打开时将焦点置于非输入容器，避免 iOS Safari 自动放大 */
const panelRef = ref(null)
/* 分组锚点引用：用于 PC 端 Chips 锚点打开后滚动/聚焦 */
const areaRef = ref(null)
const priceRef = ref(null)
const bedroomsRef = ref(null)
const availabilityRef = ref(null)
/* “更多”锚点暂指向浴室分组，可按需迁移 */
const moreRef = ref(null)

/* 响应式数据 */
const filters = ref({
  priceRange: [0, 5000],
  bedrooms: [],
  bathrooms: [],
  parking: [],
  startDate: null,
  endDate: null,
  isFurnished: false,
})

/* 选区与“附近区域”开关 */
const selectedLocations = computed(() => propertiesStore.draftSelectedLocations || [])

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

const includeNearby = ref(true)
/* 文案回退，避免显示未注册的 key */
const searchNearbyLabel = computed(() => {
  const v = t('filter.searchNearby')
  return v && v !== 'filter.searchNearby' ? v : '包含周边区域'
})
/* 标题/按钮/空态文案回退，避免显示 key */
const locationLabel = computed(() => {
  const v = t('filter.location')
  return v && v !== 'filter.location' ? v : '区域'
})
const clearAllLabel = computed(() => {
  const v = t('filter.clearAll')
  return v && v !== 'filter.clearAll' ? v : '清空全部'
})
/* 显示格式化：仅 suburb 名称；postcode 仅显示自身 */
const formatLocation = (loc) => {
  if (!loc) return ''
  return loc.type === 'suburb' ? String(loc.name || '') : String(loc.name || '')
}
const removeLocation = (id) => {
  // 改为仅操作“草稿”选区，未应用前不影响列表/标签
  const temp = (propertiesStore.draftSelectedLocations || []).filter(
    (loc) => String(loc?.id ?? '') !== String(id),
  )
  propertiesStore.setDraftSelectedLocations(temp)
  nextTick(() => updateFilteredCount())
}
const clearAllLocations = () => {
  // 清空草稿选区；需“应用”后才真正生效
  propertiesStore.setDraftSelectedLocations([])
  nextTick(() => updateFilteredCount())
}
const handleIncludeNearbyChange = () => {
  nextTick(() => updateFilteredCount())
}

/* 区域目录交互：选择时仅刷新计数，不立即应用（分离选择与应用） */
const debouncedRequestCount = (() => {
  let tid = null
  return () => {
    if (tid) clearTimeout(tid)
    tid = setTimeout(() => {
      updateFilteredCount()
      tid = null
    }, 250)
  }
})()

const onUpdateSelectedAreas = (newList) => {
  // 改为仅更新草稿，不触发 apply；仅刷新底部“显示结果 (N)”
  propertiesStore.setDraftSelectedLocations(Array.isArray(newList) ? newList : [])
  nextTick(() => debouncedRequestCount())
}

/* 本地计算的筛选结果数量 */
const localFilteredCount = ref(0)
const _countReqSeq = ref(0) // 中文注释：计数请求序号；防并发乱序响应覆盖新结果（前端表现：防止计数“跳回老数”）
const _counting = ref(false) // 中文注释：计数中标记（可用于淡化/骨架态；当前未使用）

/* 将筛选参数写入 URL 的 Query（只写非空参数；保持 V1 键名，最小改动） */
const buildQueryFromFilters = (filterParams) => {
  const q = {}
  const put = (k, v) => {
    if (v !== null && v !== undefined && v !== '') q[k] = v
  }
  put('minPrice', filterParams.minPrice)
  put('maxPrice', filterParams.maxPrice)
  put('bedrooms', filterParams.bedrooms)
  put('bathrooms', filterParams.bathrooms)
  put('parking', filterParams.parking)
  put('date_from', filterParams.date_from)
  put('date_to', filterParams.date_to)
  if (filterParams.isFurnished === true) q.isFurnished = '1'
  put('suburb', filterParams.suburb)
  put('postcodes', filterParams.postcodes)
  if (SHOW_INCLUDE_NEARBY) put('include_nearby', includeNearby.value ? '1' : '0')
  return q
}

/* 从 URL Query 恢复筛选状态（刷新/直链可复现） */
const applyQueryToState = (query, store) => {
  if (!store) return
  try {
    // 价格
    const min = query.minPrice ? Number(query.minPrice) : 0
    const max = query.maxPrice ? Number(query.maxPrice) : 5000
    if (!Number.isNaN(min) || !Number.isNaN(max)) {
      filters.value.priceRange = [Number.isNaN(min) ? 0 : min, Number.isNaN(max) ? 5000 : max]
    }
    // 卧室（单选）
    if (query.bedrooms) {
      const b = String(query.bedrooms)
      filters.value.bedrooms = [b]
    }
    // 浴室/车位（单选）
    if (query.bathrooms) {
      filters.value.bathrooms = [String(query.bathrooms)]
    }
    if (query.parking) {
      const p = String(query.parking)
      // 兼容旧直链：'0' 与 'any' 视为 Any（不传）
      if (p === '0' || p === 'any') {
        filters.value.parking = []
      } else if (['1', '2', '3+'].includes(p)) {
        filters.value.parking = [p]
      } else {
        // 非法值回退为 Any
        filters.value.parking = []
      }
    }
    // 日期
    if (query.date_from) {
      filters.value.startDate = new Date(String(query.date_from))
    }
    if (query.date_to) {
      filters.value.endDate = new Date(String(query.date_to))
    }
    // 家具
    if (
      query.isFurnished === '1' ||
      query.furnished === '1' ||
      String(query.furnished) === 'true'
    ) {
      filters.value.isFurnished = true
    }
    // 区域（仅 suburb 名称 CSV）
    const suburbsCsv = query.suburb || query.suburbs
    if (suburbsCsv) {
      const names = String(suburbsCsv)
        .split(',')
        .map((s) => s.trim())
        .filter(Boolean)
      if (names.length) {
        store.selectedLocations = names.map((name) => ({
          id: `suburb_${name}`,
          type: 'suburb',
          name,
          fullName: name,
        }))
      }
    }
    // postcodes（CSV）
    const postcodesCsv = query.postcodes
    if (postcodesCsv) {
      const codes = String(postcodesCsv)
        .split(',')
        .map((s) => s.trim())
        .filter(Boolean)
      if (codes.length) {
        const existing = Array.isArray(store.selectedLocations) ? store.selectedLocations : []
        store.selectedLocations = existing.concat(
          codes.map((code) => ({
            id: `postcode_${code}`,
            type: 'postcode',
            name: code,
            fullName: code,
          })),
        )
      }
    }
    // include_nearby
    if (SHOW_INCLUDE_NEARBY && typeof query.include_nearby !== 'undefined') {
      includeNearby.value =
        String(query.include_nearby) === '1' || String(query.include_nearby) === 'true'
    }
  } catch (e) {
    console.warn('URL 查询解析失败:', e)
  }
}

// 辅助函数：格式化日期为YYYY-MM-DD
const formatDateToYYYYMMDD = (date) => {
  if (!date) return null
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// 选项数据
const bedroomOptions = [
  { value: '0', label: 'Studio' },
  { value: '1', label: '1' },
  { value: '2', label: '2' },
  { value: '3', label: '3' },
  { value: '4+', label: '4+' },
]

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

// 计算属性
const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value),
})

const priceRangeText = computed(() => {
  const [min, max] = filters.value.priceRange
  if (min === 0 && max === 5000) {
    return t('filter.anyPrice')
  } else if (max === 5000) {
    return `$${min}+`
  } else {
    return `$${min} - $${max}`
  }
})

const filteredCount = computed(() => {
  // 如果还没有进行过筛选，返回总数
  if (localFilteredCount.value === 0 && !hasAppliedFilters.value) {
    return propertiesStore.totalCount || propertiesStore.allProperties.length
  }
  return localFilteredCount.value
})

// 检查是否应用了筛选
const hasAppliedFilters = computed(() => {
  // 中文注释：将“已选区域”也视为筛选条件之一，确保当地区选择后即使计数为0也显示为0，而非回退到总数
  return (
    (propertiesStore.selectedLocations?.length || 0) > 0 ||
    filters.value.priceRange[0] > 0 ||
    filters.value.priceRange[1] < 5000 ||
    filters.value.bedrooms.length > 0 ||
    filters.value.bathrooms.length > 0 ||
    filters.value.parking.length > 0 ||
    filters.value.startDate !== null ||
    filters.value.endDate !== null ||
    filters.value.isFurnished !== false
  )
})

const isDateRangeValid = computed(() => {
  // 中文注释：当“从/到”都选择时，校验开始日期不能晚于结束日期；否则视为有效
  const s = filters.value.startDate
  const e = filters.value.endDate
  if (s && e) {
    return new Date(s).getTime() <= new Date(e).getTime()
  }
  return true
})

// 相邻多选逻辑
const isBedroomSelected = (value) => {
  return filters.value.bedrooms.includes(value)
}

const isBathroomSelected = (value) => {
  if (value === 'any') {
    // Any 按钮在没有任何选择时显示为选中
    return filters.value.bathrooms.length === 0
  }
  return filters.value.bathrooms.includes(value)
}

const isParkingSelected = (value) => {
  if (value === 'any') {
    // Any 按钮在没有任何选择时显示为选中
    return filters.value.parking.length === 0
  }
  return filters.value.parking.includes(value)
}

// 相邻选择验证
// 注：已改为单选逻辑，不再需要相邻检查

// 事件处理
const toggleBedroom = (value) => {
  // 单选逻辑：如果已选中则取消，否则选中
  if (filters.value.bedrooms.includes(value)) {
    filters.value.bedrooms = []
  } else {
    filters.value.bedrooms = [value]
  }
  updateFilteredCount()
}

const toggleBathroom = (value) => {
  // 单选逻辑：如果已选中则取消，否则选中
  if (value === 'any') {
    filters.value.bathrooms = []
  } else if (filters.value.bathrooms.includes(value)) {
    filters.value.bathrooms = []
  } else {
    filters.value.bathrooms = [value]
  }
  updateFilteredCount()
}

const toggleParking = (value) => {
  // 单选逻辑：如果已选中则取消，否则选中
  if (value === 'any') {
    filters.value.parking = []
  } else if (filters.value.parking.includes(value)) {
    filters.value.parking = []
  } else {
    filters.value.parking = [value]
  }
  updateFilteredCount()
}

// 实时更新筛选数量（不立即应用到store）
const updateFilteredCount = async () => {
  // 中文注释：日期区间校验，非法时不发起计数请求，直接显示 0
  if (filters.value.startDate && filters.value.endDate) {
    const s = new Date(filters.value.startDate).getTime()
    const e = new Date(filters.value.endDate).getTime()
    if (s > e) {
      localFilteredCount.value = 0
      return
    }
  }
  // 准备筛选参数（先沿用现有键名，后续统一映射）
  const filterParams = {
    minPrice: filters.value.priceRange[0] > 0 ? filters.value.priceRange[0] : null,
    maxPrice: filters.value.priceRange[1] < 5000 ? filters.value.priceRange[1] : null,
    bedrooms: filters.value.bedrooms.length > 0 ? filters.value.bedrooms.join(',') : null,
    bathrooms: filters.value.bathrooms.length > 0 ? filters.value.bathrooms.join(',') : null,
    parking: filters.value.parking.length > 0 ? filters.value.parking.join(',') : null,
    date_from: filters.value.startDate ? formatDateToYYYYMMDD(filters.value.startDate) : null,
    date_to: filters.value.endDate ? formatDateToYYYYMMDD(filters.value.endDate) : null,
    isFurnished: filters.value.isFurnished || null,
  }

  // 添加已选择的区域
  const selectedSuburbs = (propertiesStore.draftSelectedLocations || [])
    .filter((loc) => loc.type === 'suburb')
    .map((loc) => loc.name)
  if (selectedSuburbs.length > 0) {
    filterParams.suburb = selectedSuburbs.join(',')
  }
  // 支持 postcodes（与 suburbs 区分；CSV）
  const selectedPostcodes = (propertiesStore.draftSelectedLocations || [])
    .filter((loc) => loc.type === 'postcode')
    .map((loc) => loc.name)
  if (selectedPostcodes.length > 0) {
    filterParams.postcodes = selectedPostcodes.join(',')
  }
  // include_nearby 作为透传参数（后端未识别时无副作用）
  if (SHOW_INCLUDE_NEARBY) {
    filterParams.include_nearby = includeNearby.value ? '1' : '0'
  }

  // 移除 null 值
  Object.keys(filterParams).forEach((key) => {
    if (filterParams[key] === null || filterParams[key] === '') {
      delete filterParams[key]
    }
  })

  // 无筛选条件时，直接使用当前总数，避免不必要请求
  if (Object.keys(filterParams).length === 0) {
    localFilteredCount.value =
      propertiesStore.totalCount || propertiesStore.allProperties.length || 0
    return
  }

  try {
    // 统一通过 store 入口获取计数，避免双通道不一致
    const seq = ++_countReqSeq.value // 生成本次请求序号
    _counting.value = true
    const total = await propertiesStore.getFilteredCount(filterParams)
    // 仅当返回的结果仍对应“最新一次请求”时才落地，防止旧响应覆盖新状态
    if (seq === _countReqSeq.value) {
      localFilteredCount.value = total
      _counting.value = false
    } else {
      // 丢弃过期响应（不改动 UI）
    }
  } catch (error) {
    console.error('获取筛选计数失败:', error)
    // 快速失败：不做本地估算，不篡改现有计数，并就近提示错误
    // 失败时统一恢复为 false，若下一次请求已开始会再次置为 true，不影响表现
    _counting.value = false
    ElMessage.error('筛选计数失败，请稍后重试')
  }
}

/* 本地估算已移除：为避免与真实结果不一致，计数统一走后端接口，通过 store.getFilteredCount() 获取 */

const handlePriceChange = () => {
  nextTick(() => updateFilteredCount())
}

const handleStartDateChange = (date) => {
  // 中文注释：若选中的开始日期晚于当前结束日期，立即“交换两端”，保持 start ≤ end（最少惊讶）
  const currentEnd = filters.value.endDate
  filters.value.startDate = date
  if (date && currentEnd && new Date(date).getTime() > new Date(currentEnd).getTime()) {
    filters.value.startDate = currentEnd
    filters.value.endDate = date
  }
  nextTick(() => updateFilteredCount())
}

const handleEndDateChange = (date) => {
  // 中文注释：若选中的结束日期早于当前开始日期，立即“交换两端”，保持 start ≤ end（最少惊讶）
  const currentStart = filters.value.startDate
  filters.value.endDate = date
  if (date && currentStart && new Date(date).getTime() < new Date(currentStart).getTime()) {
    filters.value.endDate = currentStart
    filters.value.startDate = date
  }
  nextTick(() => updateFilteredCount())
}

const handleFurnishedChange = () => {
  nextTick(() => updateFilteredCount())
}

// 关闭面板方法
const closePanel = () => {
  // 关闭时丢弃未应用的区域草稿
  try {
    propertiesStore.resetDraftSelectedLocations()
  } catch {
    /* 忽略非关键错误 */
  }
  visible.value = false
}

const applyFiltersToStore = async () => {
  try {
    // 准备筛选参数（以草稿为准），点击“应用”前不影响已应用条件
    const filterParams = {
      minPrice: filters.value.priceRange[0] > 0 ? filters.value.priceRange[0] : null,
      maxPrice: filters.value.priceRange[1] < 5000 ? filters.value.priceRange[1] : null,
      bedrooms: filters.value.bedrooms.length > 0 ? filters.value.bedrooms.join(',') : null,
      bathrooms: filters.value.bathrooms.length > 0 ? filters.value.bathrooms.join(',') : null,
      parking: filters.value.parking.length > 0 ? filters.value.parking.join(',') : null,
      date_from: filters.value.startDate ? formatDateToYYYYMMDD(filters.value.startDate) : null,
      date_to: filters.value.endDate ? formatDateToYYYYMMDD(filters.value.endDate) : null,
      isFurnished: filters.value.isFurnished || null,
    }

    // 添加已选择的区域
    const selectedSuburbs = (propertiesStore.draftSelectedLocations || [])
      .filter((loc) => loc.type === 'suburb')
      .map((loc) => loc.name)
    if (selectedSuburbs.length > 0) {
      filterParams.suburb = selectedSuburbs.join(',')
    }
    // 支持 postcodes（与 suburbs 区分；CSV）
    const selectedPostcodes = (propertiesStore.draftSelectedLocations || [])
      .filter((loc) => loc.type === 'postcode')
      .map((loc) => loc.name)
    if (selectedPostcodes.length > 0) {
      filterParams.postcodes = selectedPostcodes.join(',')
    }
    // include_nearby 透传（特性开关）
    if (SHOW_INCLUDE_NEARBY) {
      filterParams.include_nearby = includeNearby.value ? '1' : '0'
    }

    // 计算本次触达的分组（精确删除与合并，仅影响当前修改的分组）
    const beforeIds = (propertiesStore.selectedLocations || []).map((l) => String(l.id)).sort()
    const draftIds = (propertiesStore.draftSelectedLocations || []).map((l) => String(l.id)).sort()
    const areaChanged = JSON.stringify(beforeIds) !== JSON.stringify(draftIds)
    const sections = []
    // price
    if (Object.prototype.hasOwnProperty.call(filterParams, 'minPrice') || Object.prototype.hasOwnProperty.call(filterParams, 'maxPrice')) {
      sections.push('price')
    }
    // bedrooms（含浴室/车位）
    if (
      Object.prototype.hasOwnProperty.call(filterParams, 'bedrooms') ||
      Object.prototype.hasOwnProperty.call(filterParams, 'bathrooms') ||
      Object.prototype.hasOwnProperty.call(filterParams, 'parking')
    ) {
      sections.push('bedrooms')
    }
    // availability
    if (
      Object.prototype.hasOwnProperty.call(filterParams, 'date_from') ||
      Object.prototype.hasOwnProperty.call(filterParams, 'date_to')
    ) {
      sections.push('availability')
    }
    // more（仅家具）：若已应用存在家具或本次勾选家具，则纳入以便清/设
    {
      const applied = propertiesStore.currentFilterParams || {}
      const furnishedApplied = applied.isFurnished === true || applied.furnished === true
      if (filterParams.isFurnished === true || furnishedApplied) {
        sections.push('more')
      }
    }
    // area：若草稿与已应用不同，或本次提交包含 suburb/postcodes，则纳入
    if (areaChanged || Object.prototype.hasOwnProperty.call(filterParams, 'suburb') || Object.prototype.hasOwnProperty.call(filterParams, 'postcodes')) {
      sections.push('area')
    }

    // 先将草稿区域应用为“已应用”，再统一调用 applyFilters（携带分组边界）
    try {
      propertiesStore.applySelectedLocations()
    } catch {
      /* 忽略非关键错误 */
    }
    await propertiesStore.applyFilters(filterParams, { sections })
    emit('filtersChanged', filterParams)

    // 将当前筛选写入 URL，便于刷新/分享复现（仅写非空有效键；避免无意义 replace 循环）
    try {
      const raw = buildQueryFromFilters(filterParams)
      const nextQuery = sanitizeQueryParams(raw)
      const currQuery = sanitizeQueryParams(route.query || {})
      if (!isSameQuery(currQuery, nextQuery)) {
        await router.replace({ query: nextQuery })
      }
    } catch (e) {
      console.warn('同步 URL 查询参数失败:', e)
    }
  } catch (error) {
    console.error('筛选应用失败:', error)
    ElMessage.error('筛选失败，请稍后重试')
  }
}

const applyFilters = async () => {
  // 中文注释：提交前校验“从/到”日期合法性
  if (!isDateRangeValid.value) {
    ElMessage.error('开始日期不能晚于结束日期')
    return
  }
  await applyFiltersToStore()
  // 应用后更新计数为实际结果
  localFilteredCount.value = propertiesStore.totalCount
  closePanel()
}

const resetFilters = () => {
  filters.value = {
    priceRange: [0, 5000],
    bedrooms: [],
    bathrooms: [],
    parking: [],
    startDate: null,
    endDate: null,
    isFurnished: false,
  }

  // 如果有选中的区域，基于区域更新计数；否则显示总数
  if (propertiesStore.selectedLocations.length > 0) {
    updateFilteredCount()
  } else {
    localFilteredCount.value =
      propertiesStore.totalCount || propertiesStore.allProperties.length || 0
  }
}

// 暴露方法给父组件以同步状态
defineExpose({
  setFilters: (newFilters) => {
    if (newFilters.priceRange) filters.value.priceRange = newFilters.priceRange
    if (newFilters.bedrooms) filters.value.bedrooms = newFilters.bedrooms
    if (newFilters.bathrooms) filters.value.bathrooms = newFilters.bathrooms
    if (newFilters.parking) filters.value.parking = newFilters.parking
  },
})

/* 分组锚点滚动与聚焦（仅桌面启用聚焦，滚动始终可用） */
const isDesktop = () => (typeof window !== 'undefined' ? window.innerWidth >= 1200 : true)

const getFirstFocusable = (rootEl) => {
  if (!rootEl) return null
  const selector = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  const el = rootEl.querySelector(selector)
  if (el) return el
  const inner = rootEl.querySelector('.el-input__inner')
  return inner || null
}

const scrollAndFocus = (sectionRef) => {
  const el = sectionRef?.value
  if (!el) return
  try {
    el.scrollIntoView({ block: 'start', behavior: 'smooth' })
  } catch {
    /* 忽略非关键错误 */
  }
  if (!isDesktop()) return
  nextTick(() => {
    try {
      const focusEl = getFirstFocusable(el)
      focusEl?.focus?.({ preventScroll: true })
    } catch {
      /* 忽略非关键错误 */
    }
  })
}

/* 当面板打开且指定了 focusSection 时，滚动并尝试聚焦对应分组 */
watch(
  () => [visible.value, props.focusSection],
  async ([vis, section]) => {
    if (!vis || !section) return
    await nextTick()
    const map = {
      area: areaRef,
      bedrooms: bedroomsRef,
      price: priceRef,
      availability: availabilityRef,
      more: moreRef,
    }
    const target = map[section]
    if (target) scrollAndFocus(target)
  },
  { immediate: false },
)

// 滚动锁定管理
const lockBodyScroll = () => {
  if (typeof document === 'undefined') return
  // 中文注释：锁定 body 滚动，防止页面滚动条与面板滚动条并列
  document.documentElement.style.overflow = 'hidden'
  document.body.style.overflow = 'hidden'
  // 防止滚动穿透
  document.body.style.position = 'fixed'
  document.body.style.width = '100%'
}

const unlockBodyScroll = () => {
  if (typeof document === 'undefined') return
  // 中文注释：恢复 body 滚动
  document.documentElement.style.overflow = ''
  document.body.style.overflow = ''
  document.body.style.position = ''
  document.body.style.width = ''
}

// 键盘事件处理
const handleKeyDown = (event) => {
  if (event.key === 'Escape') {
    closePanel()
  }
}

// 生命周期
watch(visible, (newValue) => {
  if (newValue) {
    // 打开面板时的操作
    lockBodyScroll()
    // 打开时同步草稿=已应用，再基于草稿计算预览计数
    try {
      propertiesStore.resetDraftSelectedLocations()
    } catch {
      /* 忽略非关键错误 */
    }
    updateFilteredCount()

    // 添加键盘事件监听
    if (typeof document !== 'undefined') {
      document.addEventListener('keydown', handleKeyDown)
    }

    try {
      // 预先加载区域目录，避免首次打开仅见"静态搜索框"
      propertiesStore.getAllAreas?.()
    } catch {
      /* 忽略非关键错误 */
    }

    // iOS 防自动放大：清理当前任何活动焦点，并把焦点转移到非输入容器
    nextTick(() => {
      try {
        if (typeof document !== 'undefined' && document.activeElement) {
          document.activeElement.blur?.()
        }
      } catch {
        // 忽略非关键错误
      }
      try {
        panelRef.value?.focus?.()
      } catch {
        // 忽略非关键错误
      }
    })
  } else {
    // 关闭面板时的清理操作
    unlockBodyScroll()

    // 移除键盘事件监听
    if (typeof document !== 'undefined') {
      document.removeEventListener('keydown', handleKeyDown)
    }
  }
})

// 组件卸载时的清理
import { onUnmounted } from 'vue'
onUnmounted(() => {
  unlockBodyScroll()
  if (typeof document !== 'undefined') {
    document.removeEventListener('keydown', handleKeyDown)
  }
})

// 初始化时设置默认计数
onMounted(() => {
  // 先从 URL 恢复筛选状态（刷新/直链）
  applyQueryToState(route.query, propertiesStore)

  // 若存在筛选或已有选区，则刷新计数；否则显示总数
  if (propertiesStore.selectedLocations.length > 0 || hasAppliedFilters.value) {
    updateFilteredCount()
  } else {
    localFilteredCount.value =
      propertiesStore.totalCount || propertiesStore.allProperties.length || 0
  }
})
</script>

<style scoped>
/* Domain风格筛选面板包装器 */
.filter-panel-wrapper {
  position: fixed;
  inset: 0;
  z-index: 2000; /* 降低z-index，让日期选择器能显示在上面 */
  pointer-events: none; /* 默认不捕获事件，只在visible时才捕获 */
}

.filter-panel-wrapper.visible {
  pointer-events: auto; /* 只在显示时捕获点击事件 */
}

/* 遮罩层 */
.filter-overlay {
  position: absolute;
  inset: 0;
  background: rgb(0 0 0 / 40%);
  transition: opacity 0.3s ease;
  pointer-events: auto; /* 确保遮罩层可点击 */
}

/* 移动端遮罩层 */
@media (width <= 767px) {
  .filter-overlay {
    background: rgb(0 0 0 / 50%); /* 移动端加深背景 */
  }
}

/* Domain风格筛选面板 */
.domain-filter-panel {
  position: absolute;
  top: 0;
  right: 0;
  width: 420px;
  height: 100vh;
  background: white;
  box-shadow: -4px 0 20px rgb(0 0 0 / 15%);
  transform: translateX(100%);
  transition: transform 0.3s ease;
  display: flex;
  flex-direction: column;
  z-index: 2001; /* 确保面板在遮罩层之上 */
}

.domain-filter-panel.visible {
  transform: translateX(0);
}

/* 面板头部 - 使用设计令牌 */
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--filter-space-2xl) var(--filter-space-3xl);
  border-bottom: 1px solid var(--filter-panel-header-border);
  background: var(--filter-panel-bg);
}

.panel-title {
  font-size: var(--filter-panel-title-font-size);
  font-weight: var(--filter-panel-title-font-weight);
  color: var(--filter-panel-title-color);
  margin: 0;
  line-height: var(--filter-line-height-tight);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: var(--filter-space-xl);
}

.reset-link {
  background: none;
  border: none;
  color: var(--filter-action-link-color);
  font-size: var(--filter-action-link-font-size);
  font-weight: var(--filter-action-link-font-weight);
  cursor: pointer;
  text-decoration: underline;
  padding: var(--filter-action-link-padding-y) var(--filter-action-link-padding-x);
  border-radius: var(--filter-action-link-radius);
  transition: var(--filter-transition-fast);

  /* 移动端触摸目标 */
  min-height: 32px;
  display: inline-flex;
  align-items: center;
}

.reset-link:hover {
  background: var(--filter-action-link-hover-bg);
  color: var(--filter-action-link-hover-color);
  text-decoration: none;
}

.close-btn {
  background: none;
  border: none;
  color: var(--filter-close-btn-color);
  cursor: pointer;
  padding: var(--filter-close-btn-padding);
  border-radius: var(--filter-close-btn-radius);
  transition: var(--filter-transition-fast);
  width: var(--filter-close-btn-size);
  height: var(--filter-close-btn-size);
  display: inline-flex;
  align-items: center;
  justify-content: center;

  /* 移动端触摸目标优化 */
  min-width: 40px;
  min-height: 40px;
}

.close-btn:hover {
  background: var(--filter-close-btn-hover-bg);
  color: var(--filter-close-btn-hover-color);
}

.close-btn:focus-visible {
  outline: 2px solid var(--filter-color-focus-ring);
  outline-offset: 1px;
}

/* 面板内容 */
.panel-content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

/* 筛选区块 */
.filter-section {
  margin-bottom: 32px;
}

.filter-section:last-child {
  margin-bottom: 0;
}

/* 区块标题 */
.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 16px;
}

/* 价格区块头部 */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.price-display {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-secondary);
}

/* 价格滑块 */
.price-slider {
  margin: 8px 0;
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

/* 筛选按钮组 - 使用设计令牌 */
.filter-buttons-group {
  display: flex;
  flex-wrap: wrap;
  gap: var(--filter-space-lg);
}

/* 移动端按钮组 */
@media (width <= 767px) {
  .filter-buttons-group {
    gap: var(--filter-space-md);
  }
}

.filter-btn {
  padding: var(--filter-btn-padding-y) var(--filter-btn-padding-x);
  border: 1px solid var(--filter-color-border-default);
  border-radius: var(--filter-radius-lg);
  background: var(--filter-color-bg-primary);
  font-size: var(--filter-btn-font-size);
  font-weight: var(--filter-btn-font-weight);
  color: var(--filter-color-text-primary);
  cursor: pointer;
  transition: var(--filter-transition-normal);
  min-width: 60px;

  /* 移动端触摸目标优化 */
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.filter-btn:hover {
  border-color: var(--filter-color-hover-border);
  color: var(--filter-color-text-primary);
  background: var(--filter-color-hover-bg);
}

.filter-btn.active {
  background: var(--filter-color-selected-bg);
  border-color: var(--filter-color-selected-border);
  color: var(--filter-color-text-primary);
  font-weight: var(--filter-font-weight-semibold);
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

/* 移动端按钮优化 */
@media (width <= 767px) {
  .filter-btn {
    padding: 14px var(--filter-btn-padding-x);
    font-size: var(--filter-font-size-md);
    min-width: 64px;
    min-height: 48px; /* 更大的触摸目标 */
  }
}

/* 日期选择器 */
.date-picker-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.date-picker-start,
.date-picker-end {
  flex: 1;
}

.date-separator {
  color: var(--color-text-secondary);
}

.date-picker :deep(.el-input__wrapper) {
  border-radius: 8px;
  border: 1px solid var(--color-border-default);
}

.date-picker :deep(.el-input__wrapper):hover {
  border-color: var(--color-border-strong);
}

.date-picker :deep(.el-input__wrapper.is-focus) {
  /* 去除点击后的灰色/橙色外框与高亮，保持无 ring */
  border-color: var(--color-border-default);
  box-shadow: none;
}

/* 确保日期选择器弹出层在最上层 */
:deep(.el-date-picker__popper) {
  z-index: 10002 !important; /* 高于筛选面板的9999 */
}

:deep(.el-popper) {
  z-index: 10002 !important;
}

:deep(.el-picker__popper) {
  z-index: 10002 !important;
}

/* 家具开关 */
.furnished-toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  background: #f8f9fa;
  border: 1px solid var(--color-border-default);
  border-radius: 8px;
}

.toggle-label {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
}

.furnished-toggle :deep(.el-switch__core) {
  background-color: var(--color-border-default);
}

.furnished-toggle :deep(.el-switch.is-checked .el-switch__core) {
  background-color: var(--color-border-strong);
}

/* 面板底部 - 对齐区域面板样式 */
.panel-footer {
  display: flex;
  gap: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--color-border-default);
  background: var(--color-bg-card);
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
  background: var(--filter-color-hover-bg);
}

.cancel-btn:focus-visible {
  outline: 2px solid var(--filter-color-focus-ring);
  outline-offset: 1px;
}

.apply-btn {
  flex: 2;
  background-color: var(--juwo-primary);
  border-color: var(--juwo-primary);
  color: var(--filter-btn-primary-color);
  transition: none;
}

.apply-btn:hover {
  background-color: var(--juwo-primary-light);
  border-color: var(--juwo-primary-light);
}

.apply-btn:focus-visible {
  outline: 2px solid var(--filter-color-focus-ring);
  outline-offset: 1px;
}

.apply-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.apply-btn:disabled:hover {
  background-color: var(--filter-btn-primary-bg);
  border-color: var(--filter-btn-primary-bg);
}

/* 移动端底部按钮优化 */
@media (width <= 767px) {
  .panel-footer {
    padding: var(--filter-space-2xl);

    /* 为 iOS 底部 Home Bar 预留安全区，确保按钮不被遮挡 */
    padding-bottom: calc(var(--filter-space-2xl) + env(safe-area-inset-bottom));
    gap: var(--filter-space-lg);
  }

  .cancel-btn,
  .apply-btn {
    min-height: 52px; /* 移动端更大的触摸目标 */
    font-size: var(--filter-font-size-lg);
    font-weight: var(--filter-font-weight-semibold);
  }
}

/* Location 区样式 - 使用设计令牌 */
.location-section .location-list {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  gap: var(--filter-space-md);
  /* 新增：白底容器外观 */
  background: var(--color-bg-card);
  border: 1px solid var(--color-border-default);
  border-radius: 8px;
  padding: 12px;
}

.location-chip {
  display: inline-flex;
  align-items: center;
  gap: var(--filter-chip-gap);
  /* 贴近截图：更紧凑的内边距与更小圆角 */
  padding: 6px 10px;
  border: 1px solid var(--color-border-default);
  border-radius: 4px;
  background: var(--filter-chip-bg);
  color: var(--filter-chip-text);
  font-size: var(--filter-chip-font-size);
  font-weight: var(--filter-chip-font-weight);
  max-width: 160px;
  transition: var(--filter-transition-fast);

  /* 移动端触摸优化 */
  min-height: 32px;
}

.location-chip:hover {
  border-color: var(--filter-chip-hover-border);
  background: var(--filter-chip-hover-bg);
}

.location-chip .chip-text {
  color: inherit;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}
/* 兼容 BaseChip 子元素命名，保持现有样式生效 */
.location-chip :deep(.base-chip__text) {
  color: inherit;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

.location-chip .chip-remove {
  background: var(--filter-chip-remove-bg);
  border: none;
  color: var(--filter-chip-remove-color);
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
  flex-shrink: 0;

  /* 移动端触摸目标优化 */
  min-width: 20px;
  min-height: 20px;
}
/* 兼容 BaseChip 子元素命名，保持现有样式生效 */
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

  /* 移动端触摸目标优化 */
  min-width: 20px;
  min-height: 20px;
}

.location-chip .chip-remove:hover {
  background: var(--filter-chip-remove-hover-bg);
  color: var(--filter-chip-remove-hover-color);
}
/* 兼容 BaseChip 子元素命名，保持现有样式生效 */
.location-chip :deep(.base-chip__remove:hover) {
  background: var(--filter-chip-remove-hover-bg);
  color: var(--filter-chip-remove-hover-color);
}

/* 彻底移除“位置标签 ×”的浅蓝底：选中/hover/focus 均保持中性 remove 背景 */
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
  margin-top: var(--filter-space-sm);
  display: flex;
  gap: var(--filter-space-lg);
  align-items: center;
}

.clear-all,
.toggle-chips {
  background: none;
  border: none;
  color: var(--filter-action-link-color);
  text-decoration: underline;
  font-size: var(--filter-action-link-font-size);
  font-weight: var(--filter-action-link-font-weight);
  cursor: pointer;
  padding: var(--filter-action-link-padding-y) var(--filter-action-link-padding-x);
  border-radius: var(--filter-action-link-radius);
  transition: var(--filter-transition-fast);

  /* 移动端触摸目标 */
  min-height: 32px;
  display: inline-flex;
  align-items: center;
}

.clear-all:hover,
.toggle-chips:hover {
  background: var(--filter-action-link-hover-bg);
  color: var(--filter-action-link-hover-color);
  text-decoration: none;
}

.nearby-toggle {
  margin-top: var(--filter-space-lg);
}

/* Location 空态提示 - 使用设计令牌 */
.location-empty .empty-box {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--filter-space-md);
  border: 1px solid var(--filter-empty-border);
  background: var(--filter-empty-bg);
  border-radius: var(--filter-empty-radius);
  padding: var(--filter-empty-padding-y) var(--filter-empty-padding-x);
  text-align: center;
}

.location-empty .empty-text {
  font-size: var(--filter-empty-font-size);
  font-weight: var(--filter-empty-font-weight);
  color: var(--filter-empty-text-color);
  line-height: var(--filter-line-height-normal);
}

/* 移动端Location区域优化 */
@media (width <= 767px) {
  .location-section .location-list {
    display: flex;
    flex-wrap: wrap;
    gap: var(--filter-space-sm);
    /* 移动端：更紧凑的内边距与圆角 */
    padding: 8px;
    border-radius: 6px;
  }

  .location-chip {
    padding: calc(var(--filter-chip-padding-y) + 2px) var(--filter-chip-padding-x);
    min-height: 36px;
    font-size: var(--filter-font-size-md);
  }

  .location-chip .chip-remove {
    width: calc(var(--filter-chip-remove-size) + 4px);
    height: calc(var(--filter-chip-remove-size) + 4px);
    min-width: 24px;
    min-height: 24px;
  }
  /* 兼容 BaseChip 子元素命名，保持现有样式生效（移动端尺寸） */
  .location-chip :deep(.base-chip__remove) {
    width: calc(var(--filter-chip-remove-size) + 4px);
    height: calc(var(--filter-chip-remove-size) + 4px);
    min-width: 24px;
    min-height: 24px;
  }

  .location-actions {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--filter-space-sm);
  }

  .clear-all,
  .toggle-chips {
    min-height: 36px;
    padding: var(--filter-space-sm) var(--filter-space-md);
  }
}

/* 移动端全屏模式 */
@media (width <= 767px) {
  .domain-filter-panel {
    width: 100%;

    /* 使用 100dvh 适配 iOS 可见视口，避免地址栏导致的“超出屏幕” */
    height: 100dvh;
    max-height: 100dvh;
    top: 0;
    right: 0;
    bottom: auto;
    transform: translateX(100%);
    transition: transform 0.3s ease;

    /* 防止 iOS 文本自动缩放触发放大 */
    text-size-adjust: 100%;
  }

  .domain-filter-panel.visible {
    transform: translateX(0);
  }

  /* 让容器可被聚焦但无可见描边，配合 tabindex="-1" */
  .domain-filter-panel:focus {
    outline: none;
  }

  /* Fallback：部分旧 iOS 不支持 dvh，使用 -webkit-fill-available，其次回退到 100vh */
  @supports not (height: 100dvh) {
    .domain-filter-panel {
      height: -webkit-fill-available;
      max-height: -webkit-fill-available;
    }
  }

  @supports not (height: -webkit-fill-available) {
    .domain-filter-panel {
      height: 100vh;
      max-height: 100vh;
    }
  }

  .panel-content {
    padding: 20px;
  }

  /* iOS Safari 输入框 auto-zoom 规避：保证输入相关元素字号 ≥16px，避免聚焦触发页面放大
     收敛到筛选输入作用域（.filter-field），避免面板内其它元素被放大 */
  .domain-filter-panel .filter-field :deep(input),
  .domain-filter-panel .filter-field :deep(textarea),
  .domain-filter-panel .filter-field :deep(select),
  .domain-filter-panel .filter-field :deep(.el-input__inner),
  .domain-filter-panel .filter-field :deep(.el-input__wrapper) {
    /* iOS 自动放大阈值：确保输入字号 ≥16px；使用 !important 覆盖库内部样式 */
    font-size: var(--filter-field-font-mob, 16px) !important;
  }

  .filter-section {
    margin-bottom: 24px;
  }

  .filter-btn {
    padding: 10px 16px;
    font-size: 13px;
    min-width: 55px;
  }

  /* 移动端滚动优化 */
  .panel-content {
    -webkit-overflow-scrolling: touch;
    overscroll-behavior: contain;
  }

  .panel-footer {
    padding: 20px;

    /* 为 iOS 底部 Home Bar 预留安全区，确保按钮不被遮挡 */
    padding-bottom: calc(20px + env(safe-area-inset-bottom));
    background: white;

    /* 说明：footer 位于滚动容器(panel-content)之外，天然常驻，无需 sticky；此处仅做安全区留白 */
  }
}
</style>
