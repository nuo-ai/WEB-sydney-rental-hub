# 🔄 Sydney Rental Hub 数据流向完整解析

> **创建时间**: 2025-01-24
> **更新时间**: 2025-01-24（修正Supabase连接）
> **用途**: 理解系统数据从采集到展示的完整流程

---

## 📊 数据流向总览

```
[Domain.com.au] → [爬虫] → [CSV/Excel] → [数据库导入] → [Supabase云数据库] 
                                                            ↓
[前端展示] ← [Vite代理] ← [FastAPI] ← [数据查询]
```

---

## 1️⃣ 数据采集阶段（爬虫）

### 爬虫系统位置
```
crawler/
├── v5_furniture.py              # 主爬虫脚本（v2版本）
├── enhanced_feature_extractor.py # 特征提取器
├── config/
│   ├── temp_urls.txt           # 临时URL（优先使用）
│   ├── url.txt                  # 默认URL列表
│   └── crawler_config.yaml     # 爬虫配置
└── output/
    ├── *_Combined_*.csv         # 合并后的CSV数据
    └── *_*.xlsx                 # 各区域Excel数据
```

### 数据采集流程
1. **读取配置**: 
   - 优先从`config/temp_urls.txt`读取
   - 如果不存在则从`config/url.txt`读取Domain.com.au链接
   
2. **爬取数据**: `v5_furniture.py`爬取房源信息
   - 支持分页爬取（?page=1,2,3...）
   - 支持断点续爬（progress.json）
   - 自动延迟防封（0.8-2.2秒/请求）
   
3. **特征提取**: `enhanced_feature_extractor.py`提取8个核心特性
   - is_furnished（家具）
   - has_air_conditioning（空调）
   - has_laundry（洗衣）
   - has_dishwasher（洗碗机）
   - has_gas_cooking（燃气灶）
   - has_intercom（对讲）
   - has_study（书房）
   - has_balcony（阳台）
   
4. **数据输出**: 
   - 各区域数据保存为Excel（如`Ultimo_53properties.xlsx`）
   - 合并数据保存为CSV（如`20250821_115542_Combined_2045properties.csv`）
   
5. **自动触发ETL**: 
   - 爬虫完成后自动调用`trigger_etl_job()`
   - 执行`scripts/automated_data_update_with_notifications.py`

### 爬取的数据字段
```python
# 基础信息
- listing_id        # 房源ID
- address          # 地址
- suburb           # 区域
- rent_pw          # 周租金
- bedrooms         # 卧室数
- bathrooms        # 浴室数
- parking_spaces   # 车位数
- available_date   # 可入住日期

# V4特性信息（8个核心特性，不是22个）
- is_furnished: "unknown/yes/no"
- has_air_conditioning: "unknown/yes/no"
- has_laundry: "unknown/yes/no"
- has_dishwasher: "unknown/yes/no"
- has_gas_cooking: "unknown/yes/no"
- has_intercom: "unknown/yes/no"
- has_study: "unknown/yes/no"
- has_balcony: "unknown/yes/no"

# 多媒体
- images           # 图片URL列表(JSON)
- property_features # 原始特色列表(JSON)
```

---

## 2️⃣ 数据入库阶段（Supabase）

### 🔑 关键发现：使用Supabase云数据库
```env
# .env配置
DATABASE_URL="postgresql://postgres.urhndweqvoiqrgqpzhgk:***@aws-0-ap-southeast-2.pooler.supabase.com:5432/postgres"
```

### 数据导入脚本
```
database/
├── process_csv.py       # CSV数据处理脚本
├── update_database.py   # 数据库更新脚本（增量更新）
└── setup_database.sql   # 数据库表结构
```

### 导入流程
1. **查找CSV文件**: 
   - `process_csv.py`查找`crawler/output/`目录下最新的CSV文件
   - 或`automated_data_update_with_notifications.py`自动触发

2. **连接Supabase**:
   ```python
   # db.py 中的连接逻辑
   database_url = os.getenv("DATABASE_URL")  # 优先使用Supabase URL
   if database_url:
       conn = psycopg2.connect(database_url)  # 连接到Supabase
   ```

3. **数据处理**:
   ```python
   # PropertyDataProcessor 类
   - 读取CSV文件
   - 清洗和转换数据格式
   - 处理日期、布尔值等字段
   - 生成地理位置数据（PostGIS格式）
   ```

4. **写入Supabase数据库**:
   ```sql
   -- 插入或更新properties表
   INSERT INTO properties (
       listing_id, address, suburb, rent_pw, ...
   ) VALUES (...) 
   ON CONFLICT (listing_id) DO UPDATE SET ...
   ```

### Supabase数据库结构
```sql
-- Supabase PostgreSQL + PostGIS
properties表:
├── listing_id (主键)
├── 基础信息字段
├── 8个特性字段（V4版本，不是22个）
├── geom (PostGIS空间数据)
├── images (JSONB)
├── property_features (JSONB)
└── 时间戳字段
```

---

## 3️⃣ API数据服务阶段

### 后端API流程
```
backend/
├── main.py                     # API端点定义
├── db.py                       # Supabase连接
├── crud/properties_crud.py     # 数据库查询
└── models/property_models.py   # 数据模型
```

### 数据查询流程

1. **API请求接收** (`main.py`):
   ```python
   @app.get("/api/properties")
   async def get_properties(
       page: int = 1,
       page_size: int = 20,
       suburb: str = None,
       # ... 其他筛选参数
   )
   ```

2. **Supabase连接** (`db.py`):
   ```python
   def get_db_connection():
       # 连接到Supabase云数据库
       database_url = os.getenv("DATABASE_URL")
       conn = psycopg2.connect(database_url)
       return conn
   ```

