// 新的筛选向导 Composable - 简化版本
// 目标：线性四步流程，减少复杂状态管理

import { ref, computed, watch } from 'vue'
import { usePropertiesStore } from '@/stores/properties'
import { useRouter, useRoute } from 'vue-router'

export function useFilterWizard() {
  const propertiesStore = usePropertiesStore()
  const router = useRouter()
  const route = useRoute()

  // 当前步骤 (1-4)
  const currentStep = ref(1)

  // 筛选状态 - 简化结构
  const filterState = ref({
    // 步骤1: 区域选择 (必选)
    areas: [],

    // 步骤2: 房型选择 (必选)
    bedrooms: null,

    // 步骤3: 其他条件 (可选)
    priceRange: [0, 5000],
    bathrooms: null,
    parking: null,
    furnished: false,

    // 步骤4: 时间条件 (可选)
    dateFrom: null,
    dateTo: null
  })

  // 实时计数状态
  const previewCount = ref(0)
  const isCountingLoading = ref(false)
  const countError = ref(null)

  // 步骤验证
  const isStep1Valid = computed(() => {
    return filterState.value.areas.length > 0
  })

  const isStep2Valid = computed(() => {
    return filterState.value.bedrooms !== null
  })

  const canProceedToNext = computed(() => {
    switch (currentStep.value) {
      case 1: return isStep1Valid.value
      case 2: return isStep2Valid.value
      case 3: return true // 可选步骤
      case 4: return true // 可选步骤
      default: return false
    }
  })

  // 步骤标题
  const stepTitles = {
    1: '选择区域',
    2: '选择房型',
    3: '设置条件',
    4: '确认搜索'
  }

  const currentStepTitle = computed(() => stepTitles[currentStep.value])

  // 生成智能的结果描述
  const generateResultDescription = (count, filters) => {
    const { areas, bedrooms } = filters

    if (!areas.length || !bedrooms) {
      return `${count} 套房源`
    }

    // 区域描述
    const areaNames = areas.map(a => a.name || a.suburb || a)
    const areaText = areaNames.length > 3
      ? `${areaNames.slice(0, 2).join('、')} 等 ${areaNames.length} 个区域`
      : areaNames.join('、')

    // 房型描述
    const bedroomText = bedrooms === '0' ? 'Studio'
      : bedrooms === '4+' ? '4房及以上'
      : `${bedrooms}房`

    return `在 ${areaText} 找到 ${count} 套 ${bedroomText} 房源`
  }

  // 构建筛选参数
  const buildFilterParams = () => {
    const params = {}

    // 区域参数
    if (filterState.value.areas.length > 0) {
      const suburbs = filterState.value.areas
        .filter(area => area.type === 'suburb' || !area.type)
        .map(area => area.name || area.suburb || area)
        .filter(Boolean)

      if (suburbs.length > 0) {
        params.suburb = suburbs.join(',')
      }
    }

    // 房型参数
    if (filterState.value.bedrooms) {
      params.bedrooms = filterState.value.bedrooms
    }

    // 价格参数
    const [minPrice, maxPrice] = filterState.value.priceRange
    if (minPrice > 0) params.minPrice = minPrice
    if (maxPrice < 5000) params.maxPrice = maxPrice

    // 其他条件
    if (filterState.value.bathrooms) {
      params.bathrooms = filterState.value.bathrooms
    }
    if (filterState.value.parking) {
      params.parking = filterState.value.parking
    }
    if (filterState.value.furnished) {
      params.isFurnished = true
    }

    // 日期条件
    if (filterState.value.dateFrom) {
      params.date_from = formatDate(filterState.value.dateFrom)
    }
    if (filterState.value.dateTo) {
      params.date_to = formatDate(filterState.value.dateTo)
    }

    return params
  }

  // 格式化日期
  const formatDate = (date) => {
    if (!date) return null
    const d = new Date(date)
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
  }

  // 获取预览计数 (步骤1-2实时，步骤3-4不实时)
  const updatePreviewCount = async () => {
    // 只在步骤1-2进行实时计数
    if (currentStep.value > 2) return

    // 验证必要条件
    if (currentStep.value === 1 && !isStep1Valid.value) {
      previewCount.value = 0
      return
    }

    if (currentStep.value === 2 && (!isStep1Valid.value || !isStep2Valid.value)) {
      previewCount.value = 0
      return
    }

    isCountingLoading.value = true
    countError.value = null

    try {
      const params = buildFilterParams()
      const count = await propertiesStore.getFilteredCount(params)
      previewCount.value = count || 0
    } catch (error) {
      console.error('获取预览计数失败:', error)
      countError.value = '计数失败'
      previewCount.value = 0
    } finally {
      isCountingLoading.value = false
    }
  }

  // 步骤导航
  const goToStep = (step) => {
    if (step >= 1 && step <= 4) {
      currentStep.value = step
    }
  }

  const nextStep = () => {
    if (canProceedToNext.value && currentStep.value < 4) {
      currentStep.value++
    }
  }

  const prevStep = () => {
    if (currentStep.value > 1) {
      currentStep.value--
    }
  }

  // 应用筛选
  const applyFilters = async () => {
    try {
      const params = buildFilterParams()

      // 设置选中区域到store
      propertiesStore.setSelectedLocations(filterState.value.areas)

      // 应用筛选
      await propertiesStore.applyFilters(params)

      // 更新URL
      const query = { ...params }
      // 清理空值
      Object.keys(query).forEach(key => {
        if (query[key] === null || query[key] === undefined || query[key] === '') {
          delete query[key]
        }
      })

      await router.replace({ query })

      return true
    } catch (error) {
      console.error('应用筛选失败:', error)
      return false
    }
  }

  // 重置筛选
  const resetFilters = () => {
    filterState.value = {
      areas: [],
      bedrooms: null,
      priceRange: [0, 5000],
      bathrooms: null,
      parking: null,
      furnished: false,
      dateFrom: null,
      dateTo: null
    }
    currentStep.value = 1
    previewCount.value = 0
  }

  // 从URL恢复状态
  const restoreFromQuery = (query) => {
    try {
      // 恢复区域
      if (query.suburb) {
        const suburbNames = String(query.suburb).split(',').map(s => s.trim()).filter(Boolean)
        filterState.value.areas = suburbNames.map(name => ({
          id: `suburb_${name}`,
          type: 'suburb',
          name,
          suburb: name
        }))
      }

      // 恢复房型
      if (query.bedrooms) {
        filterState.value.bedrooms = String(query.bedrooms)
      }

      // 恢复价格
      if (query.minPrice || query.maxPrice) {
        const min = query.minPrice ? Number(query.minPrice) : 0
        const max = query.maxPrice ? Number(query.maxPrice) : 5000
        filterState.value.priceRange = [min, max]
      }

      // 恢复其他条件
      if (query.bathrooms) {
        filterState.value.bathrooms = String(query.bathrooms)
      }
      if (query.parking) {
        filterState.value.parking = String(query.parking)
      }
      if (query.isFurnished === '1' || query.isFurnished === 'true') {
        filterState.value.furnished = true
      }

      // 恢复日期
      if (query.date_from) {
        filterState.value.dateFrom = new Date(query.date_from)
      }
      if (query.date_to) {
        filterState.value.dateTo = new Date(query.date_to)
      }

    } catch (error) {
      console.warn('从URL恢复筛选状态失败:', error)
    }
  }

  // 监听区域和房型变化，自动更新计数
  watch([() => filterState.value.areas, () => filterState.value.bedrooms], () => {
    updatePreviewCount()
  }, { deep: true })

  // 保存搜索功能
  const saveSearch = async (searchName, emailFrequency = 'daily') => {
    try {
      const savedSearch = {
        id: Date.now().toString(),
        name: searchName.trim(),
        emailFrequency,
        conditions: {
          areas: filterState.value.areas,
          bedrooms: filterState.value.bedrooms,
          priceRange: filterState.value.priceRange,
          bathrooms: filterState.value.bathrooms,
          parking: filterState.value.parking,
          furnished: filterState.value.furnished,
          dateFrom: filterState.value.dateFrom,
          dateTo: filterState.value.dateTo
        },
        filterParams: buildFilterParams(),
        createdAt: new Date().toISOString(),
        lastNotified: null
      }

      // 保存到本地存储
      const existingSaves = JSON.parse(localStorage.getItem('savedSearches') || '[]')
      existingSaves.push(savedSearch)
      localStorage.setItem('savedSearches', JSON.stringify(existingSaves))

      return savedSearch
    } catch (error) {
      console.error('保存搜索失败:', error)
      throw error
    }
  }

  // 获取已保存的搜索
  const getSavedSearches = () => {
    try {
      return JSON.parse(localStorage.getItem('savedSearches') || '[]')
    } catch (error) {
      console.error('获取已保存搜索失败:', error)
      return []
    }
  }

  // 删除已保存的搜索
  const deleteSavedSearch = (searchId) => {
    try {
      const existingSaves = getSavedSearches()
      const filtered = existingSaves.filter(search => search.id !== searchId)
      localStorage.setItem('savedSearches', JSON.stringify(filtered))
      return true
    } catch (error) {
      console.error('删除已保存搜索失败:', error)
      return false
    }
  }

  // 应用已保存的搜索
  const applySavedSearch = async (savedSearch) => {
    try {
      // 恢复筛选状态
      if (savedSearch.conditions) {
        filterState.value = { ...savedSearch.conditions }
      }

      // 设置选中区域到store
      if (savedSearch.conditions.areas) {
        propertiesStore.setSelectedLocations(savedSearch.conditions.areas)
      }

      // 应用筛选
      const params = savedSearch.filterParams || buildFilterParams()
      await propertiesStore.applyFilters(params)

      // 更新URL
      const query = { ...params }
      Object.keys(query).forEach(key => {
        if (query[key] === null || query[key] === undefined || query[key] === '') {
          delete query[key]
        }
      })

      await router.replace({ query })

      return true
    } catch (error) {
      console.error('应用已保存搜索失败:', error)
      return false
    }
  }

  // 生成搜索名称建议
  const generateSearchNameSuggestion = () => {
    const { areas, bedrooms, priceRange, furnished } = filterState.value

    let name = ''

    // 区域部分
    if (areas.length > 0) {
      const areaNames = areas.map(area => area.name || area.suburb).filter(Boolean)
      if (areaNames.length === 1) {
        name += areaNames[0]
      } else if (areaNames.length > 1) {
        name += `${areaNames[0]} 等 ${areaNames.length} 个区域`
      }
    }

    // 房型部分
    if (bedrooms) {
      const bedroomText = bedrooms === '0' ? 'Studio'
        : bedrooms === '4+' ? '4房及以上'
        : `${bedrooms}房`
      name += name ? ` ${bedroomText}` : bedroomText
    }

    // 价格部分
    if (priceRange && Array.isArray(priceRange)) {
      const [min, max] = priceRange
      if (min > 0 || max < 5000) {
        const priceText = min > 0 && max < 5000
          ? `$${min}-${max}`
          : min > 0 ? `≥$${min}` : `≤$${max}`
        name += name ? ` ${priceText}` : priceText
      }
    }

    // 家具要求
    if (furnished) {
      name += name ? ' 有家具' : '有家具房源'
    }

    return name || '我的搜索'
  }

  // 初始化时从URL恢复
  if (route.query && Object.keys(route.query).length > 0) {
    restoreFromQuery(route.query)
  }

  return {
    // 状态
    currentStep,
    filterState,
    previewCount,
    isCountingLoading,
    countError,

    // 计算属性
    isStep1Valid,
    isStep2Valid,
    canProceedToNext,
    currentStepTitle,

    // 方法
    goToStep,
    nextStep,
    prevStep,
    updatePreviewCount,
    applyFilters,
    resetFilters,
    restoreFromQuery,
    generateResultDescription,
    buildFilterParams,

    // 保存搜索功能
    saveSearch,
    getSavedSearches,
    deleteSavedSearch,
    applySavedSearch,
    generateSearchNameSuggestion
  }
}
