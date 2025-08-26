# Backend API 端点文档

> **最后更新**: 2025-01-24
> **框架**: FastAPI + Strawberry GraphQL
> **基础URL**: http://localhost:8000

---

## 目录

1. [系统端点](#系统端点)
2. [房源API](#房源api)
3. [通勤API](#通勤api)
4. [AI聊天API](#ai聊天api)
5. [任务API](#任务api)
6. [GraphQL端点](#graphql端点)
7. [数据库操作函数](#数据库操作函数)

---

## 系统端点

### GET /
**描述**: 根端点，返回API信息
```python
Response: {
    "message": "JUWO Property Search API",
    "version": "1.0.0",
    "endpoints": {...}
}
```

### GET /api/health
**描述**: 健康检查端点
```python
Response: {
    "status": "healthy",
    "timestamp": "2025-01-24T10:00:00Z",
    "database": "connected",
    "redis": "connected"
}
```

### GET /test_db_connection
**描述**: 测试数据库连接
```python
Response: {
    "status": "success",
    "message": "Database connection successful",
    "property_count": 2045
}
```

---

## 房源API

### GET /api/properties
**描述**: 获取房源列表（支持筛选和分页）

**查询参数**:
```python
page: int = 1                    # 页码
page_size: int = 20              # 每页数量
suburb: str = None               # 区域筛选
property_type: str = None        # 房源类型
bedrooms: int = None             # 卧室数
bathrooms: int = None            # 浴室数
min_price: int = None            # 最低价格
max_price: int = None            # 最高价格
parking_spaces: int = None       # 车位数
available_from: date = None      # 可入住开始日期
available_to: date = None        # 可入住结束日期

# 布尔特性筛选（22个）
has_air_conditioning: bool = None
is_furnished: bool = None
has_balcony: bool = None
has_dishwasher: bool = None
has_laundry: bool = None
has_built_in_wardrobe: bool = None
has_gym: bool = None
has_pool: bool = None
has_parking: bool = None
allows_pets: bool = None
has_security_system: bool = None
has_storage: bool = None
has_study_room: bool = None
has_garden: bool = None
# ... 等等
```

**响应格式**:
```json
{
  "status": "success",
  "data": [
    {
      "listing_id": 123456,
      "address": "123 George St, Sydney NSW 2000",
      "suburb": "Sydney",
      "state": "NSW",
      "postcode": "2000",
      "property_type": "Apartment",
      "rent_pw": 800,
      "bond": 3200,
      "bedrooms": 2,
      "bathrooms": 1,
      "parking_spaces": 1,
      "available_date": "2025-02-01",
      "images": ["url1.jpg", "url2.jpg"],
      "latitude": -33.8688,
      "longitude": 151.2093,
      "property_features": {...},
      "has_air_conditioning": true,
      "is_furnished": false
      // ... 其他字段
    }
  ],
  "pagination": {
    "total": 2045,
    "page": 1,
    "page_size": 20,
    "pages": 103,
    "has_next": true,
    "has_prev": false
  }
}
```

**缓存**: 15分钟 (Redis)

### GET /api/properties/{property_id}
**描述**: 获取单个房源详情

**路径参数**:
```python
property_id: int  # 房源ID
```

**响应格式**:
```json
{
  "status": "success",
  "data": {
    "listing_id": 123456,
    "property_url": "https://domain.com.au/...",
    "address": "123 George St, Sydney NSW 2000",
    "property_headline": "Modern 2BR Apartment with City Views",
    "property_description": "Beautiful apartment in the heart of Sydney...",
    "inspection_times": "Sat 10:00-10:30am",
    "agency_name": "JUWO Real Estate",
    "agent_name": "John Smith",
    "agent_phone": "0400123456",
    "agent_email": "john@juwo.com",
    "agent_profile_url": "https://...",
    "agent_logo_url": "https://...",
    // ... 所有其他字段
  }
}
```

**错误响应**:
```json
{
  "status": "error",
  "error": {
    "code": "PROPERTY_NOT_FOUND",
    "message": "Property with ID 123456 not found",
    "details": null
  }
}
```

**缓存**: 15分钟 (Redis)

---

## 通勤API

### GET /api/directions
**描述**: 获取Google Maps通勤信息

**查询参数**:
```python
origin: str          # 起点（地址或坐标）
destination: str     # 终点（地址或坐标）
mode: str = "transit"  # 交通方式: driving, transit, walking, bicycling
```

**响应格式**:
```json
{
  "status": "success",
  "data": {
    "distance": {
      "text": "5.2 km",
      "value": 5200
    },
    "duration": {
      "text": "15 mins",
      "value": 900
    },
    "steps": [...],
    "polyline": "encoded_polyline_string"
  }
}
```

**限制**: 需要Google Maps API密钥

---

## AI聊天API

### POST /api/chat
**描述**: AI聊天助手

**请求体**:
```json
{
  "message": "I'm looking for a 2BR apartment near UNSW",
  "session_id": "uuid-string",
  "context": {
    "user_preferences": {...},
    "search_history": [...]
  }
}
```

**响应格式**:
```json
{
  "status": "success",
  "data": {
    "response": "I found several 2BR apartments near UNSW...",
    "suggestions": [
      {"listing_id": 123456, "reason": "Walking distance to UNSW"},
      {"listing_id": 789012, "reason": "Good public transport"}
    ],
    "session_id": "uuid-string"
  }
}
```

---

## 任务API

### POST /api/tasks/debug
**描述**: 创建调试任务

**请求体**:
```json
{
  "task_type": "test",
  "params": {...}
}
```

**响应格式**:
```json
{
  "task_id": "celery-task-uuid",
  "status": "pending"
}
```

### POST /api/tasks/db
**描述**: 创建数据库任务

**请求体**:
```json
{
  "operation": "update_properties",
  "params": {...}
}
```

### GET /api/tasks/{task_id}
**描述**: 获取任务状态

**响应格式**:
```json
{
  "task_id": "celery-task-uuid",
  "status": "success",  // pending, processing, success, failed
  "result": {...},
  "error": null
}
```

---

## GraphQL端点

### POST /graphql
**描述**: GraphQL查询接口

**请求示例**:
```graphql
query GetProperties {
  properties(
    filters: {
      suburb: "Sydney"
      minPrice: 500
      maxPrice: 1000
    }
    pagination: {
      page: 1
      pageSize: 10
    }
  ) {
    items {
      listingId
      address
      rentPw
      bedrooms
    }
    totalCount
  }
}
```

**查询能力**:
```graphql
# 可用查询
properties           # 房源列表
property(id: ID!)   # 单个房源
universityCommuteProfile  # 大学通勤档案
propertiesNearLocation   # 位置附近房源

# 可用变更
toggleFavorite(propertyId: ID!)
createInquiry(input: InquiryInput!)
```

---

## 数据库操作函数

### properties_crud.py

#### get_all_properties_from_db()
**参数**:
```python
conn: psycopg2.connection
page: int = 1
page_size: int = 20
filters: dict = {
    "suburb": str,
    "property_type": str,
    "bedrooms": int,
    "bathrooms": int,
    "parking_spaces": int,
    "min_price": int,
    "max_price": int,
    "available_from": date,
    "available_to": date,
    # ... 22个布尔特性
}
```

**返回**: `Tuple[List[Property], int]`  # (房源列表, 总数)

#### get_property_by_id_from_db()
**参数**:
```python
conn: psycopg2.connection
property_id: int
```

**返回**: `Optional[Property]`

#### get_properties_near_location_from_db()
**参数**:
```python
conn: psycopg2.connection
latitude: float
longitude: float
radius_km: float = 2.0
limit: int = 50
```

**返回**: `List[Property]`

---

## 中间件和安全

### CORS配置
```python
origins = [
    "http://localhost:5173",  # Vue开发服务器
    "http://localhost:5174",  # 备用端口
]
```

### 限流配置
```python
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per minute", "1000 per hour"]
)

# 特定端点限流
@limiter.limit("5 per minute")  # AI聊天
@limiter.limit("20 per minute")  # 房源列表
```

### 认证（当前未启用）
```python
# JWT配置预留
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

---

## 环境变量依赖

```bash
# 数据库
DATABASE_URL=postgresql://user:pass@localhost/db

# Redis
REDIS_URL=redis://localhost:6379

# Google Maps
GOOGLE_MAPS_API_KEY=your_api_key

# JWT（预留）
SECRET_KEY=your_secret_key

# Supabase（如使用）
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=your_anon_key
```

---

## 错误代码参考

| 错误代码 | 描述 | HTTP状态码 |
|---------|------|-----------|
| PROPERTY_NOT_FOUND | 房源不存在 | 404 |
| INVALID_PARAMS | 参数无效 | 400 |
| DATABASE_ERROR | 数据库错误 | 500 |
| RATE_LIMIT_EXCEEDED | 超过频率限制 | 429 |
| UNAUTHORIZED | 未授权 | 401 |
| INTERNAL_ERROR | 内部错误 | 500 |

---

## 性能优化

1. **Redis缓存**:
   - 房源列表: 15分钟
   - 房源详情: 15分钟
   - 热门搜索: 30分钟

2. **数据库索引**:
   - properties_geom_idx (空间索引)
   - properties_suburb_idx
   - properties_rent_pw_idx
   - properties_bedrooms_idx

3. **连接池**:
   - 数据库: 最大20连接
   - Redis: 连接池复用

---

## 测试端点

```bash
# 测试房源列表
curl http://localhost:8000/api/properties?page_size=5

# 测试房源详情
curl http://localhost:8000/api/properties/123456

# 测试健康检查
curl http://localhost:8000/api/health

# 测试GraphQL
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ properties { items { listingId } } }"}'
```