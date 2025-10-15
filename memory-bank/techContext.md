# 技术上下文 (Technical Context)

**文档状态**: 生存文档 (Living Document)  
**最后更新**: 2025-10-15

---

## 当前技术栈

- **前端主站 (`apps/web`)**：Vue 3 (Composition API) + Vite 7 + Pinia + Vue Router + Element Plus + Tailwind v4（`@tailwindcss/postcss`，`preflight=false`，`darkMode: ['class','[data-theme="dark"]']`，核心 HSL 变量集中在 `src/styles/theme.css`）。`main.js` 先加载 UI 包 tokens，再加载 `design-tokens.css`、`theme.css`、Element Plus 桥接与 Tailwind；`vite.config.js` 将开发服务器固定在 5174 并启用 `strictPort`；Storybook 8.6.x（脚本端口 6007）作为业务组件与主题演示环境，Chromatic 通过 `@chromatic-com/storybook` 集成视觉回归。
- **设计系统 (`packages/ui`)**：Vue 组件库与样式令牌的单一事实来源。Style Dictionary 将 CSS 变量输出到 `src/styles/tokens.css` / `tokens.dark.css`（通过 `exports['./dist/tokens.css']` 暴露给消费方），并生成 `dist/style-dictionary/json/tokens.json` 与 `dist/tokens.mjs`；Storybook 8.6.x（脚本端口 6006）承载基础组件文档。
- **设计 Token 工具站 (`tools/design-site-astro`)**: Astro 驱动的浏览与调参与演示站点，消费 `packages/ui` 导出的 CSS 变量。 
- **后端 (`apps/backend`)**: Python FastAPI + SQLAlchemy，默认运行在 Uvicorn，提供 REST/GraphQL 服务及 Celery 任务队列。 
- **文档站 (`apps/docs-site`)**: Docusaurus 站点，汇总设计与产品文档。 
- **小程序实验**: `apps/uni-app` (uni-app Vite 模板) 与 `apps/mini-program` 保留用于探索跨端实现。 
- **包管理与任务编排**: pnpm@9.1.0 + Turborepo；Node.js 建议版本 >= 20。 
- **测试**: Vitest 3.x 用于单元测试，Playwright 用于端到端与视觉回归校验。

---

## 项目架构概览

### 仓库结构

- `apps/*` — 独立运行的应用或服务（前端、后端、文档、实验应用等）。
- `packages/*` — 可复用的内部包（UI 组件、工具库等）。
- `tools/*` — 辅助开发/演示工具，如设计 Token 站点与脚本。 
- `tokens/` — Style Dictionary 的源数据，定义原始/语义/组件层级令牌。
- `docs/` — 设计、产品与技术文档。

### 关键配置

- `pnpm-workspace.yaml` — 声明工作区范围。
- `turbo.json` — 定义跨包任务的执行顺序与缓存策略。
- 根 `package.json` — 聚合常用脚本（dev/build/lint/test/storybook 等）并声明强制依赖版本。

---

## 组件与样式流程

### Design Tokens

1. 在 `tokens/` 下编辑 JSON 源数据（按原始 → 语义 → 组件分层）。
2. 执行 `pnpm build:tokens` 运行 Style Dictionary，生成：
   - `packages/ui/src/styles/tokens.css` (`:root`)
   - `packages/ui/src/styles/tokens.dark.css` (`[data-theme='dark']`)
   - 其他目标平台产物（如 mini-program WXSS）。
   - apps/web 主题层：`src/styles/theme.css`（核心 HSL 变量）与 `src/styles/el-theme-bridge.css`（EP 桥接）；Tailwind v4 使用 `@tailwindcss/postcss` 并禁用 `preflight`。
3. 组件仅消费语义层/组件层变量；严禁硬编码数值或直接消费原始令牌。

#### 构建与排错
- Token collisions：执行 `node scripts/build-tokens.js` 若出现“Token collisions”，使用更高日志级别定位重复命名并统一（建议：将 Style Dictionary 日志设为 verbose，或在脚本内打印冲突路径）。
- 输出位置：Web 变量输出到 `packages/ui/src/styles/tokens*.css`（暴露如 `--component-button-*`）；小程序 WXSS 输出到 `apps/mini-program/src/styles/generated/*.wxss`。
- 品牌配色差异：`tokens/themes/light.json` 仍输出桔色 `color.brand.*`，而 apps/web 主题已切换为蓝色 `theme.css`；统一品牌色后需重新运行 `pnpm build:tokens` 并发布 UI 包。

### Storybook 8.6.x 工作流

