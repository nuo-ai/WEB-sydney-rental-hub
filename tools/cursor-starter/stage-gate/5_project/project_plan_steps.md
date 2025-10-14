# 项目计划步骤：类似 PowerBI 的 F1 仪表盘

本文档概述了使用现有 T3 技术栈（Next.js、TypeScript、Tailwind CSS）构建简化的类似 PowerBI 的仪表盘应用程序的步骤，重点是使用本地 JSON 数据集的一级方程式数据示例。

**核心技术：**

*   **框架：** Next.js (App Router) - *现有 T3 设置*
*   **语言：** TypeScript - *现有 T3 设置*
*   **样式：** Tailwind CSS - *现有 T3 设置*
*   **UI 组件：** shadcn/ui
*   **数据处理：** 本地 JSON 文件 (`docs/dataset/f1_data.json`)
*   **潜在后端：** Next.js API 路由或 tRPC - *现有 T3 设置（可能是 tRPC）*
*   **包管理器：** pnpm

**阶段 1：项目设置与基础**

1.  **验证 T3 项目设置：**
    *   确保当前的 T3 项目结构已准备就绪（Next.js、TypeScript、Tailwind、tRPC/API 路由）。
    *   确认已配置必要的基础设置。
2.  **设置 shadcn/ui：**
    *   如果尚未完成，请集成 shadcn/ui。
    *   命令：`pnpm dlx shadcn@latest init`（按照提示进行配置）。
