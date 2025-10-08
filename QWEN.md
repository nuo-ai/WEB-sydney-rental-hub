# 悉尼租房平台 (Sydney Rental Platform) - QWEN Development Guide

## 项目概述

**项目名称**: 悉尼租房平台 (Sydney Rental Hub)  
**项目愿景**: 成为海外留学生在澳洲最信赖的、一站式的租房解决方案平台，通过技术手段消除信息差，解决执行难的问题。

### 核心问题
身在海外的留学生在寻找澳洲住处时，面临三大核心痛点：
1. **时间窗口错配**: 找房周期与本地市场房源空出周期难以匹配
2. **信息不对称**: 无法准确判断房源真实性价比、周边环境和通勤便利性  
3. **执行障碍**: 无法亲自看房、签约，难以在激烈竞争中胜出

### 技术架构
- **前端**: Vue 3 (Composition API) + Vite + Element Plus + Pinia + lucide-vue-next
- **后端**: Python FastAPI + Strawberry GraphQL + PostgreSQL (Supabase) + Redis
- **部署**: Netlify (前端) + Python backend (localhost:8000)
- **地图服务**: Google Maps API for directions and static maps

## Project Structure

```
├── apps/                       # Turborepo applications
│   ├── web/                    # Vue 3 frontend application
│   ├── backend/                # Python FastAPI backend
│   └── mcp-server/             # MCP server components
├── memory-bank/               # Project documentation (core design docs)
├── crawler/                   # Data crawling scripts
├── database/                  # Database configurations
├── scripts/                   # Utility scripts
├── tokens/                    # Design tokens
├── tools/                     # Development tools
├── archive/                   # Archived components
├── docs/                      # Additional documentation
└── ...
```

### Memory Bank Structure (关键文档)
- `memory-bank/projectbrief.md`: 项目愿景和核心问题
- `memory-bank/productContext.md`: 用户故事和核心交互流程
- `memory-bank/systemPatterns.md`: 系统设计和架构模式
- `memory-bank/techContext.md`: 技术上下文和开发环境
- `memory-bank/activeContext.md`: 当前上下文和焦点任务
- `memory-bank/progress.md`: 项目进展和路线图

## Building and Running

### Monorepo Setup (Turborepo + pnpm)
```bash
# Install all dependencies (first time or after dependency updates)
pnpm install

# Start all services (recommended, parallel start of frontend/backend)
pnpm dev

# --- Or start individually ---

# Start Vue frontend only (@web-sydney/web)
pnpm --filter @web-sydney/web dev

# Start FastAPI backend only (@web-sydney/backend)
pnpm --filter @web-sydney/backend dev
```

### Environment Variables
Copy `.env.example` to `.env` and configure the following:
- `DATABASE_URL`: PostgreSQL database connection string
- `REDIS_URL`: Redis connection string  
- `GOOGLE_MAPS_API_KEY`: Google Maps API key
- `SECRET_KEY`: JWT secret key
- `API_KEY`: API access key

### E2E Testing
```bash
# Install Playwright browsers (if first time)
npx playwright install

# Run URL idempotency smoke tests
npx playwright test -g "URL 幂等与仅写非空键"
```

## 核心功能

### MVP 核心价值
1. **智能向导式筛选**: 自动补全区域搜索 + 高级日期范围筛选
2. **信任代理**: "联系我们"服务，为海外学生提供线下服务入口
3. **AI聊天助手**: 智能路由到房源、法律、合同、服务等专业Agent

### 筛选系统功能
- 面积/价格/房型/可用日期筛选
- 日期范围筛选（支持特定时间段可入住）
- 家具筛选
- 附近区域推荐
- 保存搜索功能

### 用户功能
- 房源收藏
- 浏览历史记录
- 多设备同步（计划中）
- 个人中心管理

## 开发约定

### 代码规范
- **CSS**: 强制使用 CSS 变量 (`var(--*)`)，禁止硬编码颜色
- **图标**: 统一使用 `lucide-vue-next` 图标库
- **响应格式**: 统一 `{status, data, pagination, error}` 结构
- **URL同步**: 筛选状态与URL参数保持同步，支持直链/刷新恢复

### 架构模式
- **单向数据流**: Vue 3 Composition API + Pinia 状态管理
- **URL幂等性**: 筛选应用后URL可直链/刷新恢复，不产生抖动
- **缓存策略**: Redis缓存 + 15分钟TTL + 内存缓存降级
- **API一致性**: 详情端点为列表端点的超集

