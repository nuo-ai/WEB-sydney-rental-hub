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

## 项目结构

```
├── backend/                    # Python FastAPI backend
├── vue-frontend/              # Vue 3 frontend
├── crawler/                   # Data crawling scripts
├── database/                  # Database configurations
├── mcp-server/               # MCP server components
├── memory-bank/              # Project documentation (core design docs)
├── Property_data/            # Property data files
├── scripts/                  # Utility scripts
├── tests/                    # Test files
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

### 后端服务 (localhost:8000)
```bash
# 安装依赖 (首次运行)
pip install -r requirements.txt

# 启动后端服务
python scripts/run_backend.py
```

### 前端开发 (localhost:5173)
```bash
cd vue-frontend
npm install
npm run dev
```

### 环境变量配置
复制 `.env.example` 到 `.env` 并配置以下环境变量：
- `DATABASE_URL`: PostgreSQL数据库连接字符串
- `REDIS_URL`: Redis连接字符串  
- `GOOGLE_MAPS_API_KEY`: Google Maps API密钥
- `SECRET_KEY`: JWT密钥
- `API_KEY`: API访问密钥

### E2E 测试
```bash
# 安装 Playwright 浏览器
npx playwright install

# 运行测试
npx playwright test
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

### 当前进展 (2025-09-16)
- ✅ 保存搜索功能完成 (Zillow风格)
- ✅ 筛选系统P0完成 (URL幂等、预估计数、分组隔离)
- ✅ 设计系统合规 (Storybook、图标统一、令牌化)
- ✅ AI聊天助手功能
- ✅ 移动端优化

### 下一步计划
- **P0**: 筛选向导特性开关接入评估
- **P0**: 图标系统余量迁移
- **P1**: 令牌定义梳理
- **P2**: 移除var()颜色兜底

## 开发工具

### 前端工具链
- **构建工具**: Vite
- **测试**: Vitest + Playwright + Storybook
- **代码风格**: ESLint + Prettier + Stylelint
- **代理**: Vite proxy to localhost:8000

### 后端工具链
- **Web框架**: FastAPI
- **数据库**: PostgreSQL (Supabase) + asyncpg
- **GraphQL**: Strawberry GraphQL
- **缓存**: Redis + FastAPICache
- **队列**: Celery for background tasks
- **安全**: JWT + rate limiting + input validation

## 部署配置

### 前端部署 (Netlify)
- 构建命令: `npm run build`
- 发布目录: `dist/`
- SPA重写: `/*` → `/index.html`

### 后端部署
- **开发**: uvicorn with --reload
- **生产**: gunicorn/uvicorn workers
- **监控**: 内置health check和cache stats端点

## API端点

### 主要API
- `GET /api/properties` - 房源列表 (带筛选分页)
- `GET /api/properties/{id}` - 房源详情
- `GET /api/locations/suggestions` - 搜索建议
- `POST /api/chat` - AI聊天系统
- `GET /api/directions` - 通勤计算
- `GET /api/health` - 健康检查
- `POST /api/cache/invalidate` - 缓存管理

### GraphQL端点
- `GET/POST /graphql` - GraphQL API with GraphiQL
- 支持房源查询、用户认证等操作

## 特殊说明

### 记忆库驱动开发 (Memory-Bank-Driven Development)
本项目采用记忆库驱动开发模式，所有产品需求、技术架构、开发计划都记录在 `/memory-bank` 目录中。在开始任何工作前，务必先阅读相关文档。

### 安全措施
- API密钥认证
- JWT令牌验证
- 输入参数白名单校验
- SQL注入防护
- 跨域策略控制

### 外部依赖
- Google Maps API (Directions/Static Maps)
- Supabase PostgreSQL
- Redis缓存
- Email服务 (SendGrid/Mailgun)