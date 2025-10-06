# 🏠 Sydney Rental Hub - 项目主索引

> **最后更新**: 2025-01-30  
> **重要更新**: 虚拟滚动成功启用，渲染性能提升83%，DOM节点减少99.8%
> **用途**: 快速导航和定位项目所有重要文件和功能
> **原则**: 避免AI片面理解导致的连锁问题

---

## 📚 Memory Bank 文档索引

| 文档 | 用途 | 更新频率 |
|------|------|----------|
| [projectbrief.md](./projectbrief.md) | 项目概述和商业目标 | 低 |
| [productContext.md](./productContext.md) | 用户故事和交互流程 | 低 |
| [techContext.md](./techContext.md) | 技术栈和架构详情 | 中 |
| [systemPatterns.md](./systemPatterns.md) | 设计模式和最佳实践 | 中 |
| [progress.md](./progress.md) | 开发进展记录 | 高 |
| [activeContext.md](./activeContext.md) | 当前任务和紧急事项 | 高 |

---

## 🗺️ 项目结构导航

### 前端 (Vue 3)
```
apps/web/
├── src/
│   ├── views/               # 页面组件
│   │   ├── HomeView.vue         → 首页(房源列表)
│   │   ├── PropertyDetail.vue   → 房源详情页
│   │   ├── CommuteTimes.vue     → 通勤查询页面 ✨
│   │   ├── Favorites.vue        → 收藏页面
│   │   ├── CompareView.vue      → 对比页面
│   │   ├── Map.vue              → 地图视图
│   │   ├── Chat.vue             → AI聊天
│   │   ├── LoginView.vue        → 登录页
│   │   └── ProfileView.vue      → 个人中心
│   │
│   ├── components/          # 可复用组件
│   │   ├── PropertyCard.vue     → 房源卡片(核心)
│   │   ├── VirtualPropertyList.vue → 虚拟滚动列表 ✅启用
│   │   ├── SearchBar.vue        → 搜索栏
│   │   ├── FilterPanel.vue      → 筛选面板
│   │   ├── FilterTabs.vue       → 快速筛选
│   │   ├── Navigation.vue       → 导航栏
│   │   ├── CommuteCalculator.vue→ 通勤计算器
│   │   ├── CompareToolbar.vue   → 对比工具栏
│   │   ├── commute/             → 通勤相关组件 ✨
│   │   │   ├── TransportModes.vue → 交通方式选择
│   │   │   └── LocationCard.vue   → 地址卡片
│   │   └── modals/             → 模态框组件 ✨
│   │       ├── AuthModal.vue      → 认证模态框
│   │       ├── EmailVerifyModal.vue → 邮箱验证
│   │       ├── AddLocationModal.vue → 添加地址
│   │       └── NameLocationModal.vue → 地址命名
│   │
│   ├── stores/              # Pinia状态管理
│   │   ├── properties.js        → 房源数据store
│   │   ├── auth.js              → 认证store ✨
│   │   └── commute.js           → 通勤store ✨
│   │
│   ├── services/            # API服务层
│   │   └── api.js               → API封装
│   │
│   └── router/              # 路由配置
│       └── index.js             → 路由定义
```

### 后端 (FastAPI)
```
backend/
├── main.py                  # 主入口 + API端点定义
├── db.py                    # 数据库连接池
├── api/
│   └── graphql_schema.py   # GraphQL模式定义
├── crud/
│   ├── properties_crud.py  # 房源CRUD操作
│   └── commute_crud.py     # 通勤相关操作
├── models/
│   ├── property_models.py  # 房源数据模型
│   └── commute_models.py   # 通勤数据模型
├── config/
│   └── university_data.py  # 大学配置数据
└── tasks.py                 # Celery异步任务
```

### 数据库
```
database/
├── setup_database.sql       # 主表结构(properties)
├── setup_transport_stops_table.sql # 交通站点表
├── update_database.py       # 数据库更新脚本
└── process_csv.py          # CSV数据导入
```

---

## 🔌 API端点速查

