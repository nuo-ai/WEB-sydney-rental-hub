// JUWO桔屋找房 - 房源数据状态管理

import { defineStore } from 'pinia'
import { propertyAPI, locationAPI } from '@/services/api'

// 特性开关：V2 参数映射（默认关闭以保持向后兼容）
// 说明：开启后将把前端筛选状态映射为统一的后端白名单参数（suburbs/price_min/...）
// 风险控制：若后端未识别新参数，关闭开关即可回退到旧行为
const enableFilterV2 = false

// 小工具：格式化日期为 YYYY-MM-DD（避免各处重复实现）
const _fmtDate = (date) => {
  if (!date) return null
  const d = new Date(date)
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}

/**
 * 统一的筛选参数映射函数（V1→V2 兼容层）
 * 为什么：抽离参数构造，保持“组件只触发 action，契约在 store 统一管理”，
 * 并为后续切换到契约一致性的 V2 做铺垫（开启开关即可切换）
 */
const mapFilterStateToApiParams = (
  rawFilters = {},
  selectedLocations = [],
  paging = {},
  opts = { enableFilterV2: false },
) => {
  // V1：保持现有键名与行为，确保零风险上线
  if (!opts.enableFilterV2) {
    const legacy = { ...rawFilters }
    // 中文注释：P0 兼容——在 V1 契约下移除仅用于 V2 的键；如选择 v1 契约，则把 isFurnished 映射为后端可识别的 is_furnished=1
    if ('isFurnished' in legacy) {
      // 中文注释：V1 后端接收 isFurnished 布尔；需兼容 URL/字符串/数字形式（'1'/'true'/1/true/'yes'）
      const v = legacy.isFurnished
      const truthy = v === true || v === '1' || v === 1 || v === 'true' || v === 'yes'
      if (truthy) {
        legacy.isFurnished = true
      } else {
        delete legacy.isFurnished
      }
    }

    // 若组件侧未补齐 suburb，则基于已选区域填充（与历史行为一致）
    if (!legacy.suburb && Array.isArray(selectedLocations) && selectedLocations.length) {
      const suburbs = selectedLocations
        .filter((l) => l && (l.type ? l.type === 'suburb' : true))
        .map((l) => l.name)
        .filter(Boolean)
      if (suburbs.length) legacy.suburb = suburbs.join(',')
    }

    // 透传日期（若来自 Date 对象，统一格式化）
    if (legacy.date_from && legacy.date_from instanceof Date) {
      legacy.date_from = _fmtDate(legacy.date_from)
    }
    if (legacy.date_to && legacy.date_to instanceof Date) {
      legacy.date_to = _fmtDate(legacy.date_to)
    }

    // 注入分页（上限控制留给调用方）
    if (paging.page) legacy.page = paging.page
    if (paging.page_size) legacy.page_size = paging.page_size
    if (paging.sort) legacy.sort = paging.sort

    return legacy
  }

  // V2：对齐白名单参数（suburbs/date_from/date_to/price_min/price_max/bedrooms/page/page_size/sort）
  const params = {}

  // 中文注释：白名单透传已存在的 V2 键，避免预览计数丢参（如 currentFilterParams 中已有的 V2 字段）
  const _wl = ['suburbs','postcodes','date_from','date_to','price_min','price_max','bedrooms','furnished','bathrooms_min','parking_min','sort','include_nearby']
  _wl.forEach((k) => {
    const v = rawFilters[k]
    if (v !== undefined && v !== null && v !== '') {
      params[k] = v
    }
  })

  // suburbs（仅 suburb 类型，去重 + 保序）
  const suburbs = Array.from(
    new Set(
      (selectedLocations || [])
        .filter((l) => l && l.type === 'suburb')
        .map((l) => l.name)
        .filter(Boolean),
    ),
  )
  if (!params.suburbs && suburbs.length) params.suburbs = suburbs.join(',')
  // 中文注释：兜底——当开启 V2 映射但区域仍以 V1 键 suburb 存在时，转换为 V2 键 suburbs，避免计数丢失区域导致“全库总量”
  if (!params.suburbs && rawFilters.suburb) params.suburbs = String(rawFilters.suburb)
  // postcodes（仅 postcode 类型，V2 才参与映射）
  const postcodes = Array.from(
    new Set(
      (selectedLocations || [])
        .filter((l) => l && l.type === 'postcode')
        .map((l) => l.name)
        .filter(Boolean),
    ),
  )
  if (!params.postcodes && postcodes.length) params.postcodes = postcodes.join(',')

  // 日期（闭区间），接受 Date 或字符串
  if (rawFilters.startDate) params.date_from = _fmtDate(rawFilters.startDate) || rawFilters.date_from
  if (rawFilters.endDate) params.date_to = _fmtDate(rawFilters.endDate) || rawFilters.date_to
  if (!params.date_from && rawFilters.date_from) params.date_from = rawFilters.date_from
  if (!params.date_to && rawFilters.date_to) params.date_to = rawFilters.date_to

  // 价格：兼容 priceRange 或 minPrice/maxPrice
  let min = 0
  let max = 5000
  if (Array.isArray(rawFilters.priceRange)) {
    ;[min, max] = rawFilters.priceRange
  } else {
    min = Number(rawFilters.minPrice ?? 0)
    max = Number(rawFilters.maxPrice ?? 5000)
  }
  if (min > max) [min, max] = [max, min] // 纠偏以降低用户困惑
  if (params.price_min == null && min > 0) params.price_min = min
  if (params.price_max == null && max < 5000) params.price_max = max

  // 卧室：最小卧室数（支持 '4+' → 4），兼容字符串或 CSV
  if (rawFilters.bedrooms) {
    const b = Array.isArray(rawFilters.bedrooms)
      ? rawFilters.bedrooms[0]
      : String(rawFilters.bedrooms).split(',')[0]
    if (params.bedrooms == null && b) params.bedrooms = b.endsWith('+') ? parseInt(b) : parseInt(b)
  }

  // 分页/排序（含上限 50）
  const page = Number(paging.page ?? 1)
  let pageSize = Number(paging.page_size ?? 20)
  pageSize = Math.min(Math.max(pageSize, 1), 50)
  params.page = page
  params.page_size = pageSize
  if (paging.sort) params.sort = paging.sort

  // 扩展：家具/浴室/车位（V2 才启用）
  // 为什么：与“白名单 + 下限语义”保持一致，避免在多位/any 表达上产生歧义
  if (params.furnished == null && rawFilters.isFurnished === true) {
    params.furnished = true
  }
  // 浴室下限：'any' 省略；'3+' -> 3；'2' -> 2
  if (params.bathrooms_min == null && rawFilters.bathrooms) {
    const bRaw = Array.isArray(rawFilters.bathrooms)
      ? rawFilters.bathrooms[0]
      : String(rawFilters.bathrooms).split(',')[0]
    if (bRaw && bRaw !== 'any') {
      const bMin = bRaw.endsWith('+') ? parseInt(bRaw) : parseInt(bRaw)
      if (!Number.isNaN(bMin)) params.bathrooms_min = bMin
    }
  }
  // 车位下限：'any' 省略；'2+' -> 2；'0' -> 0（有效）
  if (params.parking_min == null && rawFilters.parking) {
    const pRaw = Array.isArray(rawFilters.parking)
      ? rawFilters.parking[0]
      : String(rawFilters.parking).split(',')[0]
    if (pRaw && pRaw !== 'any') {
      const pMin = pRaw.endsWith('+') ? parseInt(pRaw) : parseInt(pRaw)
      if (!Number.isNaN(pMin)) params.parking_min = pMin
    }
  }

  // 删除空值
  Object.keys(params).forEach((k) => {
    if (params[k] === '' || params[k] === null || typeof params[k] === 'undefined') {
      delete params[k]
    }
  })

  return params
}

