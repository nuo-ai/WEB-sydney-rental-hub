# Vue Frontend API 参考文档

> **最后更新**: 2025-01-24
> **用途**: 前端开发者快速查阅API调用方法和响应格式

---

## API 客户端配置

**文件位置**: `src/services/api.js`

```javascript
// 基础配置
const apiClient = axios.create({
  baseURL: '/api',     // 通过Vite代理转发到 http://localhost:8000
  timeout: 10000,      // 10秒超时
  headers: {
    'Content-Type': 'application/json',
  }
})
```

---

## 房源相关 API (propertyAPI)

### 1. 获取房源列表
```javascript
// 调用方式
const properties = await propertyAPI.getList(params)

// 参数
params = {
  page: 1,           // 页码
  page_size: 20,     // 每页数量
  suburb: '',        // 区域筛选
  min_price: null,   // 最低价格
  max_price: null,   // 最高价格
  bedrooms: null,    // 卧室数
  property_type: ''  // 房源类型
}

// 响应格式
{
  data: [
    {
      listing_id: 123456,
      address: "123 George St",
      suburb: "Sydney",
      rent_pw: 800,
      bedrooms: 2,
      bathrooms: 1,
      parking_spaces: 1,
      available_date: "2025-02-01",
      images: ["url1", "url2"],
      latitude: -33.8688,
      longitude: 151.2093
      // ... 其他字段
    }
  ],
  pagination: {
    total: 100,
    page: 1,
    page_size: 20,
    pages: 5
  }
}
```

### 2. 获取房源详情
```javascript
// 调用方式
const property = await propertyAPI.getDetail(id)

// 参数
id: String | Number  // 房源ID

// 响应格式
{
  data: {
    listing_id: 123456,
    address: "123 George St",
    suburb: "Sydney",
    property_description: "Beautiful apartment...",
    property_headline: "Modern 2BR Apartment",
    // ... 完整的房源信息
  }
}
```

### 3. 搜索房源
```javascript
// 调用方式
const results = await propertyAPI.search(query, filters)

// 参数
query: String       // 搜索关键词
filters: {          // 筛选条件
  minPrice: Number,
  maxPrice: Number,
  bedrooms: String,
  bathrooms: String,
  parking: String,
  isFurnished: Boolean,
  date_from: Date,
  date_to: Date
}

// 响应格式
[
  // 房源数组，格式同getList
]
```

---

## 用户相关 API (userAPI)

### 1. 获取收藏列表
```javascript
// 调用方式
const favorites = await userAPI.getFavorites()

// 响应格式
{
  data: [
    // 房源ID数组
    "123456", "789012"
  ]
}
```

### 2. 添加收藏
```javascript
// 调用方式
await userAPI.addFavorite(propertyId)

// 参数
propertyId: String | Number

// 响应格式
{
  success: true,
  message: "Added to favorites"
}
```

### 3. 移除收藏
```javascript
// 调用方式
await userAPI.removeFavorite(propertyId)

// 参数
propertyId: String | Number

// 响应格式
{
  success: true,
  message: "Removed from favorites"
}
```

### 4. 联系我们
```javascript
// 调用方式
await userAPI.contactUs(payload)

// 参数
payload = {
  name: String,
  email: String,
  phone: String,
  message: String,
  propertyId: String
}

// 响应格式
{
  success: true,
  message: "Message sent successfully"
}
```

---

## 交通相关 API (transportAPI)

### 获取通勤路线
```javascript
// 调用方式
const directions = await transportAPI.getDirections(origin, destination, mode)

// 参数
origin: String       // 起点地址或坐标
destination: String  // 终点地址或坐标
mode: String        // 交通方式: 'driving', 'transit', 'walking', 'bicycling'

// 响应格式
{
  distance: {
    text: "5.2 km",
    value: 5200      // 米
  },
  duration: {
    text: "15 mins",
    value: 900       // 秒
  },
  routes: [
    // Google Maps路线数据
  ]
}
```

---

## Pinia Store 数据管理

**文件位置**: `src/stores/properties.js`

### State 结构
```javascript
{
  // 房源数据
  allProperties: [],        // 所有房源
  filteredProperties: [],   // 筛选后的房源
  currentProperty: null,    // 当前查看的房源
  
  // 加载状态
  loading: false,
  error: null,
  
  // 分页
  currentPage: 1,
  pageSize: 20,
  totalCount: 0,
  
  // 搜索和筛选
  searchQuery: '',
  selectedLocations: [],
  
  // 用户数据（localStorage存储）
  favoriteIds: [],         // 收藏的房源ID
  viewHistory: [],         // 浏览历史
  compareIds: []           // 对比列表
}
```

### 主要 Actions
```javascript
// 获取房源列表
await store.fetchProperties(params)

// 应用筛选
store.applyFilters(filters)

// 切换收藏
store.toggleFavorite(propertyId)

// 添加对比
store.toggleCompare(propertyId)

// 记录浏览历史
store.logHistory(propertyId)

// 重置筛选
store.resetFilters()
```

---

## 错误处理

### 通用错误格式
```javascript
// API错误响应
{
  error: {
    code: "PROPERTY_NOT_FOUND",
    message: "Property not found",
    details: {}
  }
}

// 前端错误处理示例
try {
  const property = await propertyAPI.getDetail(id)
  // 处理成功响应
} catch (error) {
  if (error.response) {
    // 服务器返回错误状态
    console.error('API Error:', error.response.data)
    this.error = error.response.data.message || '请求失败'
  } else if (error.request) {
    // 请求发送但无响应
    this.error = '网络连接失败'
  } else {
    // 其他错误
    this.error = '发生未知错误'
  }
}
```

---

## 注意事项

### 1. API响应格式不一致
- `getList` 和 `getDetail` 返回嵌套的 `{data: ...}` 结构
- `search` 直接返回数组
- **解决方案**: 在api.js中统一处理响应格式

### 2. 缓存问题
- 后端对列表和详情API有15分钟缓存
- 数据更新后可能显示旧数据
- **解决方案**: 关键操作后手动刷新数据

### 3. 分页参数
- 后端支持但前端当前实现是客户端分页
- 大数据量时可能有性能问题
- **建议**: 迁移到服务端分页

### 4. 认证状态
- 当前使用localStorage模拟用户状态
- 实际部署需要完整的认证系统
- **TODO**: 集成JWT认证

---

## 开发提示

1. **调试API调用**:
```javascript
// 在浏览器控制台查看网络请求
// Network标签 -> Filter: XHR
```

2. **模拟API延迟**:
```javascript
// 在api.js中添加延迟
await new Promise(resolve => setTimeout(resolve, 1000))
```

3. **查看Store状态**:
```javascript
// Vue DevTools -> Pinia标签
// 或在控制台：
const store = usePropertiesStore()
console.log(store.$state)
```