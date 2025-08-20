# 资产复用计划 (Asset Reuse Plan)

本文档详细说明，在我们将前端技术栈从 Vanilla JS 升级到 React 的过程中，如何系统性地复用旧 `frontend` 目录中的已有资产，以最大化效率并确保业务逻辑的连贯性。

---

## 1. 复用原则

旧的 `frontend` 目录将作为新 `react-frontend` 项目的**“原型”和“高保真蓝图”**。我们不直接复制代码，而是系统性地迁移其核心价值。

---

## 2. 具体复用计划

### 2.1. 业务逻辑与 API 调用
- **来源**: `frontend/scripts/main.js`, `frontend/scripts/details.js`
- **复用途径**:
    - `fetchPropertyDetails` 函数中的 API 调用和数据处理逻辑，将被完整地迁移到新的 `react-frontend/src/hooks/usePropertyDetails.ts` 自定义 Hook 中。
    - `fetchAndRenderCommuteResults` 函数中的 API 调用逻辑，将被迁移到处理地图和通勤的 React 组件中。
    - 列表页的筛选和排序逻辑，将被用作构建新的 `usePropertyList.ts` Hook 的核心参考。

### 2.2. HTML 结构
- **来源**: `frontend/index.html`, `frontend/details.html`, `frontend/profile.html`
- **复用途径**:
    - 这些文件的 DOM 结构将作为我们构建 React 组件时的**视觉和结构参考**。
    - 例如，`details.html` 中的 `div#property-specs` 将被转化为一个独立的 `<PropertySpecs />` React 组件，其内部结构和显示的信息将保持一致。
    - 这为我们节省了大量的页面从零开始的设计和规划时间。

### 2.3. 配置文件
- **来源**: `frontend/netlify.toml`
- **复用途径**:
    - 文件中定义的 `[[redirects]]` 代理规则，在验证后将被**直接复制**到新的 `react-frontend/netlify.toml` 文件中，以确保前端能继续通过代理与后端 API 通信。

### 2.4. Serverless Functions
- **来源**: `frontend/functions/` 目录
- **复用途径**:
    - 整个 `functions` 目录，包括 `get-directions` 等云函数，将被**直接移动**到新的 `react-frontend/netlify/functions` 目录下。
    - 这些函数是独立的 Node.js 环境，与前端框架无关，可以无缝复用。

### 2.5. 静态资源
- **来源**: `frontend/` 目录下的图片、图标等资源。
- **复用途径**:
    - 所有需要的静态资源文件将被移动到 `react-frontend/public/` 目录下，以便在新的 React 应用中继续使用。

---
