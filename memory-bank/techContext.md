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
- **工作区**:
  - `apps/*`: 存放各个独立的应用程序（前端、后端等）。
  - `packages/*`: 存放共享的库和包，例如设计系统。
    - `@sydney-rental-hub/ui`: 设计系统的核心包，包含可复用的UI组件和样式令牌。
- **配置**:
  - `pnpm-workspace.yaml`: 定义工作区范围（`apps/*`, `packages/*` 等）。
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

# 3. 构建设计系统产物 (Tokens)
pnpm build:tokens

# 4. 独立运行设计系统开发环境 (Storybook)
pnpm run storybook -- -c packages/ui/.storybook

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

### Vite 启动问题排查 (2025-10-10)

- **问题1**: Storybook v8 与 `@storybook/addon-vitest` (v9) 版本不兼容，导致 `import` 失败。
  - **解决方案**: 在 `vite.config.js` 中改为异步和条件导入 `addon-vitest`，仅在 `isStorybook` 环境下加载。
- **问题2**: `vite-plugin-vue-devtools` 内部依赖的 `vite-plugin-inspect` 与 Vite 7+ 不兼容，因 `server.environments` 属性被移除而崩溃。
  - **解决方案**: 添加一个自定义的 `viteInspectCompatPatch` 插件，在 `configureServer` 钩子中为 `server.environments` 提供一个空对象 `{}` 作为 polyfill，确保插件能正常运行。
- **问题3**: 之前的开发进程未完全关闭，导致端口被占用。
  - **解决方案**: 使用 `netstat -aon | findstr <PORT>` 找到进程 PID，然后通过 `taskkill /PID <PID> /F` 强制终止。
- ✅ 认证系统: JWT + 邮箱验证框架
- ✅ 通勤计算: Google Directions（生产）；无 Haversine 回退

---

## 设计系统与工具链

### 1. 设计令牌 (Design Tokens)

- **单一事实来源**: `tokens/design-tokens.json` 是所有设计决策的唯一来源，遵循 W3C Design Tokens 规范。
- **自动化流程**: 使用 `Style Dictionary` 工具链将 JSON 令牌自动转换为多种格式。
  - **命令**: `pnpm build:tokens`
  - **产物**:
    - `packages/ui/dist/tokens.css`: 供所有前端应用消费的 CSS 自定义属性。
    - `packages/ui/dist/tokens.mjs`: 供 JS/TS 使用的令牌对象。
- **集成**: 主应用 `apps/web` 已全局导入 `tokens.css`，取代了旧的手动样式文件。

### 2. 组件开发 (Component Development)

- **核心包**: `@sydney-rental-hub/ui` 是所有可复用UI组件的家。
- **开发环境**: 使用 `Storybook` 作为独立的组件开发和文档环境。
  - **命令**: `pnpm --filter @sydney-rental-hub/ui run storybook`
  - **目的**: 在隔离的环境中开发、测试和可视化组件，确保其通用性和健壮性。
- **组件规范**:
  - 组件应**完全基于 Design Tokens** 构建，不包含任何硬编码样式值。
  - 优先从 `apps/web/src/components/base/` 中提炼和迁移现有基础组件。

### 3. 图标系统

- **标准**: 全站使用 `lucide-vue-next` SVG 图标库。
- **导入**: `import { IconName } from 'lucide-vue-next'`
- **颜色**: `stroke: currentColor`，由外层文字颜色 (`color`) 控制。

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
```

---

## MCP (Model Context Protocol) 服务器管理

### 添加新的 MCP 服务器

有两种方法可以添加新的 MCP 服务器，**推荐使用方法一**。

#### 方法一：直接修改 Cline 配置文件 (推荐)

这是最直接、最不容易出错的方法。它直接利用 `npx` 从 npm 拉取并运行最新的服务器，无需在本地克隆或管理依赖。

1. **找到配置文件**:
   打开位于以下路径的 Cline 全局设置文件：
   `C:\Users\nuoai\AppData\Roaming\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`
2. **添加服务器配置**:
   在 `mcpServers` 对象中，添加一个新的条目。以 `mermaid-mcp-server` 为例，配置如下：

   ```json
   "mermaid-mcp-server": {
     "autoApprove": [],
     "disabled": false,
     "timeout": 60,
     "type": "stdio",
     "command": "cmd",
     "args": [
       "/c",
       "npx",
       "-y",
       "@peng-shawn/mermaid-mcp-server@latest"
     ]
   }
   ```
3. **重新加载 VS Code**:
   为了让 Cline 识别到新的服务器配置，你**必须**重新加载 VS Code 窗口。

   - 打开命令面板 (Ctrl+Shift+P 或 Cmd+Shift+P)。
   - 输入并选择 "Developer: Reload Window"。

#### 方法二：在本地项目中克隆和构建 (不推荐)

此方法涉及将服务器仓库克隆到本地项目（例如 `apps/` 目录），然后安装依赖并构建。

**注意**: 在像本项目这样的 monorepo 环境中，直接在子目录运行 `pnpm install` 可能会因为根目录的依赖版本冲突而失败。因此，**强烈建议使用方法一**以避免此类问题。
