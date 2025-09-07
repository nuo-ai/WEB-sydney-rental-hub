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
            <svg class="spec-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="M18 6 6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- 筛选内容 -->
      <div class="panel-content">
        <!-- Location（已选区域回显 + 清空 + 附近勾选） -->
        <div class="filter-section location-section">
          <h4 class="section-title chinese-text">{{ locationLabel }}</h4>

          <template v-if="selectedLocations.length">
            <div class="location-list">
              <div
                v-for="loc in selectedLocations"
                :key="loc.id"
                class="location-chip"
                :title="loc.fullName || loc.name"
              >
                <span class="chip-text">{{ formatLocation(loc) }}</span>
                <button
                  class="chip-remove"
                  :aria-label="'移除 ' + (loc.fullName || loc.name)"
                  @click="removeLocation(loc.id)"
                >
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <path d="M18 6 6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
              </div>
            </div>
            <div class="location-actions">
              <button class="clear-all" type="button" @click="clearAllLocations">
                {{ clearAllLabel }}
              </button>
            </div>
          </template>

          <div v-else class="location-empty">
            <div class="empty-box" role="note" aria-live="polite">
              <span class="empty-text">{{ locationEmptyLabel }}</span>
              <button type="button" class="go-select" @click="closePanel">{{ goSelectLabel }}</button>
            </div>
          </div>

          <div class="nearby-toggle">
            <el-checkbox v-model="includeNearby" @change="handleIncludeNearbyChange">
              {{ searchNearbyLabel }}
            </el-checkbox>
          </div>
        </div>

        <!-- 价格范围滑块 -->
        <div class="filter-section">
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
        <div class="filter-section">
          <h4 class="section-title chinese-text">{{ $t('filter.bedrooms') }}</h4>
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
        </div>

        <!-- 浴室数量 -->
        <div class="filter-section">
          <h4 class="section-title chinese-text">{{ $t('filter.bathrooms') }}</h4>
          <div class="filter-buttons-group">
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
          <div class="filter-buttons-group">
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
        <div class="filter-section">
          <h4 class="section-title chinese-text">{{ $t('filter.date') }}</h4>
          <div class="date-picker-group">
            <el-date-picker
              v-model="filters.startDate"
              type="date"
              :placeholder="$t('filter.dateStart')"
              size="large"
              class="date-picker-start"
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
              class="date-picker-end"
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
        <el-button class="cancel-btn" size="large" @click="closePanel"> {{ $t('filter.cancel') }} </el-button>
        <el-button type="primary" class="apply-btn" size="large" @click="applyFilters" :disabled="!isDateRangeValid">
          {{ $t('filter.showResults') }} ({{ filteredCount }})
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

// 组件属性
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
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
const selectedLocations = computed(() => propertiesStore.selectedLocations || [])
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
const locationEmptyLabel = computed(() => {
  const v = t('filter.locationEmpty')
  return v && v !== 'filter.locationEmpty' ? v : '未选择任何区域，请先从搜索栏选择区域'
})
const goSelectLabel = computed(() => {
  const v = t('filter.goSelect')
  return v && v !== 'filter.goSelect' ? v : '去选择区域'
})
/* 显示格式化：Suburb, NSW, 2017 / 2017 */
const formatLocation = (loc) => {
  if (!loc) return ''
  if (loc.type === 'suburb') {
    const pc = loc.postcode ? `, NSW, ${loc.postcode}` : ''
    return `${loc.name}${pc}`
  }
  return `${loc.name}`
}
const removeLocation = (id) => {
  propertiesStore.removeSelectedLocation(id)
  nextTick(() => updateFilteredCount())
}
const clearAllLocations = () => {
  propertiesStore.setSelectedLocations([])
  nextTick(() => updateFilteredCount())
}
const handleIncludeNearbyChange = () => {
  nextTick(() => updateFilteredCount())
}

