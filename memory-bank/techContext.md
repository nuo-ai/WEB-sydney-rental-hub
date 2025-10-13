# 技术上下文 (Technical Context)

**文档状态**: 生存文档 (Living Document)  
**最后更新**: 2025-02-14

---

## 当前技术栈

- **前端主站 (`apps/web`)**: Vue 3 (Composition API) + Vite 7 + Pinia + Vue Router + Element Plus。Storybook 8.6.x 作为组件开发与演示环境，Chromatic 用于可视化回归。
- **设计系统 (`packages/ui`)**: Vue 组件库与样式令牌的单一事实来源。依赖 Style Dictionary 生成跨端 Token 产物，并通过 Storybook 8.6.x 提供组件/基础样式文档。
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
3. 组件仅消费语义层/组件层变量；严禁硬编码数值或直接消费原始令牌。

#### 构建与排错
- Token collisions：执行 `node scripts/build-tokens.js` 若出现“Token collisions”，使用更高日志级别定位重复命名并统一（建议：将 Style Dictionary 日志设为 verbose，或在脚本内打印冲突路径）。
- 输出位置：Web 变量输出到 `packages/ui/src/styles/tokens*.css`（暴露如 `--component-button-*`）；小程序 WXSS 输出到 `apps/mini-program/src/styles/generated/*.wxss`。

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

- **2025-10-13**: 新增 `component.button.*`（primary/secondary/ghost/link；sm/md/lg；含状态与通用项），构建产物包含 `--component-button-*`；`BaseButton.vue` 改为消费组件层 Token；记录 Token collisions(3) 待清理。
- **2025-02-14**: 完成 Storybook 8.6.x 版本统一，移除 npm 锁文件与过时原型 HTML，确保 pnpm + Turborepo 为唯一依赖来源。
- **2025-01**: 引入 Vitest 3.x 与 Playwright 1.55 作为统一测试栈，并在 `apps/web` 中扩展样式 Lint 规则。 
- **2024 Q4**: 完成设计 Token 分层重构，将 CSS 变量输出迁移到 `packages/ui`，Astro 设计站改为直接消费该包。
