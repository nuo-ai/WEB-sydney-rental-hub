# 阶段 4：小部件实现

**目标：** 为仪表盘创建核心小部件组件和配置 UI。

**任务：**

*   [ ] **开发小部件组件：**
    *   [ ] 创建基础小部件包装组件。
    *   [ ] 实现特定小部件类型：
        *   [ ] 条形图小部件（`src/components/widgets/BarChartWidget.tsx`）
        *   [ ] 折线图小部件（`src/components/widgets/LineChartWidget.tsx`）
        *   [ ] 统计卡片小部件（`src/components/widgets/StatCardWidget.tsx`）
        *   [ ] 数据表小部件（`src/components/widgets/DataTableWidget.tsx`）
    *   [ ] 确保所有小部件都使用 shadcn 的 `Card` 组件作为基础容器。
*   [ ] **实现动态小部件渲染：**
    *   [ ] 创建 `WidgetRegistry` 以将小部件类型映射到组件。
    *   [ ] 实现逻辑以获取仪表盘布局（初始硬编码/本地存储）。
    *   [ ] 根据布局配置动态渲染小部件。
*   [ ] **创建小部件配置 UI：**
    *   [ ] 为小部件设置实现配置对话框/面板 UI。
    *   [ ] 为数据源选择、维度、指标创建表单元素。
    *   [ ] 在适用情况下启用图表类型选择。
    *   [ ] 添加 F1 特定配置选项（例如，选择车手、车队、赛季）。

*参考：project_plan_steps.md 中的步骤 9-11*

# Phase 4: Widget Implementation

**Goal:** Create the core widget components and configuration UI for the dashboard.

**Tasks:**

*   [ ] **Develop Widget Components:**
    *   [ ] Create base Widget wrapper component.
    *   [ ] Implement specific widget types:
        *   [ ] Bar Chart Widget (`src/components/widgets/BarChartWidget.tsx`)
        *   [ ] Line Chart Widget (`src/components/widgets/LineChartWidget.tsx`)
        *   [ ] Stat Card Widget (`src/components/widgets/StatCardWidget.tsx`)
        *   [ ] Data Table Widget (`src/components/widgets/DataTableWidget.tsx`)
    *   [ ] Ensure all widgets use shadcn's `Card` components as base containers.
*   [ ] **Implement Dynamic Widget Rendering:**
    *   [ ] Create `WidgetRegistry` to map widget types to components.
    *   [ ] Implement logic to fetch dashboard layout (initially hardcoded/local storage).
    *   [ ] Render widgets dynamically based on layout configuration.
*   [ ] **Create Widget Configuration UI:**
    *   [ ] Implement configuration dialog/sheet UI for widget settings.
    *   [ ] Create form elements for data source selection, dimensions, metrics.
    *   [ ] Enable chart type selection where applicable.
    *   [ ] Add F1-specific configuration options (e.g., select drivers, teams, seasons).

*Reference: Steps 9-11 in project_plan_steps.md*
