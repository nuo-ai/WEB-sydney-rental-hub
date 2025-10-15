# 技术上下文 (Technical Context)

**文档状态**: 生存文档 (Living Document)
**最后更新**: 2025-10-16

---

## 当前技术栈

- **前端新架构 (`apps/vue-juwo`)**: Vue 3 (Composition API) + Vite + Pinia + shadcn-vue + tailwindcss。
- **设计系统 (`packages/ui`)**: Vue 组件库与样式令牌的单一事实来源。由 Style Dictionary 驱动。
- **后端 (`apps/backend`)**: Python FastAPI + SQLAlchemy，提供 REST/GraphQL 服务。
- **包管理与任务编排**: pnpm + Turborepo。

---

## 项目架构概览

- `apps/*`: 独立的应用 (前端, 后端, 文档等)。
- `packages/*`: 可复用的内部包 (UI 组件, 工具库)。
- `tools/*`: 辅助开发工具。
- `memory-bank/`: 项目的“单一事实来源”。

---

## 本地开发流程

1.  **安装依赖**: `pnpm install`
2.  **启动所有服务**: `pnpm dev`
3.  **独立运行**:
    - 前端: `pnpm --filter vue-juwo dev`
    - 后端: `pnpm --filter @web-sydney/backend dev`
4.  **代码质量**:
    - `pnpm lint`
    - `pnpm test`
    - `pnpm typecheck`
