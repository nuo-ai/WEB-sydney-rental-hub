# 当前上下文与紧急焦点

**最后更新**: 2025-09-05

---

2025-09-05｜PATCH-FILTER-MIN｜移除筛选失败时的本地回退递归；统一计数入口为 store.getFilteredCount；不改后端契约；影响文件 FilterPanel.vue / stores/properties.js｜commit 504304d（range dc68225..504304d）
2025-09-05｜DOC-FILTER-PLAN｜新增 docs/filter-upgrade-plan.md：筛选功能与面板升级技术方案；仅文档，无代码改动
2025-09-05｜DOCS-ALIGN｜对齐 Memory Bank：更新 /api/directions 为“后端 Google Directions（生产）+ Haversine 回退”，统一详情缓存 30min；纯文档，无代码改动
2025-09-05｜UI-PILL-COUNTER｜复刻图片计数器样式（min-width 118px、22×22 徽标、two-digits 胶囊、tabular-nums），模板支持 99+；纯样式与模板微调
2025-09-05｜API-CLEANUP｜移除 api.js 未使用的本地通勤估算函数（calculateDistance/estimateCommute/parseCoordinates），消除 ESLint 警告；统一依赖后端 Google Directions
2025-09-05｜DOCS-ALIGN-FINAL｜对齐通勤策略“后端 Google Directions（生产）+ Haversine 回退；前端无本地估算”，去重 systemPatterns，更新 INDEX 与 .clinerules（协作流程第8节）；纯文档与规则，零逻辑改动
2025-09-05｜FILTER-EXPERIENCE-STACK｜V1→V2 参数映射兼容层（开关 enableFilterV2= false 默认关闭）、错误 Toast（快速失败、无本地估算）、URL Query 同步（读写、刷新/直链可复现）、FilterPanel 文案 i18n 抽离（轻量 $t，默认 zh-CN）、postcodes 前端区分 suburbs/postcodes 并透传、mounted 期 propertiesStore 作用域修复、性能埋点（>800ms 警告）；影响文件：src/stores/properties.js / src/components/FilterPanel.vue / src/i18n/index.js / src/main.js｜commit d78d6def
2025-09-05｜UI-FILTER-ENTRY-UNIFY｜PC/移动端统一仅保留“筛选”入口；FilterTabs 隐藏所有下拉，仅作触发器；撤回 SearchBar 移动端“筛选”按钮；HomeView 统一绑定 toggleFullPanel ↔ FilterPanel v-model；保留步长=50、车位 any/1/2/3+、'0'→Any 兼容｜commit 6926962（文件：FilterTabs.vue / SearchBar.vue / HomeView.vue）

## 当前项目运行状态

### 服务状态

- ✅ Vue前端: `http://localhost:5173` - 虚拟DOM + 响应式系统
- ✅ Python后端: `http://localhost:8000` - FastAPI + GraphQL
- ✅ 数据库连接: 正常
- ✅ 后端API密钥: `GOOGLE_MAPS_API_KEY` 已在 `.env` 文件中正确配置 (2025-09-04)
- ✅ **通勤时间计算**: P0/P1 修复已于 2025-09-04 验证通过，前端正确调用后端 API。

---

## 当前无阻塞问题

所有核心功能均按预期运行。

---

## 下一步行动 (Next Action)

1. 用户筛选体验优化，参考 zillow 的桌面PC 端

### 计划中（未来开始，非优先）

1. **[国际化] 引入i18n框架**: 集成 `vue-i18n`，并将 `ProfileView.vue` 和 `PropertyDetail.vue` 中的硬编码中文抽离。
2. **[组件化] 抽象核心组件**: 将 `PropertyCard.vue` 中的按钮、标签等元素抽象为可复用的基础组件。
3. **[样式] 统一设计令牌使用（已完成 2025-09-03）**: 已集中改造 `PropertyDetail.vue`，将关键硬编码颜色/边框/过渡替换为全局 tokens（`var(--color-text-*)`, `var(--color-border-default)` 等），并将页面背景统一为 `var(--color-bg-page)`；全局 `src/style.css` 补齐详情页引用但缺失的设计令牌（如 `--space-*`, `--bg-*`, `--shadow-xs` 等），统一 ≥1200px 下容器宽度与左右 32px 内边距。

---

## 开发提醒

### 代码质量

- **注释规范**: 遵循CODE_COMMENT_RULES.md - 只解释原因，不解释结果
- **文档维护**: 每次主要变更后更新相关 memory-bank 文件
- **API接口**: 参考API_ENDPOINTS.md确认接口格式和字段名称

### 调试套件

- **终端测试**: 使用 `curl` 检查API端点和响应格式
- **浏览器工具**: 使用Vue DevTools检查Pinia状态和组件渲染
- **数据库检查**: 使用postgresql控制台验证查询性能
- **缓存控制**: 测试环境可调用 `/api/cache/invalidate` 进行选择性失效（仅测试/管理员上下文启用）
