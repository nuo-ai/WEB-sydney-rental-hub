# 阶段 5：交互性与数据绑定

**目标：** 实现动态仪表盘交互、数据获取和过滤功能。

**任务：**

*   [ ] **配置拖放与调整大小：**
    *   [ ] 设置 `react-grid-layout` 配置以拖动和调整小部件大小。
    *   [ ] 实现布局更改的状态管理。
    *   [ ] 创建函数以将布局更改持久化到本地存储/后端。
*   [ ] **实现数据绑定：**
    *   [ ] 将小部件连接到 tRPC 程序/API 路由以获取 F1 数据。
    *   [ ] 根据小部件配置创建小部件数据获取钩子。
    *   [ ] 在数据获取期间为小部件添加加载状态/骨架屏：
        *   [ ] `pnpm dlx shadcn@latest add skeleton`
    *   [ ] 处理数据获取问题的错误状态。
*   [ ] **创建全局过滤器和变量：**
    *   [ ] 在仪表盘标题/侧边栏中设计和实现过滤器 UI：
        *   [ ] 赛季过滤器（下拉菜单）
        *   [ ] 车队过滤器（下拉菜单）
        *   [ ] 车手过滤器（下拉菜单）
        *   [ ] 赛道过滤器（下拉菜单）
    *   [ ] 实现过滤器状态管理（例如，React Context）。
    *   [ ] 将过滤器与小部件数据获取集成。
    *   [ ] 示例：按“2023 赛季”过滤应更新所有相关小部件。

*参考：project_plan_steps.md 中的步骤 12-14*

# Phase 5: Interactivity & Data Binding

**Goal:** Implement dynamic dashboard interactions, data fetching, and filtering capabilities.

**Tasks:**

*   [ ] **Configure Drag-and-Drop & Resize:**
    *   [ ] Set up `react-grid-layout` configuration for dragging and resizing widgets.
    *   [ ] Implement state management for layout changes.
    *   [ ] Create functions to persist layout changes to local storage/backend.
*   [ ] **Implement Data Binding:**
    *   [ ] Connect widgets to tRPC procedures/API routes for F1 data.
    *   [ ] Create widget data fetching hooks based on widget configuration.
    *   [ ] Add loading states/skeletons for widgets during data fetching:
        *   [ ] `pnpm dlx shadcn@latest add skeleton`
    *   [ ] Handle error states for data fetching issues.
*   [ ] **Create Global Filters & Variables:**
    *   [ ] Design and implement filter UI in dashboard header/sidebar:
        *   [ ] Season filter (dropdown)
        *   [ ] Team filter (dropdown)
        *   [ ] Driver filter (dropdown)
        *   [ ] Track filter (dropdown)
    *   [ ] Implement filter state management (e.g., React Context).
    *   [ ] Integrate filters with widget data fetching.
    *   [ ] Example: Filtering by "2023 Season" should update all relevant widgets.

*Reference: Steps 12-14 in project_plan_steps.md*
