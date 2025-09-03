// JUWO桔屋找房 - 房源数据状态管理

import { defineStore } from 'pinia'
import { propertyAPI } from '@/services/api'

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

    // 收藏状态 (localStorage作为临时方案)
    favoriteIds: JSON.parse(localStorage.getItem('juwo-favorites') || '[]'),
    favoritePropertiesData: [],

    // 历史记录
    viewHistory: JSON.parse(localStorage.getItem('juwo-history') || '[]'),

    // 对比状态
    compareIds: JSON.parse(localStorage.getItem('juwo-compare') || '[]')
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
      return state.allProperties.filter(property =>
        state.favoriteIds.includes(String(property.listing_id))
      )
    },

    // 获取区域建议数据
    locationSuggestions: (state) => {
      const locationMap = new Map()

      state.allProperties.forEach(property => {
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
              count: 0
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
              count: 0
            })
          }
          locationMap.get(key).count++
        }
      })

      return Array.from(locationMap.values()).sort((a, b) => b.count - a.count)
    }
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
          ...params
        }

        const response = await propertyAPI.getListWithPagination(paginationParams)

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

    // 获取房源详情 - 优化版
    async fetchPropertyDetail(id) {
      // 统一转换为字符串进行比较（解决类型不匹配问题）
      const idStr = String(id)

      // 设置加载状态
      this.loading = true
      this.error = null

      try {
        // 尝试从当前列表、所有属性或当前已加载的房源中获取基础数据
        let existingProperty = this.filteredProperties.find(p => String(p.listing_id) === idStr) ||
                                this.allProperties.find(p => String(p.listing_id) === idStr) ||
                                (this.currentProperty && String(this.currentProperty.listing_id) === idStr ? this.currentProperty : null);

        // 如果在前端状态中找不到，则直接从列表API获取基础数据
        if (!existingProperty) {
          const listResponse = await propertyAPI.getListWithPagination({ listing_id: idStr });
          if (listResponse.data && listResponse.data.length > 0) {
            existingProperty = listResponse.data[0];
          }
        }

        // 如果有基础数据，先显示，避免白屏
        if (existingProperty) {
          this.currentProperty = existingProperty;
        }

        // 获取更详细的房源信息（例如，描述）
        const fullPropertyDetails = await propertyAPI.getDetail(id);

        // 智能合并数据：以现有数据为基础，用详情数据进行补充
        // 这样可以确保即使 fullPropertyDetails 中缺少某些字段（如 inspection_times），
        // 已有的数据也不会被覆盖。
        const finalProperty = {
          ...existingProperty,
          ...this.currentProperty,
          ...fullPropertyDetails
        };

        this.currentProperty = finalProperty;

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
        // 直接使用API进行服务端筛选
        const filterParams = {
          page: 1,
          page_size: 20,
          ...filters
        }

        // 移除null和空值
        Object.keys(filterParams).forEach(key => {
          if (filterParams[key] === null || filterParams[key] === undefined || filterParams[key] === '') {
            delete filterParams[key]
          }
        })

        const response = await propertyAPI.getListWithPagination(filterParams)

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
        console.error('❌ 筛选失败 - 退回到本地筛选:', error)
        this.error = error.message || '筛选失败'
        // 备用方案：使用本地筛选
        await this.applyLocalFilters(filters)
      } finally {
        this.loading = false
      }
    },

    // 本地筛选备用方案
    async applyLocalFilters(filters) {
      // 不再使用本地数据，直接调用API筛选
      // 这样可以确保数据始终是最新的，并且遵守is_active过滤
      return this.applyFilters(filters)
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
      const existingIndex = this.selectedLocations.findIndex(loc => loc.id === location.id)
      if (existingIndex === -1) {
        this.selectedLocations.push(location)
      }
    },

    // 移除选中区域
    removeSelectedLocation(locationId) {
      this.selectedLocations = this.selectedLocations.filter(loc => loc.id !== locationId)
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
          p => String(p.listing_id) !== id
        )
      } else {
        this.favoriteIds.push(id)
        // 如果当前有该房源数据，添加到收藏数据中
        const property = this.filteredProperties.find(p => String(p.listing_id) === id) ||
                        this.allProperties.find(p => String(p.listing_id) === id)
        if (property && !this.favoritePropertiesData.find(p => String(p.listing_id) === id)) {
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
        const promises = this.favoriteIds.map(id =>
          propertyAPI.getDetail(id).catch(err => {
            console.warn(`获取收藏房源 ${id} 失败:`, err)
            return null
          })
        )

        const results = await Promise.all(promises)
        this.favoritePropertiesData = results.filter(p => p !== null)
      } catch (error) {
        console.error('获取收藏房源失败:', error)
      }
    },

    // 获取筛选后的结果数量
    async getFilteredCount(params = {}) {
      try {
        const response = await propertyAPI.getListWithPagination({
          ...params,
          page_size: 1,  // 只需要获取总数
          page: 1
        })
        return response.pagination?.total || 0
      } catch (error) {
        console.error('获取筛选数量失败:', error)
        return 0
      }
    },

    // 设置当前页并重新获取数据
    async setCurrentPage(page) {
      if (page < 1 || page > this.totalPages) return

      this.currentPage = page
      // 重新获取当前页数据，传递页码参数
      await this.fetchProperties({ page: this.currentPage })
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
      await this.fetchProperties()
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

      // 重新获取未筛选的数据
      await this.fetchProperties()
    },

    // 记录浏览历史
    logHistory(propertyId) {
      const id = String(propertyId)
      // 移除已存在的记录，再添加到最前面
      const history = this.viewHistory.filter(item => item !== id)
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
        property => String(property.listing_id) !== id
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
    }
  }
})
