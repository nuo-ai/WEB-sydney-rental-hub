# 阶段 2：数据准备与后端逻辑

**目标：** 设置本地数据源和访问它的后端程序。

**任务：**

*   [ ] **创建本地 F1 数据集：** 验证 `docs/dataset/f1_data.json` 存在并包含结构化的模拟数据（车手、车队、比赛等）。
*   [ ] **实现后端 API/程序 (tRPC/API 路由)：**
    *   [ ] 创建端点/程序以获取仪表盘布局配置（初始硬编码/本地存储）。
    *   [ ] 创建端点/程序以保存/更新仪表盘布局配置（到本地存储/简单文件）。
    *   [ ] 创建端点/程序 (`getF1Data`?) 以读取 `f1_data.json` 并根据输入参数（例如 `driverId`、`trackId`、`season`）进行过滤。

*参考：project_plan_steps.md 中的步骤 5-6*

# Phase 2: Data Preparation & Backend Logic

**Goal:** Set up the local data source and backend procedures to access it.

**Tasks:**

*   [ ] **Create Local F1 Dataset:** Verify `docs/dataset/f1_data.json` exists and contains structured mock data (drivers, teams, races, etc.).
*   [ ] **Implement Backend API/Procedures (tRPC/API Routes):**
    *   [ ] Create endpoint/procedure to fetch dashboard layout configuration (initially hardcoded/local storage).
    *   [ ] Create endpoint/procedure to save/update dashboard layout configuration (to local storage/simple file).
    *   [ ] Create endpoint/procedure (`getF1Data`?) to read `f1_data.json` and filter based on input parameters (e.g., `driverId`, `trackId`, `season`).

*Reference: Steps 5-6 in project_plan_steps.md*