3.  **项目结构审查：**
    *   审查现有的 T3 结构（`src/app`、`src/components`、`src/lib`、`src/server/api` 等）。如有必要，为仪表盘特定的组件/逻辑进行调整。参考 Next.js 最佳实践 ([https://nextjs.org/docs/app/getting-started/project-structure](https://nextjs.org/docs/app/getting-started/project-structure))。
4.  **安装核心依赖项：**
    *   添加用于图表和拖放功能的库。
    *   示例：`pnpm add recharts`（或其他图表库）；`pnpm add react-grid-layout @types/react-grid-layout`（或类似库）。

**阶段 2：数据准备与后端逻辑**

5.  **创建本地 F1 数据集：**
    *   创建一个新文件：`docs/dataset/f1_data.json`。
    *   用模拟的 F1 数据（车手、车队、比赛结果、赛道信息、赛季等）填充此文件。结构要逻辑清晰，便于解析。
    *   *示例结构：* 可以是一个对象，其键为 `drivers`、`teams`、`races`，其中 `races` 是一个对象数组，包含结果并链接到车手/车队 ID。
6.  **后端 API/程序：**
    *   为以下功能设置 tRPC 程序或 API 路由：
        *   获取仪表盘布局配置（最初可能硬编码或来自另一个简单的 JSON/本地存储）。
        *   保存/更新仪表盘布局配置（在开发期间持久化到本地存储或简单文件）。
        *   根据小部件配置和过滤器从 `f1_data.json` 文件中获取数据。
    *   *F1 示例：* 一个程序 `getF1Results(input: { driverId?: string; trackId?: string; season?: number })` 将读取 `f1_data.json`，根据输入进行过滤，并返回相关数据。

**阶段 3：核心仪表盘 UI**

7.  **仪表盘布局组件：**
    *   创建一个主仪表盘页面（例如，`src/app/dashboard/page.tsx` 或 `src/app/dashboard/[dashboardId]/page.tsx`，如果以后计划有多个仪表盘）。
    *   为主仪表盘结构实现 `react-grid-layout`（或选择的替代方案）。
8.  **添加所需的 shadcn 组件：**
    *   为核心 UI 和小部件交互安装必要的 shadcn 组件。
    *   可能的组件：
        *   `button`：用于添加小部件、保存等操作。
        *   `card`、`card-header`、`card-content`、`card-title`、`card-description`、`card-footer`：用于构建单个小部件。
        *   `dialog`：用于小部件配置模态框。
        *   `sheet`：用于配置侧边栏的替代方案。
        *   `dropdown-menu`：用于过滤器选择、小部件选项。
        *   `select`：用于过滤器的更简单的下拉菜单。
        *   `input`：用于任何基于文本的配置。
        *   `label`：用于配置中的表单元素。
        *   `resizable`：如果不使用处理它的网格库，可能对直接调整大小句柄有用。
        *   `tooltip`：用于提示或额外信息。
        *   `table`、`table-header`、`table-body`、`table-row`、`table-head`、`table-cell`：用于数据表小部件。
        *   `separator`：视觉分隔符。
    *   命令：`pnpm dlx shadcn@latest add button card dialog sheet dropdown-menu select input label resizable tooltip table separator`（根据需要安装）。

**阶段 4：小部件实现**

9.  **小部件组件：**
    *   在 `src/components/widgets/` 中开发单个 React 组件（例如，`BarChartWidget.tsx`、`StatCardWidget.tsx`、`DataTableWidget.tsx`）。
    *   在这些组件中使用选择的图表库（例如，`recharts`）。
    *   将小部件内容包装在 shadcn `Card` 组件中。
10. **动态小部件渲染：**
    *   获取仪表盘布局配置（最初从本地存储/文件）并根据存储的位置/大小在 `react-grid-layout` 上动态渲染配置的小部件。
11. **小部件配置 UI：**
    *   使用 shadcn `Dialog` 或 `Sheet` 实现配置界面。
    *   使用 `Select`、`Input`、`Label` 等组件设置数据源键、维度、指标、图表类型等。
    *   *F1 示例：* 配置一个条形图小部件：选择“races”作为源，“driver.name”作为维度，“points”作为指标。

**阶段 5：交互性与数据绑定**

12. **拖放与调整大小：**
    *   配置 `react-grid-layout` 以允许拖动和调整大小。
    *   实现回调函数（`onLayoutChange`）以捕获位置/大小更改并更新布局状态（并持久化到本地存储/文件）。
13. **数据绑定：**
    *   将小部件连接到后端 API/tRPC 程序。
    *   小部件应使用其特定配置调用程序以从 `f1_data.json` 获取数据。
    *   在获取/处理数据时，使用条件渲染或 shadcn `skeleton` 组件实现加载状态。
    *   命令：`pnpm dlx shadcn@latest add skeleton`
14. **过滤器与变量：**
    *   在主仪表盘布局中（可能在网格之外）添加全局过滤器控件（例如，用于赛季、赛道、车队的 shadcn `Select` 或 `DropdownMenu`）。
    *   将过滤器状态向下传递给小部件或通过上下文/状态管理使其可访问。
    *   *F1 示例：* 在赛季下拉菜单中选择“2023”会触发相关小部件重新获取数据，并将 `season: 2023` 传递给后端程序。

**阶段 6：持久化与优化**

15. **仪表盘保存（本地）：**
    *   实现一个“保存布局”按钮，将当前的网格布局（小部件类型、位置、大小、配置）持久化到浏览器的本地存储或写入本地文件的简单后端端点。
16. **仪表盘加载（本地）：**
    *   在页面加载时，尝试从本地存储/文件加载已保存的布局配置。
17. **优化：**
    *   添加错误处理（例如，文件未找到、JSON 解析错误）。
    *   改进样式和响应性。
    *   确保过滤器、小部件配置和数据显示之间的平滑交互。

此更新计划侧重于使用本地 JSON 数据集，并与预期的 T3 和 shadcn/ui 设置更紧密地集成。

# Project Plan Steps: PowerBI-like F1 Dashboard

This document outlines the steps to build a simplified PowerBI-like dashboard application using an existing T3 stack (Next.js, TypeScript, Tailwind CSS), focusing on a Formula 1 data example using a local JSON dataset.

**Core Technologies:**

*   **Framework:** Next.js (App Router) - *Existing T3 Setup*
*   **Language:** TypeScript - *Existing T3 Setup*
*   **Styling:** Tailwind CSS - *Existing T3 Setup*
*   **UI Components:** shadcn/ui
*   **Data Handling:** Local JSON File (`docs/dataset/f1_data.json`)
*   **Potential Backend:** Next.js API Routes or tRPC - *Existing T3 Setup (likely tRPC)*
*   **Package Manager:** pnpm

**Phase 1: Project Setup & Foundation**

1.  **Verify T3 Project Setup:**
    *   Ensure the current T3 project structure is ready (Next.js, TypeScript, Tailwind, tRPC/API Routes).
    *   Confirm necessary base configurations are in place.
2.  **Setup shadcn/ui:**
    *   If not already done, integrate shadcn/ui.
    *   Command: `pnpm dlx shadcn@latest init` (Follow prompts for configuration).
3.  **Project Structure Review:**
    *   Review the existing T3 structure (`src/app`, `src/components`, `src/lib`, `src/server/api` etc.). Adapt if necessary for dashboard-specific components/logic. Refer to Next.js best practices ([https://nextjs.org/docs/app/getting-started/project-structure](https://nextjs.org/docs/app/getting-started/project-structure)).
4.  **Install Core Dependencies:**
    *   Add libraries for charting and drag-and-drop functionality.
    *   Example: `pnpm add recharts` (or other charting library) ; `pnpm add react-grid-layout @types/react-grid-layout` (or similar).

**Phase 2: Data Preparation & Backend Logic**

5.  **Create Local F1 Dataset:**
    *   Create a new file: `docs/dataset/f1_data.json`.
    *   Populate this file with mock F1 data (drivers, teams, race results, track info, seasons, etc.). Structure it logically for easy parsing.
    *   *Example Structure:* Could be an object with keys like `drivers`, `teams`, `races`, where `races` is an array of objects containing results and linking to driver/team IDs.
6.  **Backend API/Procedures:**
    *   Set up tRPC procedures or API routes for:
        *   Fetching dashboard layout configuration (initially maybe hardcoded or from another simple JSON/local storage).
        *   Saving/updating dashboard layout configuration (to local storage or a simple file for persistence during development).
        *   Fetching data *from* the `f1_data.json` file based on widget configurations and filters.
    *   *F1 Example:* A procedure `getF1Results(input: { driverId?: string; trackId?: string; season?: number })` would read `f1_data.json`, filter based on input, and return the relevant data.

**Phase 3: Core Dashboard UI**

7.  **Dashboard Layout Component:**
    *   Create a main dashboard page (e.g., `src/app/dashboard/page.tsx` or `src/app/dashboard/[dashboardId]/page.tsx` if multiple dashboards are planned later).
    *   Implement `react-grid-layout` (or chosen alternative) for the main dashboard structure.
8.  **Add Required shadcn Components:**
    *   Install the necessary shadcn components for the core UI and widget interactions.
    *   Likely components:
        *   `button`: For actions like adding widgets, saving.
        *   `card`, `card-header`, `card-content`, `card-title`, `card-description`, `card-footer`: For structuring individual widgets.
        *   `dialog`: For widget configuration modals.
        *   `sheet`: Alternative for configuration sidebars.
        *   `dropdown-menu`: For filter selections, widget options.
        *   `select`: Simpler dropdowns for filters.
        *   `input`: For any text-based configuration.
        *   `label`: For form elements in configuration.
        *   `resizable`: Potentially useful for direct resizing handles if not using a grid library that handles it.
        *   `tooltip`: For hints or extra info.
        *   `table`, `table-header`, `table-body`, `table-row`, `table-head`, `table-cell`: For data table widgets.
        *   `separator`: Visual dividers.
    *   Command: `pnpm dlx shadcn@latest add button card dialog sheet dropdown-menu select input label resizable tooltip table separator` (Install as needed).

**Phase 4: Widget Implementation**

9.  **Widget Components:**
    *   Develop individual React components within `src/components/widgets/` (e.g., `BarChartWidget.tsx`, `StatCardWidget.tsx`, `DataTableWidget.tsx`).
    *   Use the chosen charting library (e.g., `recharts`) inside these components.
    *   Wrap widget content within shadcn `Card` components.
10. **Dynamic Widget Rendering:**
    *   Fetch the dashboard layout configuration (from local storage/file initially) and dynamically render the configured widgets onto the `react-grid-layout` based on stored positions/sizes.
11. **Widget Configuration UI:**
    *   Implement the configuration interface using shadcn `Dialog` or `Sheet`.
    *   Use components like `Select`, `Input`, `Label` for setting data source keys, dimensions, metrics, chart types etc.
    *   *F1 Example:* Configure a bar chart widget: Select 'races' as source, 'driver.name' as dimension, 'points' as metric.

**Phase 5: Interactivity & Data Binding**

12. **Drag-and-Drop & Resize:**
    *   Configure `react-grid-layout` to allow dragging and resizing.
    *   Implement callback functions (`onLayoutChange`) to capture position/size changes and update the layout state (and persist to local storage/file).
13. **Data Binding:**
    *   Connect widgets to the backend API/tRPC procedures.
    *   Widgets should call the procedures with their specific configuration to get data from the `f1_data.json`.
    *   Implement loading states using conditional rendering or shadcn `skeleton` component while data is fetched/processed.
    *   Command: `pnpm dlx shadcn@latest add skeleton`
14. **Filters & Variables:**
    *   Add global filter controls (e.g., shadcn `Select` or `DropdownMenu` for season, track, team) likely in the main dashboard layout, outside the grid.
    *   Pass filter state down to widgets or make it accessible via context/state management.
    *   *F1 Example:* Selecting '2023' in a Season dropdown triggers relevant widgets to refetch data, passing `season: 2023` to the backend procedure.

**Phase 6: Persistence & Refinement**

15. **Dashboard Saving (Local):**
    *   Implement a "Save Layout" button that persists the current grid layout (widget types, positions, sizes, configurations) to the browser's local storage or a simple backend endpoint that writes to a local file.
16. **Dashboard Loading (Local):**
    *   On page load, attempt to load the saved layout configuration from local storage/file.
17. **Refinement:**
    *   Add error handling (e.g., file not found, JSON parsing errors).
    *   Improve styling and responsiveness.
    *   Ensure smooth interaction between filters, widget configurations, and data display.

This updated plan focuses on using the local JSON dataset and integrates more tightly with the expected T3 and shadcn/ui setup.
