# 🏠 Sydney Rental Hub - 项目主索引

> **最后更新**: 2025-09-06 (部署与构建修复、图标库一致化)
> **重要更新**: Netlify 部署对齐（base=vue-frontend / npm run build / dist）+ SPA 重写（/* → /index.html）；修复 PropertyDetailNew.vue 双 template 构建错误；恢复详情页 lucide-vue-next 并新增依赖；保留此前筛选/样式/文档精简成果
> **用途**: 快速导航和定位项目所有重要文件和功能

### Solo 实时协作 TL;DR

- 保持前后端服务常开；我不启动/不关闭服务
- 改动前用 ≤3 行计划：目标 / 改动文件 / 风险与回滚
- 小步提交：一次仅一个组件或 1–2 个文件，优先复用全局 tokens 与统一栅格
- 本地验证：刷新页面；如异常，仅贴 Console/Network 摘要或截图（最小信息）
- 记录一行：activeContext.md 更新“做了什么 + 任务号/commit”；遇接口/全局样式/性能影响再升至 Level 1（加最小 E2E）

完整规则见 ../.clinerules/development-guidelines.md（第7节：Solo 实时协作与省 Token 规则；第8节：验收与沉淀流程）

#### 最小反馈清单（不建 docs，直接贴要点即可）

- 复现：路径 + 1–2 步骤 + 期望/实际（≤3 行）
- Console：最多 3 行（文件/行号/错误摘要）
- Network（若相关）：METHOD URL STATUS + 响应前几行
- 样式问题：截图 + 当前窗口宽度（px）
- 环境（可选）：浏览器版本 / OS / 时间

---

## 📚 Memory Bank 文档索引

| 文档                                  | 用途               | 更新频率 | 字数 (精简后) |
| ------------------------------------- | ------------------ | -------- | ------------- |
| [projectbrief.md](./projectbrief.md)     | 项目概述和商业目标 | 低       | ~300          |
| [productContext.md](./productContext.md) | 用户故事和交互流程 | 低       | ~200          |
| [techContext.md](./techContext.md)       | 技术栈和架构详情   | 中       | ~500          |
| [systemPatterns.md](./systemPatterns.md) | 设计模式和最佳实践 | 中       | ~600          |
| [progress.md](./progress.md)             | 开发进展记录       | 高       | ~800          |
| [activeContext.md](./activeContext.md)   | 当前任务和紧急事项 | 高       | ~500          |

---

## 🔥 核心性能数据

- **列表渲染**: 0.5秒 (优化前3秒，提升83%)
- **API响应**: 0.4-0.5秒 (优化前8-10秒，提升20倍)
- **筛选查询**: 0.59秒 (优化前2.2秒，提升3.7倍)
- **DOM节点**: ~400个 (优化前17万+，减少99.8%)
- **内存占用**: 50MB (优化前400MB，减少87.5%)

---

## 🗺️ 项目结构导航

### 前端 (Vue 3 + Pinia + Vue Router)

注：标注 ✨ 表示规划中或进行中模块

```
src/
├── views/                 # 页面组件
│   ├── HomeView.vue      # 首页(房源列表)
│   ├── PropertyDetail.vue # 详情页
│   ├── CommuteTimes.vue  # 通勤查询 ✨
│   ├── LoginView.vue     # 认证页
│   ├── Favorites.vue     # 收藏页
│   └── ProfileView.vue   # 个人中心
│
├── components/           # 可复用组件
│   ├── PropertyCard.vue      # 房源卡片(580px标准)
│   ├── VirtualPropertyList.vue # 虚拟滚动组件 ✅启用
│   ├── SearchBar.vue         # 自动补全搜索
│   ├── FilterPanel.vue       # 筛选面板(抽屉式)
│   ├── FilterTabs.vue        # 已弃用（不渲染）；筛选入口在搜索框后缀图标（sliders）
│   ├── Navigation.vue        # 响应式导航栏
│   └── commutes/             # 通勤相关组件 ✨
│
├── stores/               # Pinia状态管理
│   ├── properties.js       # 房源数据(unified data)
│   ├── auth.js            # 用户认证与地址 ✨
│   └── commute.js         # 通勤计算与缓存 ✨
│
├── services/api.js       # API服务层封装
└── router/index.js       # SPA路由配置
```

### 后端 (FastAPI + GraphQL)

```
├── main.py               # API端点定义 + 服务入口
├── db.py                 # Supabase连接池配置
├── api/graphql_schema.py # GraphQL查询支持
├── crud/                 # 数据访问层
├── models/               # 数据模型定义
└── config/               # 配置管理
```

---

## 🔌 核心API端点

| 端点                      | 方法 | 功能                  | 缓存策略       |
| ------------------------- | ---- | --------------------- | -------------- |
| `/api/properties`       | GET  | 房源列表 + 分页       | 服务端分页     |
| `/api/properties/{id}`  | GET  | 房源详情              | 30分钟缓存     |
| `/api/directions`       | GET  | 后端代理 Google Directions（生产）；失败回退 Haversine（测试/降级） | 后端计算（必要时 Haversine 降级） |
| `/api/auth/register`    | POST | 用户注册              | JWT令牌        |
| `/api/user/addresses`   | POST | 地址持久化            | localStorage   |
| `/graphql`              | ALL  | 灵活数据查询          | 不适用于AI工具 |
| `/api/cache/invalidate` | GET  | 缓存失效（测试/调试） | 测试环境       |

**禁止** ❌: 前端调用AI工具的Express服务器 (`localhost:3001`)

---

## ⚡ 服务运行状态

- ✅ **Vue前端**: `http://localhost:5173` (虚拟DOM + 响应式)
- ✅ **Python后端**: `http://localhost:8000` (FastAPI + GraphQL)
- ✅ **性能优化**: 虚拟滚动 + API缓存 + 数据库索引
- ✅ **搜索功能**: 全量数据搜索89号，相邻区域推荐
- ✅ **筛选系统**: 单选逻辑 + 服务端筛选 + 区域联动
- ✅ **认证系统**: JWT + 邮箱验证 + 测试模式支持
- ✅ **地图服务**: OpenStreetMap 底图 + 后端 Google Directions（生产）+ Haversine（降级）
- ✅ **通勤功能**: 后端 Google Directions API 已启用；本地 Haversine 仅作测试/降级使用

---

## 🔑 数据模型概要

### Property核心字段

```javascript
{
  listing_id: Number,      // 主键ID
  address: String,        // 完整地址
  suburb: String,         // 区域名称
  rent_pw: Number,        // 周租金
  bedrooms: Number,       // 卧室数
  bathrooms: Number,      // 浴室数
  available_date: Date,   // 入住日期
  images: Array,          // 图片数组
  latitude: Number,       // GPS纬度
  longitude: Number,      // GPS经度
  // + 8个V4特性字段
}
```

---

## 🚨 高优先级任务 (P0)

- 等待用户沟通后确认

## 🚀 快速启动

```bash
# 后端启动 (Python FastAPI)
python scripts/run_backend.py

# 前端启动 (Vue 3 + Vite)
cd vue-frontend && npm run dev

# 状态检查
curl http://localhost:5173/     # 前端索引页
curl http://localhost:8000/docs # API文档页
```

---

## 🛠️ 开发工作流

### 前期准备

- 启动后端服务 (`FastAPI :8000`)
- 处理前端 (`local-urban :5173`)
- 检查Supabase数据库连接

### 功能开发

- 使用Pinia store管理状态变化
- 通过Vite proxy (`/api`) 调用后端
- 遵循单一数据源原则和组件职责分离

### 性能测试

- 使用虚拟滚动查看页面性能
- 检查网络面板的API请求时间
- 验证筛选和搜索的响应速度

---

## 🔍 故障排除指南

| 问题症状     | 定位文件/组件                 | 解决思路                 |
| ------------ | ----------------------------- | ------------------------ |
| 房源列表空白 | `api.js`, `properties.js` | 检查API调用和数据格式    |
| 筛选无效     | `applyFilters()` action     | 确认服务端筛选参数       |
| 详情页报错   | `PropertyDetail.vue`        | 检查ID类型转换和字段名称 |
| 通勤功能失败 | `CommuteCalculator.vue`     | 验证Google API替代方案   |
| 图片不显示   | `PropertyCard.vue`          | 检查images数组处理逻辑   |
