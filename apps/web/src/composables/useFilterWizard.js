// 新的筛选向导 Composable - 简化版本
// 目标：线性四步流程，同时保持与 Pinia Store/URL 的单一数据源同步

import { ref, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { usePropertiesStore } from '@/stores/properties'
import { sanitizeQueryParams, isSameQuery } from '@/utils/query'

const createDefaultState = () => ({
  areas: [],
  bedrooms: null,
  priceRange: [0, 5000],
  bathrooms: null,
  parking: null,
  furnished: false,
  dateFrom: null,
  dateTo: null,
})

const parseDateValue = (value) => {
  if (!value) return null
  const date = new Date(value)
  return Number.isNaN(date.getTime()) ? null : date
}

const normalisePriceRange = (range) => {
  if (!Array.isArray(range) || range.length !== 2) {
    return [0, 5000]
  }
  const min = Number(range[0])
  const max = Number(range[1])
  const safeMin = Number.isFinite(min) ? Math.max(0, min) : 0
  const safeMax = Number.isFinite(max) ? Math.max(safeMin, max) : 5000
  return [safeMin, safeMax]
}

const createAreaEntry = (value, type) => {
  const name = String(value ?? '').trim()
  if (!name) return null

  if (type === 'postcode') {
    return {
      id: `postcode_${name}`,
      type: 'postcode',
      name,
      postcode: name,
      fullName: name,
    }
  }

  return {
    id: `suburb_${name}`,
    type: 'suburb',
    name,
    suburb: name,
    fullName: name,
  }
}

const cloneAreas = (areas) => (Array.isArray(areas) ? areas.map((area) => ({ ...area })) : [])

const formatDate = (date) => {
  if (!date) return null
  const d = new Date(date)
  if (Number.isNaN(d.getTime())) return null
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

const areaDisplayName = (area) => {
  if (!area) return ''
  if (area.type === 'postcode') {
    return `邮编 ${area.name || area.postcode || ''}`.trim()
  }
  return area.name || area.suburb || ''
}

export function useFilterWizard() {
  const propertiesStore = usePropertiesStore()
  const router = useRouter()
  const route = useRoute()

  const currentStep = ref(1)
  const filterState = ref(createDefaultState())

  const previewCount = ref(0)
  const isCountingLoading = ref(false)
  const countError = ref(null)

  const isStep1Valid = computed(() => filterState.value.areas.length > 0)
  const isStep2Valid = computed(() => filterState.value.bedrooms !== null)

  const canProceedToNext = computed(() => {
    switch (currentStep.value) {
      case 1:
        return isStep1Valid.value
      case 2:
        return isStep2Valid.value
      case 3:
      case 4:
        return true
      default:
        return false
    }
  })

  const stepTitles = {
    1: '选择区域',
    2: '选择房型',
    3: '设置条件',
    4: '确认搜索',
  }

  const currentStepTitle = computed(() => stepTitles[currentStep.value])

  const generateResultDescription = (count, filters) => {
    const { areas, bedrooms } = filters
    if (!Array.isArray(areas) || !areas.length || !bedrooms) {
      return `${count} 套房源`
    }

    const names = areas.map((area) => areaDisplayName(area)).filter(Boolean)
    const areaText = names.length > 3
      ? `${names.slice(0, 2).join('、')} 等 ${names.length} 个区域`
      : names.join('、')

    const bedroomText = bedrooms === '0' ? 'Studio' : bedrooms === '4+' ? '4房及以上' : `${bedrooms}房`
    return `在 ${areaText} 找到 ${count} 套 ${bedroomText} 房源`
  }

  const syncRouterQuery = async (params) => {
    const preserved = {}
    if (typeof route.query?.sort === 'string' && route.query.sort) {
      preserved.sort = route.query.sort
    }
    const rawQuery = { ...preserved, ...params }
    const nextQuery = sanitizeQueryParams(rawQuery)
    const currentQuery = sanitizeQueryParams(route.query || {})
    if (!isSameQuery(currentQuery, nextQuery)) {
      await router.replace({ query: nextQuery })
    }
  }

  const buildFilterParams = () => {
    const params = {}

    const suburbSet = new Set()
    const postcodeSet = new Set()
    ;(filterState.value.areas || []).forEach((area) => {
      if (!area) return
      const rawType = area.type || (String(area.id || '').startsWith('postcode_') ? 'postcode' : 'suburb')
      const value = String(area.name || area.suburb || area.postcode || '').trim()
      if (!value) return
      if (rawType === 'postcode') {
        postcodeSet.add(value)
      } else {
        suburbSet.add(value)
      }
    })

    if (suburbSet.size > 0) {
      params.suburb = Array.from(suburbSet).join(',')
    }
    if (postcodeSet.size > 0) {
      params.postcodes = Array.from(postcodeSet).join(',')
    }

    if (filterState.value.bedrooms) {
      params.bedrooms = String(filterState.value.bedrooms)
    }

    const [minPrice, maxPrice] = filterState.value.priceRange
    if (minPrice > 0) params.minPrice = minPrice
    if (maxPrice < 5000) params.maxPrice = maxPrice

    if (filterState.value.bathrooms) {
      params.bathrooms = String(filterState.value.bathrooms)
    }
    if (filterState.value.parking) {
      params.parking = String(filterState.value.parking)
    }
    if (filterState.value.furnished) {
      params.isFurnished = true
    }

    if (filterState.value.dateFrom) {
      params.date_from = formatDate(filterState.value.dateFrom)
    }
    if (filterState.value.dateTo) {
      params.date_to = formatDate(filterState.value.dateTo)
    }

    return params
  }

  let previewCountSeq = 0
  const updatePreviewCount = async () => {
    if (currentStep.value > 2) {
      isCountingLoading.value = false
      return
    }

    if (currentStep.value === 1 && !isStep1Valid.value) {
      previewCount.value = 0
      countError.value = null
      isCountingLoading.value = false
      return
    }

    if (currentStep.value === 2 && (!isStep1Valid.value || !isStep2Valid.value)) {
      previewCount.value = 0
      countError.value = null
      isCountingLoading.value = false
      return
    }

    const seq = ++previewCountSeq
    isCountingLoading.value = true
    countError.value = null

    try {
      const params = buildFilterParams()
      const count = await propertiesStore.getFilteredCount(params)

      if (seq !== previewCountSeq) return

      if (typeof count === 'number' && !Number.isNaN(count)) {
        previewCount.value = count
        countError.value = null
      } else {
        previewCount.value = 0
        countError.value = '结果数量暂不可用'
      }
    } catch (error) {
      if (seq !== previewCountSeq) return
      console.error('获取预览计数失败:', error)
      countError.value = '计数失败'
      previewCount.value = 0
    } finally {
      if (seq === previewCountSeq) {
        isCountingLoading.value = false
      }
    }
  }

  const goToStep = (step) => {
    if (step >= 1 && step <= 4) {
      currentStep.value = step
    }
  }

  const nextStep = () => {
    if (canProceedToNext.value && currentStep.value < 4) {
      currentStep.value += 1
    }
  }

  const prevStep = () => {
    if (currentStep.value > 1) {
      currentStep.value -= 1
    }
  }

  const applyFilters = async () => {
    try {
      const params = buildFilterParams()
      propertiesStore.setSelectedLocations(filterState.value.areas)
      await propertiesStore.applyFilters(params)
      await syncRouterQuery(params)
      return true
    } catch (error) {
      console.error('应用筛选失败:', error)
      return false
    }
  }

  const resetFilters = () => {
    filterState.value = createDefaultState()
    currentStep.value = 1
    previewCount.value = 0
    countError.value = null
  }

  const restoreFromQuery = (query = route.query || {}) => {
    try {
      const nextState = createDefaultState()
      const seen = new Set()
      const pushArea = (entry) => {
        if (!entry) return
        const key = entry.id || `${entry.type}_${entry.name}`
        if (seen.has(key)) return
        seen.add(key)
        nextState.areas.push(entry)
      }

      const suburbCsv = query.suburb || query.suburbs
      if (suburbCsv) {
        String(suburbCsv)
          .split(',')
          .map((item) => item.trim())
          .filter(Boolean)
          .forEach((name) => pushArea(createAreaEntry(name, 'suburb')))
      }

      if (query.postcodes) {
        String(query.postcodes)
          .split(',')
          .map((item) => item.trim())
          .filter(Boolean)
          .forEach((code) => pushArea(createAreaEntry(code, 'postcode')))
      }

      if (nextState.areas.length === 0 && Array.isArray(propertiesStore.selectedLocations)) {
        propertiesStore.selectedLocations.forEach((area) => {
          const entry = createAreaEntry(area?.postcode || area?.name || area?.suburb, area?.type)
          pushArea(entry)
        })
      }

      if (query.bedrooms) {
        nextState.bedrooms = String(query.bedrooms)
      } else if (propertiesStore.currentFilterParams?.bedrooms) {
        nextState.bedrooms = String(propertiesStore.currentFilterParams.bedrooms)
      }

      const minPrice = query.minPrice ?? query.price_min
      const maxPrice = query.maxPrice ?? query.price_max
      if (minPrice !== undefined || maxPrice !== undefined) {
        nextState.priceRange = normalisePriceRange([
          minPrice !== undefined ? Number(minPrice) : 0,
          maxPrice !== undefined ? Number(maxPrice) : 5000,
        ])
      } else if (
        propertiesStore.currentFilterParams?.minPrice !== undefined ||
        propertiesStore.currentFilterParams?.maxPrice !== undefined ||
        propertiesStore.currentFilterParams?.price_min !== undefined ||
        propertiesStore.currentFilterParams?.price_max !== undefined
      ) {
        nextState.priceRange = normalisePriceRange([
          propertiesStore.currentFilterParams.minPrice ?? propertiesStore.currentFilterParams.price_min ?? 0,
          propertiesStore.currentFilterParams.maxPrice ?? propertiesStore.currentFilterParams.price_max ?? 5000,
        ])
      }

      if (query.bathrooms) {
        nextState.bathrooms = String(query.bathrooms)
      } else if (propertiesStore.currentFilterParams?.bathrooms) {
        nextState.bathrooms = String(propertiesStore.currentFilterParams.bathrooms)
      }

      if (query.parking) {
        nextState.parking = String(query.parking)
      } else if (propertiesStore.currentFilterParams?.parking) {
        nextState.parking = String(propertiesStore.currentFilterParams.parking)
      }

      if (
        query.isFurnished === '1' ||
        query.isFurnished === 'true' ||
        query.furnished === '1' ||
        String(propertiesStore.currentFilterParams?.isFurnished) === 'true' ||
        propertiesStore.currentFilterParams?.furnished === true
      ) {
        nextState.furnished = true
      }

      if (query.date_from) {
        nextState.dateFrom = parseDateValue(query.date_from)
      } else if (propertiesStore.currentFilterParams?.date_from) {
        nextState.dateFrom = parseDateValue(propertiesStore.currentFilterParams.date_from)
      }

      if (query.date_to) {
        nextState.dateTo = parseDateValue(query.date_to)
      } else if (propertiesStore.currentFilterParams?.date_to) {
        nextState.dateTo = parseDateValue(propertiesStore.currentFilterParams.date_to)
      }

      filterState.value = {
        areas: nextState.areas,
        bedrooms: nextState.bedrooms,
        priceRange: [...nextState.priceRange],
        bathrooms: nextState.bathrooms,
        parking: nextState.parking,
        furnished: nextState.furnished,
        dateFrom: nextState.dateFrom,
        dateTo: nextState.dateTo,
      }

      propertiesStore.setSelectedLocations(filterState.value.areas)
    } catch (error) {
      console.warn('从URL恢复筛选状态失败:', error)
    }
  }

  watch(
    [() => filterState.value.areas, () => filterState.value.bedrooms],
    () => {
      updatePreviewCount()
    },
    { deep: true },
  )

  watch(
    () => route.query,
    (next) => {
      restoreFromQuery(next)
    },
    { deep: true },
  )

  const saveSearch = async (searchName, emailFrequency = 'daily') => {
    try {
      const savedSearch = {
        id: Date.now().toString(),
        name: searchName.trim(),
        emailFrequency,
        conditions: {
          areas: cloneAreas(filterState.value.areas),
          bedrooms: filterState.value.bedrooms,
          priceRange: [...filterState.value.priceRange],
          bathrooms: filterState.value.bathrooms,
          parking: filterState.value.parking,
          furnished: filterState.value.furnished,
          dateFrom: filterState.value.dateFrom ? filterState.value.dateFrom.toISOString() : null,
          dateTo: filterState.value.dateTo ? filterState.value.dateTo.toISOString() : null,
        },
        filterParams: { ...buildFilterParams() },
        createdAt: new Date().toISOString(),
        lastNotified: null,
      }

      const existingSaves = JSON.parse(localStorage.getItem('savedSearches') || '[]')
      existingSaves.push(savedSearch)
      localStorage.setItem('savedSearches', JSON.stringify(existingSaves))

      return savedSearch
    } catch (error) {
      console.error('保存搜索失败:', error)
      throw error
    }
  }

  const getSavedSearches = () => {
    try {
      return JSON.parse(localStorage.getItem('savedSearches') || '[]')
    } catch (error) {
      console.error('获取已保存搜索失败:', error)
      return []
    }
  }

  const deleteSavedSearch = (searchId) => {
    try {
      const existingSaves = getSavedSearches()
      const filtered = existingSaves.filter((search) => search.id !== searchId)
      localStorage.setItem('savedSearches', JSON.stringify(filtered))
      return true
    } catch (error) {
      console.error('删除已保存搜索失败:', error)
      return false
    }
  }

  const applySavedSearch = async (savedSearch) => {
    try {
      if (savedSearch.conditions) {
        const nextState = createDefaultState()
        const source = savedSearch.conditions
        nextState.areas = cloneAreas(source.areas)
        nextState.bedrooms = source.bedrooms ?? null
        nextState.priceRange = normalisePriceRange(source.priceRange)
        nextState.bathrooms = source.bathrooms ?? null
        nextState.parking = source.parking ?? null
        nextState.furnished = !!source.furnished
        nextState.dateFrom = parseDateValue(source.dateFrom)
        nextState.dateTo = parseDateValue(source.dateTo)

        filterState.value = {
          areas: nextState.areas,
          bedrooms: nextState.bedrooms,
          priceRange: [...nextState.priceRange],
          bathrooms: nextState.bathrooms,
          parking: nextState.parking,
          furnished: nextState.furnished,
          dateFrom: nextState.dateFrom,
          dateTo: nextState.dateTo,
        }

        propertiesStore.setSelectedLocations(filterState.value.areas)
      }

      const params = savedSearch.filterParams ? { ...savedSearch.filterParams } : buildFilterParams()
      await propertiesStore.applyFilters(params)
      const appliedQuery = sanitizeQueryParams(
        propertiesStore.currentFilterParams && Object.keys(propertiesStore.currentFilterParams).length
          ? propertiesStore.currentFilterParams
          : params,
      )
      await syncRouterQuery(appliedQuery)
      return appliedQuery
    } catch (error) {
      console.error('应用已保存搜索失败:', error)
      return null
    }
  }

  const generateSearchNameSuggestion = () => {
    const { areas, bedrooms, priceRange, furnished } = filterState.value
    let name = ''

    if (areas.length > 0) {
      const names = areas.map((area) => areaDisplayName(area)).filter(Boolean)
      if (names.length === 1) {
        name += names[0]
      } else if (names.length > 1) {
        name += `${names[0]} 等 ${names.length} 个区域`
      }
    }

    if (bedrooms) {
      const bedroomText = bedrooms === '0' ? 'Studio' : bedrooms === '4+' ? '4房及以上' : `${bedrooms}房`
      name += name ? ` ${bedroomText}` : bedroomText
    }

    if (priceRange && Array.isArray(priceRange)) {
      const [min, max] = priceRange
      if (min > 0 || max < 5000) {
        const priceText = min > 0 && max < 5000 ? `$${min}-${max}` : min > 0 ? `≥$${min}` : `≤$${max}`
        name += name ? ` ${priceText}` : priceText
      }
    }

    if (furnished) {
      name += name ? ' 有家具' : '有家具房源'
    }

    return name || '我的搜索'
  }

  restoreFromQuery(route.query)

  return {
    currentStep,
    filterState,
    previewCount,
    isCountingLoading,
    countError,
    isStep1Valid,
    isStep2Valid,
    canProceedToNext,
    currentStepTitle,
    goToStep,
    nextStep,
    prevStep,
    updatePreviewCount,
    applyFilters,
    resetFilters,
    restoreFromQuery,
    generateResultDescription,
    buildFilterParams,
    saveSearch,
    getSavedSearches,
    deleteSavedSearch,
    applySavedSearch,
    generateSearchNameSuggestion,
  }
}