### 设计令牌
- **主色**: #0057ff (纯正蓝)
- **统一圆角**: 6px
- **布局对齐**: 1200px最大宽度，32px间距
- **响应式**: 768px/1200px/1920px 断点

## 项目特性

### 性能优化成果
1. **虚拟滚动**: DOM节点减少99.8%，列表加载提升83%
2. **API响应**: 服务端响应从8-10秒降至0.4-0.5秒，提升20倍
3. **数据库**: 索引查询从2.2秒降至0.59秒，提升3.7倍
4. **缓存**: 15分钟客户端缓存 + Redis降级

### AI聊天系统
- **智能路由**: 根据消息内容路由到property/legal/contract/service等专业Agent
- **服务卡片**: 支持展示房源、法律咨询、合同审核、代看房等服务
- **大学推荐**: 针对UTS/UNSW/USYD等大学的房源推荐

### 当前进展 (2025-10-07)
- ✅ 保存搜索功能完成 (Zillow风格)
- ✅ 筛选系统P0完成 (URL幂等、预估计数、分组隔离)
- ✅ 设计系统合规 (Storybook、图标统一、令牌化)
- ✅ AI聊天助手功能
- ✅ 移动端优化
- ✅ 多端战略：小程序 → App → Android (小程序为设计基线)

### 下一步计划
- **P0**: Design Token 先行 - 完成颜色/字体/图标/标签/间距的第一轮统一
- **P0**: TorUI 验证 - 在 VS Code 环境下测试 TorUI 主题与 Token 扩展可行性
- **P0**: MVP 功能范围控制 - 优先交付核心房源流程，暂缓增强功能
- **P1**: 引入 TorUI 组件库，建立统一 Design Token 体系

## 开发工具

### Frontend Toolchain
- **Build System**: Vite + Turborepo
- **Testing**: Vitest + Playwright + Storybook
- **Code Style**: ESLint + Prettier + Stylelint (with CSS variable enforcement)
- **Proxy**: Vite proxy to localhost:8000 (API requests)

### Backend Toolchain
- **Web Framework**: FastAPI
- **Database**: PostgreSQL (Supabase) + asyncpg
- **GraphQL**: Strawberry GraphQL
- **Caching**: Redis + FastAPICache
- **Queue**: Celery for background tasks
- **Security**: JWT + rate limiting + input validation

## Deployment Configuration

### Netlify Deployment
- **Config File**: netlify.toml
- **Build Settings**: base="apps/web", command="pnpm --filter @web-sydney/web build", publish="dist"
- **SPA Rewrite**: `/*` → `/index.html` (status=200)

### Backend Deployment
- **Dev**: uvicorn with --reload (localhost:8000)
- **Prod**: gunicorn/uvicorn workers with process management
- **Health Check**: Built-in health check and cache stats endpoints

## API Endpoints

### Main REST API
- `GET /api/properties` - Property list (with filtering/pagination)
- `GET /api/properties/{id}` - Property detail (superset of list endpoint)
- `GET /api/locations/suggestions` - Search suggestions with auto-complete
- `POST /api/chat` - AI chat system
- `GET /api/directions` - Commute time calculation
- `GET /api/health` - Health check
- `POST /api/cache/invalidate` - Cache management

### GraphQL Endpoint
- `GET/POST /graphql` - GraphQL API with GraphiQL
- Supports property queries, user authentication, and advanced filtering

## Special Notes

### Memory-Bank-Driven Development
This project uses memory-bank-driven development. All product requirements, technical architecture, and development plans are documented in `/memory-bank`. Always read relevant docs before starting work.

### Architecture Constraints
- **Data Flow**: Browser (Vue @ :5173) → Vite Proxy → Python Backend (@ :8000)
- **No Reverse Dependencies**: AI agents must not create reverse dependencies
- **API Consistency**: Detail endpoints must be supersets of list endpoints

### Security Measures
- API key authentication
- JWT token validation
- Input parameter whitelisting
- SQL injection protection
- CORS policy control

### Multi-Platform Strategy (as of 2025-10-07)
- **Platform Order**: 小程序 → App → Android
- **Design Baseline**: All design specs based on小程序 implementation
- **Component Library**: Evaluating TorUI for cross-platform compatibility
- **MVP Focus**: Property search/sort/view收藏/customer service (defer advanced features)

### External Dependencies
- Google Maps API (Directions/Static Maps)
- Supabase PostgreSQL
- Redis caching
- Email service (SendGrid/Mailgun)
- Lucide Vue Icons