- **启动设计系统 Storybook**: `pnpm --filter @sydney-rental-hub/ui storybook`
- **启动业务应用 Storybook**: `pnpm --filter @web-sydney/web storybook`
- **构建静态站点**: 使用相应包内的 `storybook build` 脚本，产物输出到 `storybook-static/`。
- **Chromatic 集成**: 统一使用 `@chromatic-com/storybook@^4.1.1`，在 CI 中运行 `pnpm chromatic`（详见 `.github/workflows/`）。

### Astro 设计站

- **启动**: `pnpm --filter @srh/design-site-astro dev`
- **用途**: 快速预览 tokens、验证暗色模式和组件示例，不替代 Storybook，而是补充令牌调参体验。

---

## 本地开发流程

1. 安装依赖：`pnpm install`
2. 启动主要前端与后端：`pnpm dev`（依赖 Turborepo 在各包执行 `dev` 脚本）
3. 独立运行：
   - Web 前端：`pnpm --filter @web-sydney/web dev`
   - 后端 API：`pnpm --filter @web-sydney/backend dev`
   - Celery Worker：`pnpm --filter @web-sydney/backend worker`
4. 代码质量：
   - Lint：`pnpm lint`
   - 单测：`pnpm test`
   - Type Check：`pnpm typecheck`
   - Playwright：`pnpm --filter @web-sydney/web exec npx playwright test`

---

## 已知注意事项

- pnpm 使用严格的依赖去重策略，Storybook 8.6.x 需要在根 `pnpm.overrides` 中钉住版本以避免旧版包混入。升级 Storybook 相关依赖时务必同步更新根 overrides 与子包 `package.json`。
- Storybook 与 Vite 插件生态差异较大，遇到编译报错时优先检查 `apps/web/vite.config.ts` 与 `packages/ui/.storybook/main.ts` 的兼容性配置。 
- FastAPI 服务使用 `.env` 中的凭据，运行本地后端前确保环境变量齐备。 
- Playwright 安装浏览器依赖需要执行 `pnpm --filter @web-sydney/web exec npx playwright install`。

---

## 近期变更日志

- **2025-10-14**: apps/web 引入 Tailwind v4（`@tailwindcss/postcss`，preflight=false），新增 `src/styles/theme.css`（核心 HSL 变量）与 `src/styles/el-theme-bridge.css`（EP 变量映射），`darkMode` 同时支持 `.dark` 与 `[data-theme="dark"]`；/globals-demo 与 /cards-demo 验证统一视觉与可访问性（focus-visible 由 `--ring` 驱动）；修复 /cards-demo → 详情页 404（store 预注入 + fetch guard）；DevServer 使用 5174/`strictPort: true`。
- **2025-10-13**: 新增 `component.button.*`（primary/secondary/ghost/link；sm/md/lg；含状态与通用项），构建产物包含 `--component-button-*`；`BaseButton.vue` 改为消费组件层 Token；记录 Token collisions(3) 待清理。
- **2025-02-14**: 完成 Storybook 8.6.x 版本统一，移除 npm 锁文件与过时原型 HTML，确保 pnpm + Turborepo 为唯一依赖来源。
- **2025-01**: 引入 Vitest 3.x 与 Playwright 1.55 作为统一测试栈，并在 `apps/web` 中扩展样式 Lint 规则。 
- **2024 Q4**: 完成设计 Token 分层重构，将 CSS 变量输出迁移到 `packages/ui`，Astro 设计站改为直接消费该包。

---

## 新增：apps/web-shadcn（纯净 Web 子应用）

目标
- 在与 legacy 解耦的纯净环境中，以 Vite + Vue 3 + TypeScript + Tailwind v4 + shadcn-vue 重建 Property Detail 等页面，实现“像素级对标 + 高可维护性”。

关键依赖
- UI：shadcn-vue（按需生成组件到 `src/components/ui/*`）、`lucide-vue-next`
- 样式：Tailwind v4（`@tailwindcss/vite`），`src/style.css` → `@import "tailwindcss"`
- 反馈：`vue-sonner`（Toast）
- 文本：`markdown-it`（描述渲染，生产需注意 XSS 防护）

TS/构建配置
- `tsconfig.json`：
  - `"compilerOptions": { "baseUrl": ".", "paths": { "@/*": ["./src/*"] } }`
  - references 指向 `tsconfig.app.json` 与 `tsconfig.node.json`
- `tsconfig.app.json`：
  - include 覆盖：`"src/env.d.ts"`, `"src/**/*.d.ts"`, `"src/**/*.vue"`, `"src/**/*.ts?(x)"`
  - 建议显式补充（若 vue-tsc 仍找不到 alias）：`"baseUrl": "."`, `"paths": { "@/*": ["./src/*"] }`
