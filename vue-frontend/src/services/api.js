// JUWO桔屋找房 - API服务层

import axios from 'axios'

// API基础配置 - 使用代理路径解决CORS问题
const API_BASE_URL = '/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 增加超时时间到30秒
  headers: {
    'Content-Type': 'application/json'
  }
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
    timestamp: Date.now()
  })
  // 限制缓存大小
  if (cache.size > 50) {
    const firstKey = cache.keys().next().value
    cache.delete(firstKey)
  }
}

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
        page_size: 20, // 减小默认大小，提高响应速度
        ...params
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
        pagination: response.data.pagination || null
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
      
      const startTime = Date.now()
      
      const response = await apiClient.get(`/properties/${id}`)
      
      const loadTime = Date.now() - startTime
      
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
// 计算两点之间的直线距离（Haversine公式）
function calculateDistance(lat1, lon1, lat2, lon2) {
  const R = 6371; // 地球半径（公里）
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = 
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
}

// 根据距离和交通方式估算通勤时间
function estimateCommute(distance, mode) {
  // 悉尼市区的平均速度估算
  const speeds = {
    DRIVING: 30,    // 30 km/h（考虑交通拥堵）
    TRANSIT: 25,    // 25 km/h（包括等车和换乘）
    WALKING: 5      // 5 km/h
  };
  
  // 路线弯曲系数（实际路线通常比直线距离长）
  const routeFactors = {
    DRIVING: 1.4,
    TRANSIT: 1.3,
    WALKING: 1.2
  };
  
  const speed = speeds[mode] || speeds.DRIVING;
  const factor = routeFactors[mode] || routeFactors.DRIVING;
  const actualDistance = distance * factor;
  const hours = actualDistance / speed;
  const minutes = Math.round(hours * 60);
  
  // 格式化时间显示
  let duration;
  if (minutes < 60) {
    duration = `${minutes} min`;
  } else {
    const h = Math.floor(minutes / 60);
    const m = minutes % 60;
    duration = m > 0 ? `${h} hr ${m} min` : `${h} hr`;
  }
  
  // 格式化距离显示
  const distanceStr = actualDistance < 1 
    ? `${Math.round(actualDistance * 1000)} m` 
    : `${actualDistance.toFixed(1)} km`;
  
  return {
    duration,
    distance: distanceStr,
    estimatedMinutes: minutes
  };
}

// 解析地址中的坐标（如果是坐标格式）
function parseCoordinates(location) {
  // 检查是否是 "lat,lng" 格式
  const coordPattern = /^-?\d+\.\d+,-?\d+\.\d+$/;
  if (coordPattern.test(location)) {
    const [lat, lng] = location.split(',').map(Number);
    return { lat, lng };
  }
  return null;
}

export const transportAPI = {
  // 获取通勤路线（使用本地估算避免Google API费用）
  async getDirections(origin, destination, mode) {
    try {
      // 测试模式：使用本地估算
      const testMode = localStorage.getItem('auth-testMode') === 'true';
      
      if (testMode) {
        // 解析起点坐标
        const originCoords = parseCoordinates(origin);
        if (!originCoords) {
          throw new Error('Invalid origin coordinates');
        }
        
        // 目标地址坐标（需要从保存的地址数据中获取）
        // 从localStorage获取保存的地址
        const savedAddresses = JSON.parse(localStorage.getItem('juwo-addresses') || '[]');
        const destAddress = savedAddresses.find(addr => addr.address === destination);
        
        if (destAddress && destAddress.latitude && destAddress.longitude) {
          // 计算距离和估算时间
          const distance = calculateDistance(
            originCoords.lat, originCoords.lng,
            destAddress.latitude, destAddress.longitude
          );
          
          const result = estimateCommute(distance, mode);
          return result;
        } else {
          // 如果找不到坐标，返回默认估算
          const defaultEstimates = {
            DRIVING: { duration: '15-30 min', distance: '10-20 km' },
            TRANSIT: { duration: '25-45 min', distance: '10-20 km' },
            WALKING: { duration: '2-3 hr', distance: '10-20 km' }
          };
          return defaultEstimates[mode] || defaultEstimates.DRIVING;
        }
      }
      
      // 生产模式：调用后端API
      const response = await apiClient.get('/directions', {
        params: { origin, destination, mode }
      });
      
      if (response.data.error) {
        throw new Error(`API错误: ${response.data.error.message}`);
      }
      
      return response.data.data;
    } catch (error) {
      console.error(`获取通勤路线失败 (模式: ${mode}):`, error);
      // 返回默认估算作为降级方案
      const fallbackEstimates = {
        DRIVING: { duration: '20-40 min', distance: '15-25 km' },
        TRANSIT: { duration: '30-50 min', distance: '15-25 km' },
        WALKING: { duration: '3-4 hr', distance: '15-25 km' }
      };
      return fallbackEstimates[mode] || fallbackEstimates.DRIVING;
    }
  }
};

// 导出默认API客户端
export default apiClient
