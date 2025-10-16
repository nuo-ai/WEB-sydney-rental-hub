# 系统设计模式与最佳实践 (System Patterns)

**文档状态**: 生存文档 (Living Document)
**最后更新**: 2025-10-16

---

## 核心架构决策

1.  **废弃旧前端**:
    - `archive/web` 中的旧版 Element Plus + Vue 3 前端代码库已废弃，不再进行任何维护和开发。

2.  **保留并重构后端**:
    - `apps/backend` 中的 FastAPI 后端服务将被完整迁移和重构，作为项目唯一的数据服务来源。
    - 所有 API 必须符合 `API_ENDPOINTS.md` 中定义的契约。

3.  **新前端架构 (`apps/vue-juwo`)**:
    - 采用 `shadcn-vue` 和 `tailwindcss` 作为核心 UI 构建方案。
    - UI 设计遵循 `shadcn-vue` 和 `tailwindcss` 的设计系统，仅对颜色等进行定制化。
    - 优先复用 `packages/ui` 中的设计令牌和基础组件。
    - **组件安装方式**: 由于 shadcn-vue CLI 存在配置问题，采用手动安装方式创建组件到 `src/components/ui/`

## Monorepo 原则

- 使用 `pnpm` + `Turborepo` 统筹所有应用与包。
- `apps/*`: 独立运行的应用。
- `packages/*`: 可复用的内部包。

## 数据与服务模式

- **单一数据源**: `apps/backend` 是唯一的数据服务来源。
- **前端数据流**: Vue + Pinia 作为前端的单一状态管理方案。
- **API 契约**: 后端 API 响应结构统一为 `{ status, data, error, pagination }`。
