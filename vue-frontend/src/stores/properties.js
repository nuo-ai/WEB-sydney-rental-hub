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
        
        console.log('📡 调用API获取房源数据...', paginationParams)
        const startTime = Date.now()
        
        const response = await propertyAPI.getListWithPagination(paginationParams)
        
        const loadTime = Date.now() - startTime
        console.log(`✅ 数据加载完成，耗时: ${loadTime}ms`)
        
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
        console.log(`📁 已缓存 ${baseData.length} 条基础数据用于搜索建议`)
      } catch (error) {
        console.warn('⚠️ 加载基础数据失败，搜索建议功能可能受影响:', error)
      }
    },

    // 获取房源详情 - 优化版
    async fetchPropertyDetail(id) {
      // 统一转换为字符串进行比较（解决类型不匹配问题）
      const idStr = String(id)
      
      // 先检查是否已有数据（从列表页或缓存）
      const existingProperty = this.filteredProperties.find(p => String(p.listing_id) === idStr) ||
                              this.allProperties.find(p => String(p.listing_id) === idStr) ||
                              (this.currentProperty && String(this.currentProperty.listing_id) === idStr ? this.currentProperty : null)
      
      if (existingProperty) {
        console.log('📦 使用已有的房源数据')
        this.currentProperty = existingProperty
        // 仍然异步获取完整详情（可能有更多信息）
        this.fetchFullDetailAsync(id)
        return
      }
      
      this.loading = true
      this.error = null
      
      try {
        const property = await propertyAPI.getDetail(id)
        this.currentProperty = property
        
      } catch (error) {
        this.error = error.message || '获取房源详情失败'
        console.error('❌ 房源详情加载失败:', error)
      } finally {
        this.loading = false
      }
    },
    
    // 异步获取完整详情
    async fetchFullDetailAsync(id) {
      try {
        const fullProperty = await propertyAPI.getDetail(id)
        // 如果当前房源ID没变，更新详情
        if (this.currentProperty && this.currentProperty.listing_id === id) {
          this.currentProperty = { ...this.currentProperty, ...fullProperty }
        }
      } catch (error) {
        console.warn('⚠️ 异步获取完整详情失败:', error)
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
      console.log('🔍 applyFilters 被调用, 参数:', filters)
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
        
        console.log('📡 发送API请求, 参数:', filterParams)
        const response = await propertyAPI.getListWithPagination(filterParams)
        console.log('✅ API响应:', response)
        
        // 更新数据
        this.filteredProperties = response.data || []
        
        // 更新分页信息
        if (response.pagination) {
          this.totalCount = response.pagination.total
          this.totalPages = response.pagination.pages
          this.hasNext = response.pagination.has_next
          this.hasPrev = response.pagination.has_prev
          console.log('📊 总数更新为:', this.totalCount)
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
      // 确保有数据可以筛选
      if (this.allProperties.length === 0) {
        // 如果没有数据，先加载数据
        this.loading = true
        try {
          // 分批加载，避免 422 错误
          const batches = await Promise.all([
            propertyAPI.getList({ page_size: 100, page: 1 }),
            propertyAPI.getList({ page_size: 100, page: 2 }),
            propertyAPI.getList({ page_size: 100, page: 3 })
          ])
          
          // 合并所有批次的数据
          this.allProperties = batches.flat()
        } catch (error) {
          console.error('❌ 加载筛选数据失败:', error)
          // 降级到更小的数据量
          try {
            const fallbackData = await propertyAPI.getList({ page_size: 50 })
            this.allProperties = fallbackData
          } catch (fallbackError) {
            this.error = '加载数据失败，请重试'
            return
          }
        } finally {
          this.loading = false
        }
      }
      
      // 更新store中的筛选状态，确保单一数据源
      if (filters.areas) {
        // 将字符串数组转换为符合预期的对象数组
        this.selectedLocations = filters.areas.map(area => ({
          id: area,
          type: 'suburb', // 假设快速筛选只处理suburb
          name: area
        }));
      }

      let filtered = [...this.allProperties]
      
      // 区域筛选 (使用更新后的state)
      if (this.selectedLocations.length > 0) {
        filtered = filtered.filter(property => {
          return this.selectedLocations.some(location => {
            if (location.type === 'suburb') {
              return property.suburb && 
                property.suburb.toLowerCase() === location.name.toLowerCase()
            } else if (location.type === 'postcode') {
              const propertyPostcode = property.postcode ? 
                Math.floor(property.postcode).toString() : ''
              return propertyPostcode === location.name
            }
            return false
          })
        })
      }
      
      // 文本搜索
      if (this.searchQuery) {
        const searchTerm = this.searchQuery.toLowerCase()
        filtered = filtered.filter(property =>
          (property.address || '').toLowerCase().includes(searchTerm) ||
          (property.suburb || '').toLowerCase().includes(searchTerm) ||
          (property.postcode || '').toString().includes(searchTerm)
        )
      }
      
      // 价格筛选
      if (filters.minPrice !== null && filters.minPrice !== undefined) {
        filtered = filtered.filter(property => 
          property.rent_pw && parseInt(property.rent_pw) >= filters.minPrice
        )
      }
      
      if (filters.maxPrice !== null && filters.maxPrice !== undefined) {
        filtered = filtered.filter(property => 
          property.rent_pw && parseInt(property.rent_pw) <= filters.maxPrice
        )
      }
      
      // 卧室筛选 - 处理多选
      if (filters.bedrooms && filters.bedrooms !== '') {
        const bedroomValues = typeof filters.bedrooms === 'string' 
          ? filters.bedrooms.split(',').filter(v => v && v !== '')
          : []
        
        // 检查是否选择了所有卧室选项（等同于不筛选）
        const allBedroomOptions = ['1', '2', '3', '4+']
        const isAllSelected = allBedroomOptions.every(opt => bedroomValues.includes(opt))
        
        if (bedroomValues.length > 0 && !isAllSelected) {
          filtered = filtered.filter(property => {
            const beds = property.bedrooms || 0
            
            return bedroomValues.some(value => {
              if (value === 'studio/1') {
                return beds === 0 || beds === 1
              } else if (value.includes('+')) {
                const minBeds = parseInt(value)
                return beds >= minBeds
              } else {
                return beds === parseInt(value)
              }
            })
          })
        }
      }
      
      // 浴室筛选 - 处理多选
      if (filters.bathrooms && filters.bathrooms !== '') {
        const bathroomValues = typeof filters.bathrooms === 'string'
          ? filters.bathrooms.split(',').filter(v => v && v !== '')
          : []
        
        // 检查是否选择了所有浴室选项（等同于不筛选）
        const allBathroomOptions = ['1', '2', '3+']
        const isAllSelected = allBathroomOptions.every(opt => bathroomValues.includes(opt))
        
        if (bathroomValues.length > 0 && !isAllSelected) {
          filtered = filtered.filter(property => {
            const baths = property.bathrooms || 0
            
            return bathroomValues.some(value => {
              if (value.includes('+')) {
                const minBaths = parseInt(value)
                return baths >= minBaths
              } else {
                return baths === parseInt(value)
              }
            })
          })
        }
      }
      
      // 车位筛选 - 处理多选
      if (filters.parking && filters.parking !== '') {
        const parkingValues = typeof filters.parking === 'string'
          ? filters.parking.split(',').filter(v => v && v !== '')
          : []
        
        // 检查是否选择了所有车位选项（等同于不筛选）
        const allParkingOptions = ['0', '1', '2+']
        const isAllSelected = allParkingOptions.every(opt => parkingValues.includes(opt))
        
        if (parkingValues.length > 0 && !isAllSelected) {
          filtered = filtered.filter(property => {
            const parking = property.parking_spaces || 0
            
            return parkingValues.some(value => {
              if (value.includes('+')) {
                const minParking = parseInt(value)
                return parking >= minParking
              } else {
                return parking === parseInt(value)
              }
            })
          })
        }
      }
      
      // 入住日期筛选
      if (filters.date_from) {
        const startDate = new Date(filters.date_from)
        startDate.setHours(0, 0, 0, 0) // 标准化到当天的开始
        filtered = filtered.filter(property => {
          if (!property.available_date) return true // 如果房源没有可用日期，暂时不筛选掉
          const propertyDate = new Date(property.available_date)
          return propertyDate >= startDate
        })
      }

      if (filters.date_to) {
        const endDate = new Date(filters.date_to)
        endDate.setHours(23, 59, 59, 999) // 标准化到当天的结束
        filtered = filtered.filter(property => {
          if (!property.available_date) return false // 如果没有可用日期，则不符合结束日期筛选
          const propertyDate = new Date(property.available_date)
          return propertyDate <= endDate
        })
      }
      
      // 家具筛选
      if (filters.isFurnished) {
        filtered = filtered.filter(property => property.is_furnished === true)
      }
      
      // 仅作为本地备用时使用
      this.filteredProperties = filtered.slice(0, 20) // 只显示前20条
      this.totalCount = filtered.length // 本地筛选的总数
      this.currentPage = 1 // 重置到第一页
      
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
      } else {
        this.favoriteIds.push(id)
      }
      
      // 保存到localStorage
      localStorage.setItem('juwo-favorites', JSON.stringify(this.favoriteIds))
      
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
      // 确保有数据
      if (this.allProperties.length === 0) {
        await this.fetchProperties()
      }
      
      this.filteredProperties = [...this.allProperties]
      this.searchQuery = ''
      this.selectedLocations = []
      this.currentPage = 1
      this.totalCount = this.allProperties.length
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
