// JUWO桔屋找房 - API服务层

import axios from 'axios'

/**
 * API基础配置
 * 说明（为什么这么做）：
 * - 本地开发：走 '/api'，由 Vite 代理转发到本机 FastAPI，避免 CORS
 * - 生产部署：从环境变量 VITE_API_BASE_URL 读取后端基址；为降低出错率，若未带 '/api' 则自动补上
 *  （这样 Netlify 只需设置后端根域名或完整 /api 前缀均可）
 */
const API_BASE_URL = (() => {
  const raw =
    import.meta.env && import.meta.env.VITE_API_BASE_URL
      ? String(import.meta.env.VITE_API_BASE_URL).trim()
      : ''
  if (raw) {
    let base = raw.replace(/\/+$/, '') // 去掉末尾多余斜杠，防止出现双斜杠
    if (!/\/api$/.test(base)) {
      base += '/api' // 若未包含 /api，自动补齐以匹配后端路由前缀
    }
    return base
  }
  // 回退：本地开发默认 '/api' 由 Vite 代理处理
  return '/api'
})()

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 增加超时时间到30秒
  headers: {
    'Content-Type': 'application/json',
  },
})

// 简单的内存缓存
const cache = new Map()
const CACHE_DURATION = 15 * 60 * 1000 // 15分钟缓存，与后端保持一致

const getCacheKey = (url, params) => {
  return `${url}:${JSON.stringify(params)}`
}

const getCachedData = (key) => {
  const cached = cache.get(key)
  if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
    return cached.data
  }
  return null
}

const setCachedData = (key, data) => {
  cache.set(key, {
    data,
    timestamp: Date.now(),
  })
  // 限制缓存大小
  if (cache.size > 50) {
    const firstKey = cache.keys().next().value
    cache.delete(firstKey)
  }
}

// 清除所有缓存（用于调试或强制刷新）
const clearAllCache = () => {
  cache.clear()
  // API缓存已清除（移除 console.log 调试输出）
}

// 暴露到window对象方便调试
if (typeof window !== 'undefined') {
  window.clearAPICache = clearAllCache
}

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    console.error('❌ 请求错误:', error)
    return Promise.reject(error)
  },
)

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    console.error('❌ API错误:', error.response?.status, error.message)
    return Promise.reject(error)
  },
)

// 房源API服务
export const propertyAPI = {
  // 获取房源列表
  async getList(params = {}) {
    try {
      // 确保page_size不超过后端限制
      const finalParams = {
        page_size: 20, // 减小默认大小，提高响应速度
        ...params,
      }

      // 检查缓存
      const cacheKey = getCacheKey('/properties', finalParams)
      const cachedData = getCachedData(cacheKey)
      if (cachedData) {
        return cachedData
      }

      const response = await apiClient.get('/properties', { params: finalParams })

      if (response.data.error) {
        throw new Error(`API错误: ${response.data.error.message}`)
      }

      const data = response.data.data || []
      // 缓存数据
      setCachedData(cacheKey, data)
      return data
    } catch (error) {
      console.error('获取房源列表失败:', error)
      throw error
    }
  },

  // 获取房源列表（带分页信息）
  async getListWithPagination(params = {}) {
    try {
      // 检查缓存
      const cacheKey = getCacheKey('/properties-paginated', params)
      const cachedData = getCachedData(cacheKey)
      if (cachedData) {
        return cachedData
      }

      const response = await apiClient.get('/properties', { params })

      if (response.data.error) {
        throw new Error(`API错误: ${response.data.error.message}`)
      }

      const result = {
        data: response.data.data || [],
        pagination: response.data.pagination || null,
      }

      // 缓存结果
      setCachedData(cacheKey, result)
      return result
    } catch (error) {
      console.error('获取房源列表失败:', error)
      throw error
    }
  },

  // 获取房源详情
  async getDetail(id) {
    try {
      // 检查缓存
      const cacheKey = getCacheKey(`/properties/${id}`, {})
      const cachedData = getCachedData(cacheKey)
      if (cachedData) {
        return cachedData
      }

      const response = await apiClient.get(`/properties/${id}`)

      if (response.data.error) {
        throw new Error(`API错误: ${response.data.error.message}`)
      }

      const data = response.data.data

      // 缓存详情数据
      setCachedData(cacheKey, data)

      return data
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
        ...filters,
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
  },
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
  async contactUs() {
    // TODO: 实现后端联系API
    // 模拟成功响应
    return { success: true, message: '您的请求已发送' }
  },
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

  // 搜索区域建议（默认上限提升至 100，覆盖“2*”邮编等全量场景）
  async getSuggestions(query, limit = 100) {
    try {
      const response = await apiClient.get('/locations/suggestions', {
        params: { q: query, limit },
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
        params: { suburb, limit },
      })
      if (response.data.status === 'success') {
        return response.data.data
      }
      throw new Error(response.data.error?.message || '获取相邻区域失败')
    } catch (error) {
      console.error('❌ 获取相邻区域失败:', error)
      return { current: suburb, nearby: [] }
    }
  },
}

// 交通API服务

export const transportAPI = {
  // 获取通勤路线（调用后端Google Maps API）
  async getDirections(origin, destination, mode) {
    const response = await apiClient.get('/directions', {
      params: { origin, destination, mode },
    })

    if (response.data.error) {
      throw new Error(`API错误: ${response.data.error.message}`)
    }

    return response.data.data
  },
}

// 导出API客户端和工具函数
export { clearAllCache }
export default apiClient
