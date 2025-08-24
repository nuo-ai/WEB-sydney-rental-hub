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
    
    // 分页状态
    currentPage: 1,
    pageSize: 20,
    totalCount: 0,
    
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
    // 获取当前页的房源
    paginatedProperties: (state) => {
      const startIndex = (state.currentPage - 1) * state.pageSize
      const endIndex = startIndex + state.pageSize
      return state.filteredProperties.slice(startIndex, endIndex)
    },

    // 获取总页数
    totalPages: (state) => {
      return Math.ceil(state.filteredProperties.length / state.pageSize)
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
    // 获取房源列表
    async fetchProperties(params = {}) {
      this.loading = true
      this.error = null
      
      try {
        const properties = await propertyAPI.getList(params)
        this.allProperties = properties
        this.filteredProperties = properties
        this.totalCount = properties.length
        
      } catch (error) {
        this.error = error.message || '获取房源数据失败'
        console.error('❌ 房源数据加载失败:', error)
      } finally {
        this.loading = false
      }
    },

    // 获取房源详情
    async fetchPropertyDetail(id) {
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
    applyFilters(filters) {
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
      
      // 卧室筛选
      if (filters.bedrooms && filters.bedrooms !== 'any') {
        if (filters.bedrooms === 'studio/1') {
          filtered = filtered.filter(property => 
            property.bedrooms === 0 || property.bedrooms === 1
          )
        } else if (String(filters.bedrooms).includes('+')) {
          const minBeds = parseInt(filters.bedrooms)
          filtered = filtered.filter(property => 
            property.bedrooms && property.bedrooms >= minBeds
          )
        } else {
          filtered = filtered.filter(property => 
            property.bedrooms === parseInt(filters.bedrooms)
          )
        }
      }
      
      // 浴室筛选
      if (filters.bathrooms && filters.bathrooms !== 'any') {
        if (String(filters.bathrooms).includes('+')) {
          const minBaths = parseInt(filters.bathrooms)
          filtered = filtered.filter(property => 
            property.bathrooms && property.bathrooms >= minBaths
          )
        } else {
          filtered = filtered.filter(property => 
            property.bathrooms === parseInt(filters.bathrooms)
          )
        }
      }
      
      // 车位筛选
      if (filters.parking && filters.parking !== 'any') {
        if (String(filters.parking).includes('+')) {
          const minParking = parseInt(filters.parking)
          filtered = filtered.filter(property => 
            property.parking_spaces && property.parking_spaces >= minParking
          )
        } else {
          filtered = filtered.filter(property => 
            property.parking_spaces === parseInt(filters.parking)
          )
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
      
      this.filteredProperties = filtered
      this.totalCount = filtered.length
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

    // 设置当前页
    setCurrentPage(page) {
      this.currentPage = page
    },

    // 清空错误
    clearError() {
      this.error = null
    },

    // 重置筛选条件
    resetFilters() {
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