- `src/env.d.ts`：
  ```ts
  /// <reference types="vite/client" />
  declare module '*.vue' {
    import type { DefineComponent } from 'vue'
    const component: DefineComponent<{}, {}, any>
    export default component
  }
  // 无 @types 时临时声明：
  declare module 'markdown-it';
  ```
- Vite：`vite.config.ts` 启用 `@tailwindcss/vite` 插件与 `alias: { '@': path.resolve(__dirname,'./src') }`

组件与页面现状
- 已接入（shadcn 生成）：alert, avatar, badge, button, card(+子件), carousel(+子件), dialog(+子件), input, separator, skeleton, sonner, textarea
- 新增：Tabs 组件家族（`Tabs/TabsList/TabsTrigger/TabsContent` + `index.ts`），并在 `PropertyDetail.vue` 将 “Description/Features” 合并为 `Details` 卡片下的 Tabs
- 缺口（P0 优先）：DatePicker/Calendar、Sheet/Drawer、Select/Combobox、Tooltip/Popover/Dropdown、Progress/Spinner、Label/Form、Tabs/Accordion/Table、Breadcrumb、Scroll Area

蓝图抓取与对标流程（“蓝图法”）
- 结构蓝图（已生成）：`docs/blueprints/domain/<slug>/blueprint-raw.json`（来自 web_fetch，含模块分区与文案字段）
- 视觉度量（待补）：使用真实浏览器注入探针导出 `tokens-suggestion.json`（colors/radius/shadows/spacing/typography/layout）与 1440/1024/390 截图（叠图验收）
- 合规边界：仅抓取“度量与指标”，不保存受版权保护资产（图片/字体/Logo/文案）

开发建议与已知问题
- 建议优先以“有头 shadcn”覆盖 80% 通用模块，以“无头/半无头”实现 Gallery 缩略条、Sticky CTA、Map Overlay、Floorplan Zoom 等像素敏感模块
- 已知：`vue-tsc -b` 可能出现 alias 类型找不到（`@/lib/utils`/`@/components/ui/*`）与 `markdown-it` 类型声明缺失
  - 修复：在 `tsconfig.app.json` 显式加入 `baseUrl/paths`；在 `src/env.d.ts` 加临时 `declare module 'markdown-it'` 或安装 `@types/markdown-it`
  - 修复核对清单（apps/web-shadcn）：
    - tsconfig.app.json：`compilerOptions.baseUrl="."` 与 `paths["@/*"]=["./src/*"]`
    - src/env.d.ts：临时 `declare module 'markdown-it'` 或安装 `@types/markdown-it`
    - 校验命令：
      - `pnpm -C apps/web-shadcn typecheck`
      - `pnpm -C apps/web-shadcn build`
    - 验证别名：确保 `@/lib/utils` 与 `@/components/ui/*` 在 IDE 可跳转，构建无报错
- 后续：完成批次 A 组件生成后，在 PDP 中接入 Schools/Transport（Tabs+Table）、Inspections（DatePicker+Sheet）、分享/收藏（Dropdown/Tooltip），并叠图校验至 ≤ 2px 偏差

运行与构建
- Dev：`pnpm -C apps/web-shadcn dev`
- Build：`pnpm -C apps/web-shadcn build`（依赖 `vue-tsc -b` + `vite build`，需先解决 alias 与类型声明）
- 质量：优先 Lint/TypeCheck；对可访问性（焦点/键盘）进行自查

## MCP 浏览器工具使用要点（简版 · 2025-10-15）
- 断点规范：1440 / 1024 / 390，DPR=2，stabilizationDelayMs=1500
- 选择器优先：使用 data-testid（如 listing-details__summary / __gallery），通过 chrome_get_interactive_elements 探测
- 截图策略：优先元素截图（chrome_screenshot + selector，savePng=true，storeBase64=false）；全页受配额（MAX_CAPTURE_VISIBLE_TAB_CALLS_PER_SECOND）影响，需间隔重试
- 文件落点：由浏览器保存到 Downloads；入库需人工移动到 docs/blueprints/domain/<slug>/...，再把 JSON 中绝对路径替换为相对路径（遵守文件系统规则）
- 抽取策略：computedStyle 受 CSP/扩展隔离影响不稳定；采用“占位→回填”，先写容器 width/height 与截图路径，其余字段置 null，后续自动/半自动回填
- tokens-suggestion.json 与 modules/*.json：统一结构（selectors/screen­shots/measurements/styles/nextActions），防止信息缺项
- 风险应对：注入/控制台抓取失败时立即切换“元素截图 + 半自动回填”，避免阻塞
