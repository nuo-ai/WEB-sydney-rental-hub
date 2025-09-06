# 当前上下文与紧急焦点

**最后更新**: 2025-09-06

---
 
2025-09-06｜UI-NAV-GLOBAL-RULES｜src/style.css 追加“导航通用规则”：hover 橙色（#FF5824）不加粗/不灰底；focus/click 无外框；图标随 currentColor；作用范围限定于导航容器；覆写导航内 .el-menu-item:hover 灰底为透明｜pending commit
2025-09-06｜EP-GUARDRAIL-2ND-PASS｜Element Plus 交互灰阶护栏（二轮）：Select/Dropdown/Cascader/DatePicker/Input 清除/聚焦态统一中性灰，CTA 仍用品牌橙；仅样式层覆盖，最小 diff｜pending commit
2025-09-06｜LIST-PAGE-SPLIT-PLAN｜列表页拆分路线：P0 新增 ResultsSummary/PaginationBar/SearchHeader；P1 抽象 PropertiesListContainer；P2 预留 Grid 两栏（列表+地图）开关；不改行为，易回滚｜plan

 
2025-09-06｜DB-POOL-6543｜techContext 增补：事务池 6543 / cache_key_by_url / TTL=900；准备 backend/.env.example 事务池示例；QA：清缓存或15分钟后核对地区统计｜待提交
2025-09-06｜DOCS-ALIGN｜统一筛选入口=SearchBar 后缀；FilterTabs 标注弃用（仅文档调整，无代码改动）｜待提交
2025-09-06｜FILTER-PANEL-LOCATION-SECTION｜FilterPanel 顶部常驻 Location 区，chips 回显/移除/清空；空态提示避免清空后“区域信息消失”；include_nearby 勾选（URL include_nearby=1/0 透传）；i18n 回退修复（filter.location/clearAll/searchNearby 等）；事件名统一 open-filter-panel（同时兼容 camelCase）｜commit 23f186f
2025-09-06｜SEARCHBAR-INLINE-CHIPS｜搜索框内部浅灰 chip 占位回显所选区域（未聚焦/未输入/未打开 Overlay 时显示；pointer-events:none，不改变交互；前 2 项 +“+N” 汇总）｜commit 23f186f
2025-09-06｜FILTER-PAGINATION-GUARD｜Pinia：持久化 currentFilterParams；fetchProperties 合并并显式覆盖 page/page_size；HomeView.handleLocationSelected 统一走 applyFilters/resetFilters；修复 page_size=1 泄漏导致“每页仅 1 条/第二页异常”，23 条场景分页恢复为 20+3｜commit 23f186f
2025-09-06｜UI-SEARCH-FILTER-SUFFIX｜SearchBar 在 el-input 内嵌 sliders-horizontal 16×16，右距 12px；相对 .el-input__wrapper 绝对定位；令牌化 --search-suffix-right=12px、--search-suffix-hit=32px；移除 clearable；HomeView 隐藏 FilterTabs，监听 openFilterPanel｜commit 2deb50c
2025-09-06｜UI-CARD-FULLBLEED-MOBILE｜移动端房源卡片 @media≤767px：width/max-width:100vw；左右 margin: calc(50% - 50vw) 实现 full-bleed；border-radius:0；图片/轮播高度 250px 不变｜commit 2deb50c
2025-09-06｜API-LIST-500-FIX｜移除 /api/properties SELECT 中 cover_image（数据库无此列），修复 500｜commit 2deb50c
2025-09-06｜DEPLOY-NETLIFY-CONFIG｜netlify.toml 对齐 monorepo：base=vue-frontend；command="npm run build"；publish="dist"；新增 SPA 重写（/* → /index.html）｜commit f375181..b227da3
2025-09-06｜BUILD-FIX-SFC｜修复 PropertyDetailNew.vue 存在第二个 <template> 导致 Vite 构建失败；删除冗余模板块，保持单模板规范｜commit f375181..b227da3
2025-09-06｜UI-ICON-LIB｜恢复详情页 lucide-vue-next 图标库，新增依赖；移除临时 Element Plus 图标替换，维持全站图标一致性｜commit f375181..b227da3

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