/* 本地计算的筛选结果数量 */
const localFilteredCount = ref(0)

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
  put('include_nearby', includeNearby.value ? '1' : '0')
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
    if (query.isFurnished === '1' || query.furnished === '1' || String(query.furnished) === 'true') {
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
    if (typeof query.include_nearby !== 'undefined') {
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
  return (
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
  const selectedSuburbs = propertiesStore.selectedLocations
    .filter((loc) => loc.type === 'suburb')
    .map((loc) => loc.name)
  if (selectedSuburbs.length > 0) {
    filterParams.suburb = selectedSuburbs.join(',')
  }
  // 支持 postcodes（与 suburbs 区分；CSV）
  const selectedPostcodes = propertiesStore.selectedLocations
    .filter((loc) => loc.type === 'postcode')
    .map((loc) => loc.name)
  if (selectedPostcodes.length > 0) {
    filterParams.postcodes = selectedPostcodes.join(',')
  }
  // include_nearby 作为透传参数（后端未识别时无副作用）
  filterParams.include_nearby = includeNearby.value ? '1' : '0'

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
    const total = await propertiesStore.getFilteredCount(filterParams)
    localFilteredCount.value = total
  } catch (error) {
    console.error('获取筛选计数失败:', error)
    // 快速失败：不做本地估算，不篡改现有计数，并就近提示错误
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
  visible.value = false
}

const applyFiltersToStore = async () => {
  try {
    // 准备筛选参数，直接传递选中的值
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
    const selectedSuburbs = propertiesStore.selectedLocations
      .filter((loc) => loc.type === 'suburb')
      .map((loc) => loc.name)
    if (selectedSuburbs.length > 0) {
      filterParams.suburb = selectedSuburbs.join(',')
    }
    // 支持 postcodes（与 suburbs 区分；CSV）
    const selectedPostcodes = propertiesStore.selectedLocations
      .filter((loc) => loc.type === 'postcode')
      .map((loc) => loc.name)
    if (selectedPostcodes.length > 0) {
      filterParams.postcodes = selectedPostcodes.join(',')
    }
    // include_nearby 透传
    filterParams.include_nearby = includeNearby.value ? '1' : '0'

    await propertiesStore.applyFilters(filterParams)
    emit('filtersChanged', filterParams)

    // 将当前筛选写入 URL，便于刷新/分享复现
    try {
      const query = buildQueryFromFilters(filterParams)
      await router.replace({ query })
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

// 生命周期
watch(visible, (newValue) => {
  if (newValue) {
    // 打开面板时，更新筛选计数
    updateFilteredCount()
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
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 2000; /* 降低z-index，让日期选择器能显示在上面 */
  pointer-events: none; /* 默认不捕获事件，只在visible时才捕获 */
}

.filter-panel-wrapper.visible {
  pointer-events: auto; /* 只在显示时捕获点击事件 */
}

/* 遮罩层 */
.filter-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  transition: opacity 0.3s ease;
  pointer-events: auto; /* 确保遮罩层可点击 */
}

/* 移动端遮罩层 */
@media (max-width: 767px) {
  .filter-overlay {
    background: rgba(0, 0, 0, 0.5); /* 移动端加深背景 */
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
  box-shadow: -4px 0 20px rgba(0, 0, 0, 0.15);
  transform: translateX(100%);
  transition: transform 0.3s ease;
  display: flex;
  flex-direction: column;
  z-index: 2001; /* 确保面板在遮罩层之上 */
}

.domain-filter-panel.visible {
  transform: translateX(0);
}

/* 面板头部 */
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--color-border-default);
  background: white;
}

.panel-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.reset-link {
  background: none;
  border: none;
  color: var(--color-text-secondary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  text-decoration: underline;
  padding: 4px;
}

.reset-link:hover {
  color: var(--color-text-primary);
}

.close-btn {
  background: none;
  border: none;
  color: var(--color-text-secondary);
  font-size: 20px;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: #f5f5f5;
  color: var(--color-text-primary);
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
  margin: 0 0 16px 0;
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

/* 筛选按钮组 */
.filter-buttons-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

/* 移动端按钮组 */
@media (max-width: 767px) {
  .filter-buttons-group {
    gap: 8px;
  }
}

.filter-btn {
  padding: 12px 18px;
  border: 1px solid var(--color-border-default);
  border-radius: 2px;
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

/* 面板底部 */
.panel-footer {
  display: flex;
  gap: 12px;
  padding: 24px;
  border-top: 1px solid var(--color-border-default);
  background: white;
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

/* Location 区样式 */
.location-section .location-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.location-chip {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  border: 1px solid var(--color-border-default);
  border-radius: 2px;
  background: #fafbfc;
}
.location-chip .chip-text {
  font-size: 14px;
  color: var(--color-text-primary);
}
.location-chip .chip-remove {
  background: transparent;
  border: none;
  color: var(--color-text-secondary);
  width: 22px;
  height: 22px;
  border-radius: 6px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.location-chip .chip-remove:hover {
  background: #e5e7eb;
  color: var(--color-text-primary);
}
.location-actions {
  margin-top: 6px;
}
.clear-all {
  background: none;
  border: none;
  color: var(--color-text-secondary);
  text-decoration: underline;
  font-size: 13px;
  cursor: pointer;
}
.nearby-toggle {
  margin-top: 10px;
}

/* Location 空态提示 */
.location-empty .empty-box {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  border: 1px dashed var(--color-border-default, #e5e7eb);
  background: #fafafa;
  border-radius: 12px;
  padding: 10px 12px;
}
.location-empty .empty-text {
  font-size: 13px;
  color: var(--color-text-secondary, #6b7280);
}
.location-empty .go-select {
  background: none;
  border: none;
  color: var(--color-text-secondary);
  font-size: 13px;
  text-decoration: underline;
  cursor: pointer;
}


/* 移动端全屏模式 */
@media (max-width: 767px) {
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
    -webkit-text-size-adjust: 100%;
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

  /* iOS Safari 输入框 auto-zoom 规避：保证输入相关元素字号 ≥16px，避免聚焦触发页面放大 */
  .domain-filter-panel :deep(input),
  .domain-filter-panel :deep(textarea),
  .domain-filter-panel :deep(select),
  .domain-filter-panel :deep(.el-input__inner),
  .domain-filter-panel :deep(.el-input__wrapper) {
    /* iOS 自动放大阈值：确保输入字号 ≥16px；使用 !important 覆盖库内部样式 */
    font-size: 16px !important;
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