### REST API
| 端点 | 方法 | 功能 | 缓存 |
|------|------|------|------|
| `/api/properties` | GET | 获取房源列表 | 15分钟 |
| `/api/properties/{id}` | GET | 获取房源详情 | 15分钟 |
| `/api/directions` | GET | 获取通勤路线 | 15分钟(前端) |
| `/api/chat` | POST | AI聊天 | 无 |
| `/api/health` | GET | 健康检查 | 无 |
| `/api/auth/register` | POST | 用户注册 | 无 |
| `/api/auth/login` | POST | 用户登录 | 无 |
| `/api/user/addresses` | GET/POST | 用户地址管理 | 无 |

### GraphQL
| 端点 | 功能 |
|------|------|
| `/graphql` | 灵活的数据查询接口 |

---

## 📊 数据流向图

```
用户浏览器 (localhost:5173)
    ↓
Vue 3 前端
    ↓
Vite Proxy (/api/*)
    ↓
FastAPI 后端 (localhost:8000)
    ↓
Supabase云数据库 (AWS悉尼) + Redis缓存
```

---

## 🔑 关键数据模型

### Property (房源)
```javascript
{
  listing_id: Number,        // 主键
  address: String,          // 地址
  suburb: String,           // 区域
  rent_pw: Number,          // 周租金
  bedrooms: Number,         // 卧室数
  bathrooms: Number,        // 浴室数
  parking_spaces: Number,   // 车位数
  available_date: Date,     // 可入住日期
  images: Array,            // 图片数组
  latitude: Number,         // 纬度
  longitude: Number,        // 经度
  // + 8个特性字段（V4版本）
}
```

---

## ⚠️ 已知问题和注意事项

### 需要立即关注的问题：
1. **虚拟滚动未启用（P0）**:
   - 已有VirtualPropertyList.vue组件但未使用
   - 3456条数据导致渲染卡顿3-5秒
   - **影响**: 列表页性能差，内存占用高
   - **解决**: 启用虚拟滚动，预期提升80%性能

2. **调试代码未清理（P0）**:
   - 35个console.log需要清理
   - **影响**: 生产环境信息泄露，性能损耗
   - **解决**: 使用构建工具自动移除

3. **收藏功能后端未实现（P1）**:
   - 4个TODO待实现API
   - **影响**: 核心功能缺失
   - **解决**: 实现后端收藏API

### 开发注意事项：
1. **修改前必读**:
   - 检查此索引了解整体架构
   - 查看相关组件的依赖关系
   - 验证API端点的实际返回格式

2. **避免的错误**:
   - ❌ 不要假设API格式，要实际检查
   - ❌ 不要只改前端不改后端
   - ❌ 不要忽视缓存的影响

3. **测试要点**:
   - ✅ 前后端联调测试
   - ✅ 缓存清理后测试
   - ✅ 错误情况测试

---

## 🚀 快速启动命令

```bash
# 启动后端
python scripts/run_backend.py

# 启动前端
cd apps/web && npm run dev

# 检查服务状态
curl http://localhost:5173/       # 前端
curl http://localhost:8000/api/health  # 后端
```

---

## 📝 开发工作流

1. **开始新任务前**:
   - 读取此INDEX.md了解全局
   - 读取activeContext.md了解当前状态
   - 检查相关模块的依赖关系

2. **修改代码时**:
   - 使用TodoWrite工具跟踪进度
   - 一次只改一处，立即验证
   - 考虑对其他模块的影响

3. **完成任务后**:
   - 更新progress.md记录变更
   - 更新activeContext.md反映新状态
   - 如有架构变化，更新此索引

---

## 🔍 常见问题快速定位

| 问题类型 | 检查文件 | 可能原因 |
|----------|----------|----------|
| 房源不显示 | `properties.js`, `api.js` | API调用失败或数据格式问题 |
| 图片不加载 | `PropertyCard.vue` | images数组处理或CDN问题 |
| 筛选无效 | `properties.js:applyFilters()` | 筛选逻辑或状态更新问题 |
| 详情页报错 | `PropertyDetail.vue`, `properties_crud.py` | ID类型或字段缺失问题 |
| 通勤计算失败 | `CommuteCalculator.vue`, `/api/directions` | Google API密钥或配额问题 |
| ~~列表卡顿~~ | ~~`HomeView.vue`, `VirtualPropertyList.vue`~~ | ~~虚拟滚动未启用~~ ✅已解决 |
| 查询缓慢 | `main.py:check_and_optimize_indexes()` | 数据库索引缺失或未优化 |

---

**维护提示**: 此索引是项目的导航中心，任何架构级变更都应及时更新此文件。