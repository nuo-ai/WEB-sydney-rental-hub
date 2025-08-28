import { defineStore } from 'pinia'
import { transportAPI } from '@/services/api'

export const useCommuteStore = defineStore('commute', {
  state: () => ({
    currentProperty: null,      // 当前查询的房源信息
    selectedMode: 'DRIVING',    // 当前选中的交通方式
    calculationCache: new Map(), // 缓存计算结果
    isCalculating: false,
    cacheExpiry: 15 * 60 * 1000, // 缓存15分钟
  }),

  getters: {
    hasProperty: (state) => !!state.currentProperty,
  },

  actions: {
    setCurrentProperty(property) {
      this.currentProperty = property
      // 清空缓存当切换房源时
      this.calculationCache.clear()
    },

    setTransportMode(mode) {
      this.selectedMode = mode
    },

    getFromCache(key) {
      const cached = this.calculationCache.get(key)
      if (cached) {
        // 检查缓存是否过期
        if (Date.now() - cached.timestamp < this.cacheExpiry) {
          return cached.data
        } else {
          // 缓存过期，删除
          this.calculationCache.delete(key)
        }
      }
      return null
    },

    setCache(key, data) {
      this.calculationCache.set(key, {
        data,
        timestamp: Date.now()
      })
    },

    clearCache() {
      this.calculationCache.clear()
    },

    async calculateCommute(destination, mode = null) {
      if (!this.currentProperty || !destination) {
        throw new Error('Missing property or destination')
      }

      const selectedMode = mode || this.selectedMode
      const cacheKey = `${this.currentProperty.coordinates.lat},${this.currentProperty.coordinates.lng}-${destination.id}-${selectedMode}`
      
      // 检查缓存
      const cached = this.getFromCache(cacheKey)
      if (cached) {
        return cached
      }
      
      this.isCalculating = true
      
      try {
        // 调用API
        const origin = `${this.currentProperty.coordinates.lat},${this.currentProperty.coordinates.lng}`
        const result = await transportAPI.getDirections(
          origin,
          destination.address,
          selectedMode
        )
        
        if (result.error) {
          throw new Error(result.error)
        }
        
        const commuteData = {
          duration: result.duration,
          distance: result.distance,
          mode: selectedMode
        }
        
        // 缓存结果
        this.setCache(cacheKey, commuteData)
        
        return commuteData
      } catch (error) {
        console.error('Failed to calculate commute:', error)
        throw error
      } finally {
        this.isCalculating = false
      }
    },

    async calculateMultiple(destinations, mode = null) {
      const selectedMode = mode || this.selectedMode
      const results = []
      
      for (const destination of destinations) {
        try {
          const result = await this.calculateCommute(destination, selectedMode)
          results.push({
            destinationId: destination.id,
            ...result
          })
        } catch (error) {
          results.push({
            destinationId: destination.id,
            error: true,
            duration: 'N/A',
            distance: ''
          })
        }
      }
      
      return results
    }
  },
})