3. **数据库查询** (`properties_crud.py`):
   ```python
   def get_all_properties_from_db(conn, page, page_size, filters):
       # 从Supabase查询数据
       query = """
           SELECT * FROM properties 
           WHERE is_active = TRUE
           AND ({筛选条件})
           LIMIT %s OFFSET %s
       """
       # 执行查询并返回结果
   ```

4. **缓存处理**:
   - Redis缓存15分钟
   - 减少Supabase查询压力

---

## 4️⃣ 前端数据展示阶段

### 前端数据获取流程
```
apps/web/src/
├── services/api.js          # API调用
├── stores/properties.js     # 状态管理
└── views/HomeView.vue       # 页面展示
```

### 数据流转步骤

1. **API调用** (`api.js`):
   ```javascript
   // 通过Vite代理调用后端
   const response = await axios.get('/api/properties', {
       params: { page: 1, page_size: 20 }
   })
   ```

2. **状态管理** (`properties.js`):
   ```javascript
   // Pinia store
   async fetchProperties(params) {
       const properties = await propertyAPI.getList(params)
       this.allProperties = properties
       this.filteredProperties = properties
   }
   ```

3. **组件展示** (`PropertyCard.vue`):
   ```vue
   <template>
     <div class="property-card">
       <el-carousel>
         <el-carousel-item v-for="img in images">
           <img :src="img" />
         </el-carousel-item>
       </el-carousel>
       <div class="property-info">
         <div class="price">${{ property.rent_pw }}/周</div>
         <div class="address">{{ property.address }}</div>
       </div>
     </div>
   </template>
   ```

---

## 5️⃣ 完整数据流时序图（含Supabase）

```mermaid
sequenceDiagram
    participant D as Domain.com.au
    participant C as 爬虫(v5_furniture.py)
    participant CSV as CSV文件
    participant S as Supabase云数据库
    participant API as FastAPI
    participant R as Redis缓存
    participant V as Vue前端
    participant U as 用户

    Note over D,C: 1. 数据采集
    C->>D: 请求房源页面
    D-->>C: 返回HTML
    C->>C: 解析HTML提取数据
    C->>C: enhanced_feature_extractor提取特性
    C->>CSV: 保存为CSV/Excel

    Note over CSV,S: 2. 数据导入到Supabase
    C->>C: trigger_etl_job()
    CSV->>S: process_csv.py导入到Supabase
    S->>S: 更新云端properties表

    Note over S,V: 3. 数据服务
    U->>V: 访问网站
    V->>API: GET /api/properties
    API->>R: 检查Redis缓存
    alt 缓存命中
        R-->>API: 返回缓存数据
    else 缓存未命中
        API->>S: 查询Supabase properties表
        S-->>API: 返回查询结果
        API->>R: 存入缓存(15分钟)
    end
    API-->>V: 返回JSON数据
    V->>V: 更新Pinia Store
    V-->>U: 展示房源列表
```

---

## ⚠️ 数据流关键节点（Supabase版本）

### 1. 数据更新频率
- **爬虫运行**: 
  - 可配置定时运行（PIPELINE_SCHEDULE="0 */8 * * *"）
  - 或手动运行`crawler/v5_furniture.py`
- **Supabase更新**: 增量更新，保留历史数据
- **缓存时间**: Redis 15分钟

### 2. 数据一致性保证
- **Supabase级**: 使用事务，ON CONFLICT处理重复
- **API级**: 统一的响应格式包装
- **前端级**: Pinia单一数据源

### 3. 数据转换节点
- **CSV→Supabase**: 
  - 日期格式转换（过期日期→"Available Now"）
  - 特性值转换（"unknown"/"yes"/"no"）
- **Supabase→API**: Snake_case字段名
- **API→前端**: 嵌套data结构处理

### 4. 性能优化点
- **Supabase优势**:
  - 云端托管，无需本地维护
  - 自动备份和扩展
  - 内置PostGIS地理功能
- **Redis缓存**: 减少Supabase查询
- **连接池**: Supabase Pooler优化连接

---

## 🔧 常见问题定位

| 问题 | 检查点 | 解决方案 |
|-----|--------|---------|
| 前端无数据显示 | 1. Supabase连接<br>2. DATABASE_URL配置 | 检查.env中的DATABASE_URL |
| 数据不是最新 | 1. Redis缓存<br>2. 爬虫是否运行 | 清理Redis或运行爬虫 |
| 数据导入失败 | 1. Supabase连接<br>2. CSV格式 | 检查DATABASE_URL和CSV路径 |
| 爬虫后数据未更新 | 1. ETL是否触发<br>2. Supabase权限 | 检查trigger_etl_job()执行 |

---

## 📝 维护建议

1. **Supabase管理**:
   - 定期检查数据库大小（Supabase有限制）
   - 监控API调用次数
   - 备份重要数据

2. **自动化运行**:
   - 设置RUN_ON_STARTUP="true"测试
   - 配置PIPELINE_SCHEDULE定时运行

3. **监控数据质量**:
   - 检查特性提取准确性
   - 验证地理坐标有效性

---

## 🔑 关键配置

```env
# Supabase连接（生产环境）
DATABASE_URL="postgresql://...@aws-0-ap-southeast-2.pooler.supabase.com:5432/postgres"

# 自动化配置
PIPELINE_SCHEDULE="0 */8 * * *"  # 每8小时运行
RUN_ON_STARTUP="true"            # 启动时运行一次
```

---

**最后更新**: 2025-01-24
**关键修正**: 数据库实际使用Supabase云服务，而非本地PostgreSQL