/**
 * 特性开关：在未全局开启的情况下，检测是否包含 V2 扩展键以“按需启用”V2 映射
 * 为什么：More 面板产生的是 isFurnished/bathrooms/parking 等键；当出现这些键时应切换到 V2 白名单映射，
 * 避免以 V1 键名（如 isFurnished）请求导致后端不识别。
 */

// 特性开关守卫工具：检测是否已选择“区域”（suburb/postcode）
// 目的：在 UI 禁用之外，增加 Store 侧的早返回保护，避免无意义的接口请求
const hasRegionSelected = (selectedLocations = []) => {
  try {
    return (
      Array.isArray(selectedLocations) &&
      selectedLocations.some((l) => l && (l.type === 'suburb' || l.type === 'postcode'))
    )
  } catch {
    return false
  }
}

export const usePropertiesStore = defineStore('properties', {
  state: () => ({
    // 房源数据
    allProperties: [],
    filteredProperties: [],
    currentProperty: null,

    // 加载状态
    loading: false,
    error: null,

    // 分页状态 (服务端分页)
    currentPage: 1,
    pageSize: 20,
    totalCount: 0,
    totalPages: 0,
    hasNext: false,
    hasPrev: false,

    // 搜索状态
    searchQuery: '',
    selectedLocations: [],

    // 区域缓存（15分钟TTL）
    areasCache: { list: [], ts: 0 },

    // 收藏状态 (localStorage作为临时方案)
    favoriteIds: JSON.parse(localStorage.getItem('juwo-favorites') || '[]'),
    favoritePropertiesData: [],

    // 历史记录
    viewHistory: JSON.parse(localStorage.getItem('juwo-history') || '[]'),

    // 对比状态
    compareIds: JSON.parse(localStorage.getItem('juwo-compare') || '[]'),

    // 特性开关（集中管理回滚策略）
    // requireRegionBeforeFilter: 启用后，未选择区域（suburb/postcode）将禁用筛选并在 Store 侧早返回
      featureFlags: {
        requireRegionBeforeFilter: false,
      },

    // 当前已应用的筛选参数（用于翻页/改每页大小时保持筛选条件）
    currentFilterParams: {},
    // 全局“草稿”聚合（各面板未应用的改动，按 section 聚合；用于统一预览计数口径）
    previewDraftSections: {},
    // 排序状态（UI占位；后端暂不识别时仅透传且不做前端本地排序）
    sort: '',
  }),

  getters: {
    // 获取当前页的房源 (使用服务端分页后，直接返回filteredProperties)
    paginatedProperties: (state) => {
      return state.filteredProperties
    },

    // 检查是否为收藏房源
    isFavorite: (state) => {
      return (propertyId) => state.favoriteIds.includes(String(propertyId))
    },

    // 获取收藏房源列表
    favoriteProperties: (state) => {
      // 优先从专门的收藏数据中获取
      if (state.favoritePropertiesData.length > 0) {
        return state.favoritePropertiesData
      }
      // 兼容旧逻辑：从allProperties中过滤
      return state.allProperties.filter((property) =>
        state.favoriteIds.includes(String(property.listing_id)),
      )
    },

    // 获取区域建议数据
    locationSuggestions: (state) => {
      const locationMap = new Map()

      state.allProperties.forEach((property) => {
        // 处理区域 (suburb)
        if (property.suburb) {
          const suburb = property.suburb.trim()
          const postcode = property.postcode ? Math.floor(property.postcode).toString() : ''
          const key = `${suburb}_${postcode}`

          if (!locationMap.has(key)) {
            locationMap.set(key, {
              id: key,
              type: 'suburb',
              name: suburb,
              postcode: postcode,
              fullName: postcode ? `${suburb} NSW ${postcode}` : suburb,
              count: 0,
            })
          }
          locationMap.get(key).count++
        }

        // 处理邮编 (postcode)
        if (property.postcode) {
          const postcode = Math.floor(property.postcode).toString()
          const suburb = property.suburb ? property.suburb.trim() : ''
          const key = `postcode_${postcode}`

          if (!locationMap.has(key)) {
            locationMap.set(key, {
              id: key,
              type: 'postcode',
              name: postcode,
              suburb: suburb,
              fullName: suburb ? `${postcode} (${suburb})` : postcode,
              count: 0,
            })
          }
          locationMap.get(key).count++
        }
      })

      return Array.from(locationMap.values()).sort((a, b) => b.count - a.count)
    },
  },

  actions: {
    // 获取房源列表 - 优化版，直接使用服务端分页
    async fetchProperties(params = {}) {
      this.loading = true
      this.error = null

      try {
        // 合并分页参数，优先使用传入的参数
        const paginationParams = {
          page: params.page || this.currentPage,
          page_size: params.page_size || this.pageSize,
          ...params,
        }

        // 若已有“已应用的筛选条件”，翻页/改每页大小时需要与之合并，保持条件不丢失
        let requestParams = paginationParams
        if (this.currentFilterParams && Object.keys(this.currentFilterParams).length) {
          // Store 守卫：当强制要求先选区域时，未选区域直接短路返回，避免无意义请求
          if (this.featureFlags?.requireRegionBeforeFilter && !hasRegionSelected(this.selectedLocations)) {
            this.filteredProperties = []
            this.totalCount = 0
            this.totalPages = 0
            this.hasNext = false
            this.hasPrev = false
            this.currentPage = 1
            this.loading = false
            return
          }
          requestParams = { ...this.currentFilterParams, ...paginationParams }
        }
        // 显式以本次分页为最高优先级，防止任何历史值（含 page_size=1）污染
        requestParams.page = paginationParams.page
        requestParams.page_size = paginationParams.page_size

        const t0 = typeof performance !== 'undefined' && performance.now ? performance.now() : Date.now()
        const response = await propertyAPI.getListWithPagination(requestParams)
        const t1 = typeof performance !== 'undefined' && performance.now ? performance.now() : Date.now()
        const dur = t1 - t0
        if (dur > 800) {
          console.warn(`[FILTER-PERF] fetchProperties p95 threshold exceeded: ${Math.round(dur)} ms`, paginationParams)
        }

        // 更新数据
        this.filteredProperties = response.data || []

        // 更新分页信息
        if (response.pagination) {
          this.totalCount = response.pagination.total
          this.totalPages = response.pagination.pages
          this.hasNext = response.pagination.has_next
          this.hasPrev = response.pagination.has_prev
        }

        // 暂时禁用自动加载基础数据，提升首次加载速度
        // 仅在用户真正使用搜索功能时才加载
        // if (this.allProperties.length === 0 && !params.suburb) {
        //   this.loadBaseDataAsync()
        // }
      } catch (error) {
        this.error = error.message || '获取房源数据失败'
        console.error('❌ 房源数据加载失败:', error)
      } finally {
        this.loading = false
      }
    },

    // 异步加载基础数据（用于搜索建议）
    async loadBaseDataAsync() {
      try {
        // 只加载第一批100条数据用于搜索建议
        const baseData = await propertyAPI.getList({ page_size: 100 })
        this.allProperties = baseData
      } catch (error) {
        console.warn('⚠️ 加载基础数据失败，搜索建议功能可能受影响:', error)
      }
    },

    // 获取全量区域目录（A→Z），TTL=15分钟
    // 为什么：AreasSelector 需要完整区域清单进行分组/多选；优先走后端接口，失败时从前端数据回退推导
    async getAllAreas() {
      try {
        const now = Date.now()
        const TTL = 15 * 60 * 1000
        if (
          this.areasCache?.ts &&
          now - this.areasCache.ts < TTL &&
          Array.isArray(this.areasCache.list) &&
          this.areasCache.list.length
        ) {
          return this.areasCache.list
        }

        // 优先从后端接口获取
        let list = []
        try {
          const remote = await locationAPI.getAllLocations()
          if (Array.isArray(remote) && remote.length) {
            list = remote
          }
        } catch {
          // 忽略接口错误，采用前端回退
        }

        // 若本地无基础数据，尝试懒加载一批用于构建目录
        if (!list.length && (!Array.isArray(this.allProperties) || this.allProperties.length === 0)) {
          try {
            await this.loadBaseDataAsync()
          } catch (err) {
            // 中文注释：忽略懒加载失败，仅用于区域目录兜底；不中断流程
            console.warn('getAllAreas: loadBaseDataAsync failed (ignored)', err)
          }
        }

        // 回退：从已加载的数据推导（优先 allProperties，其次 filteredProperties）
        if (!list.length) {
          const source = (Array.isArray(this.allProperties) && this.allProperties.length)
            ? this.allProperties
            : (Array.isArray(this.filteredProperties) ? this.filteredProperties : [])
          if (source.length) {
            const map = new Map()
            for (const p of source) {
              const suburb = p?.suburb && String(p.suburb).trim()
              const postcode = p?.postcode != null ? String(Math.floor(p.postcode)) : ''
              if (suburb) {
                const id = `suburb_${suburb}`
                if (!map.has(id)) {
                  map.set(id, {
                    id,
                    type: 'suburb',
                    name: suburb,
                    postcode,
                    fullName: postcode ? `${suburb} NSW ${postcode}` : suburb,
                  })
                }
              }
              if (postcode) {
                const id = `postcode_${postcode}`
                if (!map.has(id)) {
                  map.set(id, {
                    id,
                    type: 'postcode',
                    name: postcode,
                    fullName: postcode,
                  })
                }
              }
            }
            list = Array.from(map.values())
          }
        }

        // 写入缓存
        this.areasCache = { list, ts: now }
        return list
      } catch {
        return []
      }
    },

    // 获取房源详情 - 优化版
    async fetchPropertyDetail(id) {
      // 统一转换为字符串进行比较（解决类型不匹配问题）
      const idStr = String(id)

      // 设置加载状态
      this.loading = true
      this.error = null

      try {
        // 尝试从当前列表、所有属性或当前已加载的房源中获取基础数据
        let existingProperty =
          this.filteredProperties.find((p) => String(p.listing_id) === idStr) ||
          this.allProperties.find((p) => String(p.listing_id) === idStr) ||
          (this.currentProperty && String(this.currentProperty.listing_id) === idStr
            ? this.currentProperty
            : null)

        // 如果在前端状态中找不到，则直接从列表API获取基础数据
        if (!existingProperty) {
          const listResponse = await propertyAPI.getListWithPagination({ listing_id: idStr })
          if (listResponse.data && listResponse.data.length > 0) {
            existingProperty = listResponse.data[0]
          }
        }

        // 如果有基础数据，先显示，避免白屏
        if (existingProperty) {
          this.currentProperty = existingProperty
        }

        // 获取更详细的房源信息（例如，描述）
        const fullPropertyDetails = await propertyAPI.getDetail(id)

        // 智能合并数据：以现有数据为基础，用详情数据进行补充
        // 这样可以确保即使 fullPropertyDetails 中缺少某些字段（如 inspection_times），
        // 已有的数据也不会被覆盖。
        const finalProperty = {
          ...existingProperty,
          ...this.currentProperty,
          ...fullPropertyDetails,
        }

        this.currentProperty = finalProperty
      } catch (error) {
        this.error = error.message || '获取房源详情失败'
        console.error('❌ 房源详情加载失败:', error)
      } finally {
        this.loading = false
      }
    },

    // 搜索房源
    async searchProperties(query, filters = {}) {
      this.loading = true
      this.error = null
      this.searchQuery = query

      try {
        const properties = await propertyAPI.search(query, filters)
        this.filteredProperties = properties
        this.totalCount = properties.length
        this.currentPage = 1 // 重置到第一页
      } catch (error) {
        this.error = error.message || '搜索房源失败'
        console.error('❌ 房源搜索失败:', error)
      } finally {
        this.loading = false
      }
    },

    // 应用筛选条件
    async applyFilters(filters) {
      this.loading = true
      this.error = null

      try {
        // Store 守卫：未选择区域时直接短路返回，避免无意义请求
        if (this.featureFlags?.requireRegionBeforeFilter && !hasRegionSelected(this.selectedLocations)) {
          // 清空当前结果，维持一致 UI 行为（按钮已禁用，此处为双保险）
          this.filteredProperties = []
          this.totalCount = 0
          this.totalPages = 0
          this.hasNext = false
          this.hasPrev = false
          this.currentPage = 1
          return
        }
        // 统一通过映射层构造请求参数
        // 目的：维持 V1 行为（默认），并可通过开关无缝切至 V2 契约（suburbs/price_min/...）
        // 中文注释：P0 稳定策略——仅当显式开启开关时才走 V2，禁用“按需切换”以防契约不一致
        const useV2 = enableFilterV2
        const mappedParams = mapFilterStateToApiParams(
          filters,
          this.selectedLocations,
          { page: 1, page_size: this.pageSize, sort: this.sort },
          { enableFilterV2: useV2 },
        )

        // 移除 null/空串，避免无效参数污染缓存与后端白名单
        Object.keys(mappedParams).forEach((key) => {
          if (
            mappedParams[key] === null ||
            mappedParams[key] === undefined ||
            mappedParams[key] === ''
          ) {
            delete mappedParams[key]
          }
        })

        // 记录“当前已应用的筛选条件”，供翻页/改每页大小复用
        this.currentFilterParams = { ...mappedParams }

        // 中文注释：调试输出本次请求参数（仅用于开发定位，生产可注释）
        {
          let __dbg = ''
          try { __dbg = JSON.stringify(mappedParams) } catch (err) { void err; __dbg = '[unserializable]' }
          // eslint-disable-next-line no-console
          console.debug('[FILTER-DEBUG][applyFilters] mappedParams:', __dbg)
        }
        const t0 = typeof performance !== 'undefined' && performance.now ? performance.now() : Date.now()
        const response = await propertyAPI.getListWithPagination(mappedParams)
        const t1 = typeof performance !== 'undefined' && performance.now ? performance.now() : Date.now()
        const dur = t1 - t0
        if (dur > 800) {
          console.warn(`[FILTER-PERF] applyFilters p95 threshold exceeded: ${Math.round(dur)} ms`, mappedParams)
        }

        // 更新数据
        this.filteredProperties = response.data || []

        // 更新分页信息
        if (response.pagination) {
          this.totalCount = response.pagination.total
          this.totalPages = response.pagination.pages
          this.hasNext = response.pagination.has_next
          this.hasPrev = response.pagination.has_prev
        }

        this.currentPage = 1 // 重置到第一页
      } catch (error) {
        console.error('❌ 筛选失败:', error)
        this.error = error.message || '筛选失败'
        // 快速失败：禁止本地降级，避免递归回退导致卡死
      } finally {
        this.loading = false
      }
    },

    // 本地筛选备用方案
    async applyLocalFilters() {
      // 已弃用：为避免递归回退与数据不一致，此方法不再执行任何操作
      return
    },

    // 设置搜索查询
    setSearchQuery(query) {
      this.searchQuery = query
    },

    // 设置选中的区域
    setSelectedLocations(locations) {
      this.selectedLocations = locations
    },

    // 添加选中区域
    addSelectedLocation(location) {
      const existingIndex = this.selectedLocations.findIndex((loc) => loc.id === location.id)
      if (existingIndex === -1) {
        this.selectedLocations.push(location)
      }
    },

    // 移除选中区域
    removeSelectedLocation(locationId) {
      this.selectedLocations = this.selectedLocations.filter((loc) => loc.id !== locationId)
    },

    // 添加收藏
    addFavorite(propertyId) {
      const id = String(propertyId)
      if (!this.favoriteIds.includes(id)) {
        this.favoriteIds.push(id)
        localStorage.setItem('juwo-favorites', JSON.stringify(this.favoriteIds))
      }
    },

    // 移除收藏
    removeFavorite(propertyId) {
      const id = String(propertyId)
      const index = this.favoriteIds.indexOf(id)
      if (index > -1) {
        this.favoriteIds.splice(index, 1)
        localStorage.setItem('juwo-favorites', JSON.stringify(this.favoriteIds))
      }
    },

    // 切换收藏状态
    toggleFavorite(propertyId) {
      const id = String(propertyId)
      const index = this.favoriteIds.indexOf(id)

      if (index > -1) {
        this.favoriteIds.splice(index, 1)
        // 从收藏数据中移除
        this.favoritePropertiesData = this.favoritePropertiesData.filter(
          (p) => String(p.listing_id) !== id,
        )
      } else {
        this.favoriteIds.push(id)
        // 如果当前有该房源数据，添加到收藏数据中
        const property =
          this.filteredProperties.find((p) => String(p.listing_id) === id) ||
          this.allProperties.find((p) => String(p.listing_id) === id)
        if (property && !this.favoritePropertiesData.find((p) => String(p.listing_id) === id)) {
          this.favoritePropertiesData.push(property)
        }
      }

      // 保存到localStorage
      localStorage.setItem('juwo-favorites', JSON.stringify(this.favoriteIds))
    },

    // 获取收藏的房源数据
    async fetchFavoriteProperties() {
      if (this.favoriteIds.length === 0) {
        this.favoritePropertiesData = []
        return
      }

      try {
        // 批量获取收藏的房源
        const promises = this.favoriteIds.map((id) =>
          propertyAPI.getDetail(id).catch((err) => {
            console.warn(`获取收藏房源 ${id} 失败:`, err)
            return null
          }),
        )

        const results = await Promise.all(promises)
        this.favoritePropertiesData = results.filter((p) => p !== null)
      } catch (error) {
        console.error('获取收藏房源失败:', error)
      }
    },

    // 获取筛选后的结果数量
    async getFilteredCount(params = {}) {
      try {
        // Store 守卫：未选择区域时计数恒为 0（不触发网络请求）
        if (this.featureFlags?.requireRegionBeforeFilter && !hasRegionSelected(this.selectedLocations)) {
          return 0
        }
        // 计数亦走统一映射，确保与列表参数一致
        // 中文注释：P0 稳定策略——仅当显式开启开关时才走 V2，禁用“按需切换”以防契约不一致
        const useV2 = enableFilterV2
        const mappedParams = mapFilterStateToApiParams(
          params,
          this.selectedLocations,
          { page: 1, page_size: 1 }, // 仅取总数
          { enableFilterV2: useV2 },
        )

        // 中文注释：调试输出计数请求参数（仅用于开发定位，生产可注释）
        {
          let __dbg = ''
          try { __dbg = JSON.stringify(mappedParams) } catch (err) { void err; __dbg = '[unserializable]' }
          // eslint-disable-next-line no-console
          console.debug('[FILTER-DEBUG][getFilteredCount] mappedParams:', __dbg)
        }
        const t0 = typeof performance !== 'undefined' && performance.now ? performance.now() : Date.now()
        const response = await propertyAPI.getListWithPagination(mappedParams)
        const t1 = typeof performance !== 'undefined' && performance.now ? performance.now() : Date.now()
        const dur = t1 - t0
        if (dur > 800) {
          console.warn(`[FILTER-PERF] getFilteredCount p95 threshold exceeded: ${Math.round(dur)} ms`, mappedParams)
        }
        return response.pagination?.total || 0
      } catch (error) {
        console.error('获取筛选数量失败:', error)
        return 0
      }
    },

    // 统一预览计数：合并“已应用条件 + 全局草稿 + 额外草稿”，并调用后端计数
    async getPreviewCount(extraDraft = {}) {
      try {
        // 中文注释：统一口径——以 Store 为单一真源聚合草稿，避免各面板“各算各的”
        const base = this.currentFilterParams || {}
        const mergedPreview = Object.values(this.previewDraftSections || {}).reduce((acc, obj) => {
          if (obj && typeof obj === 'object') return { ...acc, ...obj }
          return acc
        }, {})
        const merged = { ...base, ...mergedPreview, ...extraDraft }
        return await this.getFilteredCount(merged)
      } catch (e) {
        console.warn('getPreviewCount 失败', e)
        return 0
      }
    },

    // 更新/合并某个分组的“草稿”参数；值为 undefined/null/'' 代表删除该键
    updatePreviewDraft(section, partialDraft = {}) {
      // 中文注释：按 section 维度存储草稿，便于面板关闭时仅清理自己的增量
      if (!section) return
      const cleaned = { ...partialDraft }
      Object.keys(cleaned).forEach((k) => {
        if (cleaned[k] === undefined || cleaned[k] === null || cleaned[k] === '') {
          delete cleaned[k]
        }
      })
      const prev = this.previewDraftSections?.[section] || {}
      this.previewDraftSections = {
        ...this.previewDraftSections,
        [section]: { ...prev, ...cleaned },
      }
    },

    // 清理某个分组的草稿（面板关闭或“清除”时调用）
    clearPreviewDraft(section) {
      if (!section) return
      if (this.previewDraftSections && this.previewDraftSections[section]) {
        const next = { ...this.previewDraftSections }
        delete next[section]
        this.previewDraftSections = next
      }
    },

    // 设置当前页并重新获取数据
    async setCurrentPage(page) {
      if (page < 1 || page > this.totalPages) return

      this.currentPage = page
      // 重新获取当前页数据，显式传递页码与每页大小（防止遗留参数覆盖）
      await this.fetchProperties({ page: this.currentPage, page_size: this.pageSize })
    },

    // 下一页
    async nextPage() {
      if (this.hasNext) {
        await this.setCurrentPage(this.currentPage + 1)
      }
    },

    // 上一页
    async prevPage() {
      if (this.hasPrev) {
        await this.setCurrentPage(this.currentPage - 1)
      }
    },

    // 设置每页大小
    async setPageSize(size) {
      this.pageSize = size
      this.currentPage = 1 // 重置到第一页
      // 保留当前筛选条件，带上新的分页大小
      await this.fetchProperties({ page: 1, page_size: this.pageSize })
    },

    // 设置排序（仅透传到后端；后端未识别时保持UI一致且不做前端本地排序）
    async setSort(sort) {
      this.sort = sort || ''
      this.currentPage = 1
      // 将排序写入当前请求参数，遵守“单一数据源”：不在前端本地排序
      await this.fetchProperties({ page: 1, page_size: this.pageSize, sort: this.sort })
    },

    // 清空错误
    clearError() {
      this.error = null
    },

    // 重置筛选条件
    async resetFilters() {
      // 清空筛选条件并重新从API加载数据
      this.searchQuery = ''
      this.selectedLocations = []
      this.currentPage = 1
      this.currentFilterParams = {} // 清空已应用的筛选参数

      // 重新获取未筛选的数据
      await this.fetchProperties()
    },

    // 记录浏览历史
    logHistory(propertyId) {
      const id = String(propertyId)
      // 移除已存在的记录，再添加到最前面
      const history = this.viewHistory.filter((item) => item !== id)
      history.unshift(id)
      // 最多只保留50条
      this.viewHistory = history.slice(0, 50)
      localStorage.setItem('juwo-history', JSON.stringify(this.viewHistory))
    },

    // 隐藏房源（从搜索结果移除）
    hideProperty(propertyId) {
      const id = String(propertyId)
      // 添加到隐藏列表
      if (!this.hiddenIds) {
        this.hiddenIds = []
      }
      if (!this.hiddenIds.includes(id)) {
        this.hiddenIds.push(id)
        localStorage.setItem('juwo-hidden', JSON.stringify(this.hiddenIds))
      }

      // 从当前显示列表中移除
      this.filteredProperties = this.filteredProperties.filter(
        (property) => String(property.listing_id) !== id,
      )
      this.totalCount = Math.max(0, this.totalCount - 1)
    },

    // 切换对比状态
    toggleCompare(propertyId) {
      const id = String(propertyId)
      const index = this.compareIds.indexOf(id)

      if (index > -1) {
        this.compareIds.splice(index, 1)
      } else {
        // 最多只对比4个
        if (this.compareIds.length < 4) {
          this.compareIds.push(id)
        } else {
          // 在实际应用中，这里应该给用户一个提示
        }
      }
      localStorage.setItem('juwo-compare', JSON.stringify(this.compareIds))
    },
  },
})
