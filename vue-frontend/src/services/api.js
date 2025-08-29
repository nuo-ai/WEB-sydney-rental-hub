// JUWO桔屋找房 - API服务层

import axios from 'axios'

// API基础配置 - 使用代理路径解决CORS问题
const API_BASE_URL = '/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    console.error('❌ 请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    console.error('❌ API错误:', error.response?.status, error.message)
    return Promise.reject(error)
  }
)

// 房源API服务
export const propertyAPI = {
  // 获取房源列表
  async getList(params = {}) {
    try {
      // 确保page_size不超过后端限制
      const finalParams = {
        page_size: 100,
        ...params
      }
      
      const response = await apiClient.get('/properties', { params: finalParams })
      
      if (response.data.error) {
        throw new Error(`API错误: ${response.data.error.message}`)
      }
      
      return response.data.data || []
    } catch (error) {
      console.error('获取房源列表失败:', error)
      throw error
    }
  },

  // 获取房源列表（带分页信息）
  async getListWithPagination(params = {}) {
    try {
      const response = await apiClient.get('/properties', { params })
      
      if (response.data.error) {
        throw new Error(`API错误: ${response.data.error.message}`)
      }
      
      return {
        data: response.data.data || [],
        pagination: response.data.pagination || null
      }
    } catch (error) {
      console.error('获取房源列表失败:', error)
      throw error
    }
  },

  // 获取房源详情
  async getDetail(id) {
    try {
      const response = await apiClient.get(`/properties/${id}`)
      
      if (response.data.error) {
        throw new Error(`API错误: ${response.data.error.message}`)
      }
      
      return response.data.data
    } catch (error) {
      console.error('获取房源详情失败:', error)
      throw error
    }
  },

  // 搜索房源
  async search(query, filters = {}) {
    try {
      const params = {
        page_size: 100,
        ...filters
      }
      
      // 如果有搜索关键词，添加到参数中
      if (query && query.trim()) {
        params.search = query.trim()
      }
      
      const response = await apiClient.get('/properties', { params })
      
      if (response.data.error) {
        throw new Error(`API错误: ${response.data.error.message}`)
      }
      
      return response.data.data || []
    } catch (error) {
      console.error('搜索房源失败:', error)
      throw error
    }
  }
}

// 用户API服务 (预留)
export const userAPI = {
  // 获取收藏列表
  async getFavorites() {
    // TODO: 实现后端收藏API
    return []
  },

  // 添加收藏
  async addFavorite() {
    // TODO: 实现后端收藏API
  },

  // 移除收藏
  async removeFavorite() {
    // TODO: 实现后端收藏API
  },

  // 联系我们
  async contactUs(payload) {
    // TODO: 实现后端联系API
    console.log('发送联系请求:', payload)
    // 模拟成功响应
    return { success: true, message: '您的请求已发送' }
  }
}

// 位置/区域API服务
export const locationAPI = {
  // 获取所有区域（初始化搜索建议）
  async getAllLocations() {
    try {
      const response = await apiClient.get('/locations/all')
      if (response.data.status === 'success') {
        return response.data.data
      }
      throw new Error(response.data.error?.message || '获取区域数据失败')
    } catch (error) {
      console.error('❌ 获取区域数据失败:', error)
      return []
    }
  },

  // 搜索区域建议
  async getSuggestions(query, limit = 20) {
    try {
      const response = await apiClient.get('/locations/suggestions', {
        params: { q: query, limit }
      })
      if (response.data.status === 'success') {
        return response.data.data
      }
      throw new Error(response.data.error?.message || '搜索失败')
    } catch (error) {
      console.error('❌ 搜索区域失败:', error)
      return []
    }
  },

  // 获取相邻区域推荐
  async getNearbySuburbs(suburb, limit = 6) {
    try {
      const response = await apiClient.get('/locations/nearby', {
        params: { suburb, limit }
      })
      if (response.data.status === 'success') {
        return response.data.data
      }
      throw new Error(response.data.error?.message || '获取相邻区域失败')
    } catch (error) {
      console.error('❌ 获取相邻区域失败:', error)
      return { current: suburb, nearby: [] }
    }
  }
}

// 交通API服务
export const transportAPI = {
  // 获取通勤路线
  async getDirections(origin, destination, mode) {
    try {
      // apiClient的baseURL是'/api'，所以请求会发到'/api/directions'
      const response = await apiClient.get('/directions', {
        params: { origin, destination, mode }
      });
      
      if (response.data.error) {
        throw new Error(`API错误: ${response.data.error.message}`);
      }
      
      return response.data.data; // 修正: 直接返回data字段
    } catch (error) {
      console.error(`获取通勤路线失败 (模式: ${mode}):`, error);
      // 返回一个标准错误结构，方便前端处理
      return { 
          error: '无法计算通勤时间',
          duration: 'N/A', 
          distance: 'N/A' 
      };
    }
  }
};

// 导出默认API客户端
export default apiClient
