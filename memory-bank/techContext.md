# 技术上下文 (Technical Context)

**文档状态**: 生存文档 (Living Document)
**最后更新**: 2025-09-15

---

## 当前技术栈

- **前端**: Vue 3 (Composition API) + Vite + Element Plus + Pinia + lucide-vue-next（图标）
- **小程序计划**: 评估 TorUI 组件库（Taro/小程序生态）并验证 VS Code 下主题与 token 扩展的可行性
- **后端**: Python FastAPI + Strawberry GraphQL + Supabase (AWS悉尼区域)
- **数据库**: PostgreSQL (Supabase) + Redis缓存（默认 15 分钟 TTL）
- **地图**: Google Maps JavaScript/Static Map（前端）+ Google Directions（后端，生产）；当前无 Haversine 回退

---

## 项目架构概览

### 项目结构
- **Monorepo**: 采用 `pnpm` + `Turborepo` 结构。
- **工作区 (`apps/*`)**:
  - `apps/web`: Vue 3 前端应用。
  - `apps/backend`: Python FastAPI 后端服务。
  - `apps/mcp-server`: MCP 服务。
- **配置**:
  - `pnpm-workspace.yaml`: 定义工作区范围 (`apps/*`)。
  - `turbo.json`: 统一任务编排与缓存策略。
  - 根 `package.json`: 提供顶层命令 (`dev`, `build`, `lint` 等)。

### API集成架构
- **代理配置**: 默认将 `/api`转发到 `http://localhost:8000`
- **响应格式**: 统一 `{status, data, pagination, error}`结构
- **失败策略**: 快速失败并抛错，便于监控定位

---

## 筛选系统技术约定

### URL 幂等与状态同步
- **实现文件**: `apps/web/src/utils/query.js`（sanitizeQueryParams、isSameQuery）
- **落地点**: FilterPanel 统一面板、五个分面、HomeView.sort
- **前端表现**: 应用后 URL 可直链/刷新恢复，不写空键，地址栏不抖动

### 预估计数统一
- **composable**: useFilterPreviewCount 统一"应用（N）"口径
- **特性**: 并发序号守卫、300ms 防抖、组件卸载清理
- **降级**: 计数失败返回 null，按钮退回"应用/确定"

### 分组边界隔离
- **API**: `applyFilters(filters, { sections })`
- **分组**: area/price/bedrooms/availability/more
- **原则**: 仅删除指定分组旧键再合并，避免跨面板覆盖

---

## 开发环境

### 本地运行

项目已迁移至 `pnpm` + `Turborepo` 工作流，请在**项目根目录**执行所有命令。

```bash
# 1. 安装所有依赖 (首次或依赖更新后)
pnpm install

# 2. 启动所有服务 (推荐，并行启动前后端)
pnpm dev

# --- 或单独启动 ---

# 只启动 Vue 前端 (@web-sydney/web)
pnpm --filter @web-sydney/web dev

# 只启动 FastAPI 后端 (@web-sydney/backend)
pnpm --filter @web-sydney/backend dev
```

### E2E 测试
```bash
# 安装依赖（如首次）
npx playwright install

# 运行 URL 幂等冒烟测试
npx playwright test -g "URL 幂等与仅写非空键"
```

### 当前运行状态
- ✅ Vue前端: 正常运行 (localhost:5173)
- ✅ Python后端: 正常运行 (localhost:8000)
- ✅ 数据库连接: 正常 (Supabase PostgreSQL)
- ✅ 认证系统: JWT + 邮箱验证框架
- ✅ 通勤计算: Google Directions（生产）；无 Haversine 回退

---

## 设计系统

### JUWO品牌设计系统
- **主色**: #0057ff (纯正蓝)
- **统一圆角**: 6px（组件设计令牌）
- **布局对齐**: 1200px最大宽度，32px间距
- **响应式断点**: 768px（平板）、1200px（桌面）、1920px（超宽）

### 设计令牌约束
- **强制使用**: `var(--*)` 形式的 CSS 自定义属性
- **禁止**: 硬编码颜色、`var(--token, #hex)` 兜底形式
- **护栏**: Stylelint 规则拦截新增硬编码色

### 图标系统
- **标准**: 全站使用 `lucide-vue-next` SVG 图标库
- **导入**: `import { IconName } from 'lucide-vue-next'`
- **颜色**: `stroke: currentColor`，由外层控制

### 2025-10-07 平台战略更新
- **平台先后**: 小程序 → App → Android，所有设计规范以小程序实现为基线，再向其他端扩散。
- **组件框架策略**: 引入 TorUI 组件库验证 VS Code 下的主题/Token 配置能力，必要时封装补充原子组件以覆盖空缺。
- **Design Token 统一**: 借鉴 Polaris Migrator 的自动迁移手法，为颜色、字体、图标、标签、间距建立跨端 token 映射与校验脚本。
- **MVP 功能聚焦**: 先交付房源筛选、排序、搜索-查看-收藏-客服下单流程；后续迭代再扩展地铁/火车站点筛选、帖子发布、付费通知等高级能力。

---

## 性能优化成果

1. **虚拟滚动优化**: DOM节点减少99.8%，列表加载提升83%
2. **API响应加速**: 服务端响应从8-10秒降至0.4-0.5秒，提升20倍
3. **数据库索引**: 筛选查询从2.2秒降至0.59秒，提升3.7倍
4. **缓存策略**: 15分钟客户端缓存 + Redis降级到内存缓存

---

## 部署配置

### Netlify 部署
- **配置文件**: netlify.toml
- **构建设置**: base="apps/web", command="pnpm --filter @web-sydney/web build", publish="dist"
- **SPA 重写**: `/*` → `/index.html` (status=200)

### 本地运维（PowerShell）
```powershell
# 进入项目根目录
Set-Location 'C:\Users\nuoai\Desktop\WEB-sydney-rental-hub'

# 跑 ETL
& 'C:\Python313\python.exe' 'scripts\automated_data_update_with_notifications.py' --run-once

# 清缓存
Invoke-WebRequest -UseBasicParsing -Method POST -Uri 'http://localhost:8000/api/cache/invalidate?invalidate_all=true' | Out-Null
