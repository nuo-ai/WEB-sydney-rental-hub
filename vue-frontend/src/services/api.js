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
    console.log('🔍 API请求:', config.method?.toUpperCase(), config.url, config.params)
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
    console.log('✅ API响应:', response.config.url, '数据量:', response.data?.data?.length || 0)
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

  // 获取房源详情
  async getDetail(id) {
    try {
      const response = await apiClient.get(`/properties/${id}`)
      
      if (response.data.error) {
        throw new Error(`API错误: ${response.data.error.message}`)
      }
      
      return response.data
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
  async addFavorite(propertyId) {
    // TODO: 实现后端收藏API
    console.log('添加收藏:', propertyId)
  },

  // 移除收藏
  async removeFavorite(propertyId) {
    // TODO: 实现后端收藏API
    console.log('移除收藏:', propertyId)
  }
}

// 导出默认API客户端
export default apiClient
