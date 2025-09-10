![1757262958422](image/techContext/1757262958422.png)# 技术上下文 (Technical Context)

**文档状态**: 生存文档 (Living Document)
**最后更新**: 2025-09-10

---

## 1. 当前技术栈

- **前端**: Vue 3 (Composition API) + Vite + Element Plus + Pinia + lucide-vue-next（图标）
- **后端**: Python FastAPI + Strawberry GraphQL + Supabase (AWS悉尼区域)
- **数据库**: PostgreSQL (Supabase) + Redis缓存（默认 15 分钟 TTL；详情端点 /api/properties/{id} 为 30 分钟）
- **地图**: OpenStreetMap（底图）+ 后端 Google Directions（生产）+ Haversine（测试回退）

---

## 2. 项目架构概览

### 项目结构
```
vue-frontend/
├── src/views/          # 页面组件 (Home.vue, PropertyDetail.vue等)
├── src/components/     # 可复用组件 (PropertyCard.vue, Sidebar.vue等)
├── src/stores/         # Pinia状态管理 (properties.js, auth.js)
├── src/services/       # API服务层 (api.js)
├── src/router/         # Vue Router配置
└── vite.config.js      # Vite配置 (CORS代理到localhost:8000)
```

### JUWO品牌设计系统
- **主色**: #FF5824 (橙色)
- **统一圆角**: 6px（组件设计令牌）
- **标准房源卡片**: 580px宽度
- **布局对齐**: 1200px最大宽度，32px间距

### API集成架构
- **代理配置**: 默认将`/api`转发到 `http://localhost:8000`；在 WSL/容器环境可通过环境变量 `VITE_API_TARGET` 切换为 `http://172.31.16.1:8000`
- **拦截器**: 自动携带JWT认证头（按需启用；已具备框架基础）
- **响应格式**: 统一`{status, data, pagination, error}`结构
- **失败策略**: 前端已移除 testMode 与本地估算降级；当后端异常时快速失败并抛错，便于监控定位

---

## 3. 性能优化成果 🎯

**多项性能突破**:

1. **虚拟滚动优化**: DOM节点减少99.8% (17万+ → ~400)，列表加载提升83%
2. **API响应加速**: 服务端响应从8-10秒降至0.4-0.5秒，提升20倍
3. **数据库索引**: 筛选查询从2.2秒降至0.59秒，提升3.7倍
4. **缓存策略**: 15分钟客户端缓存 + Redis降级到内存缓存
5. **数据传输**: API字段优化减少70%响应体积

---

## 4. 开发环境

```bash
# Vue前端开发环境
cd vue-frontend
npm run dev              # localhost:5173

# 后端API服务
cd ../
python scripts/run_backend.py  # localhost:8000
```

**当前运行状态**:
- ✅ Vue前端: 正常运行 (虚拟DOM + 响应式系统)
- ✅ Python后端: 正常运行 (FastAPI + GraphQL)
- ✅ 数据库连接: 正常 (3456条示例数据；会随导入更新)
- ✅ CORS代理: 配置完成
- ✅ 地图服务: OpenStreetMap备选
- ✅ 认证系统: JWT + 邮箱验证框架
- ✅ 通勤计算: 后端 Google Directions（生产）+ Haversine 回退；前端无本地估算

---

## 已解决的技术债务 ✅

**核心问题修复**:
- 用户认证体系完整 (注册/登录/邮箱验证)
- Google Places API完全替代方案 (本地存储/pre设数据)
- Redis依赖降级 (内存缓存备选)
- API响应格式统一 (description字段问题)
- 服务端分页完整迁移
- 代码注释规范建立
- PC 详情页风格一致性：统一背景/容器/内边距；替换硬编码为全局 tokens；在 src/style.css 补齐缺失变量映射

## 样式系统更新（2025-09-03）

- 在 `src/style.css` 的 `:root` 补充变量映射：`--space-1-5`, `--space-3`, `--space-3-5`, `--space-4`, `--space-6`, `--text-xs`, `--text-sm`, `--text-base`, `--text-lg`, `--font-semibold`, `--bg-base`, `--bg-hover`, `--bg-secondary`, `--radius-full`, `--shadow-xs`, `--brand-primary`, `--text-primary`, `--text-tertiary`, `--link-color`，与 JUWO 全局设计系统对齐。
- 在 `PropertyDetail.vue` 统一使用全局 tokens：如 `var(--color-bg-page)`, `var(--color-text-*)`, `var(--color-border-default)`；移除未定义变量（如 `--transition-all`）以避免回退。
- 统一 ≥1200px 与 1920px 断点的容器规范（`max-width: 1200px`, `padding: 0 32px`），与首页 Home 栅格一致，消除“另一套主题”观感。

### PropertyDetail 布局实现摘要
- 选择器基线：.property-detail-page .content-card 及其分区（description-section、map-section 等）
- 断点：
  - ≥1200px：启用 453px 左缘、496px 右缘的主版心计算；容器全宽布局
  - ≥1920px：仅对 .description-section p 应用 max-width: var(--paragraph-measure, 68ch)
- 关键计算：
  - margin-left: calc(453px - var(--section-padding-x, 50px))
  - margin-right: calc(496px - var(--section-padding-x, 50px))
- 分隔线伪元素：left/right = var(--section-padding-x, 50px)，保证与正文内边距对齐
- 不影响区域：Hero 顶部大图、<1200px 移动端布局
- 潜在风险/注意：
  - 若后续修改 --section-padding-x，需同时验证分隔线、标题与卡片边缘是否仍一致
  - 长段落 measure 仅对 p 生效，富文本内其他块级元素（如 ul/ol、表格）如需限制应另行评估

---

## 运行与集成增补（2025-09-06）

- 部署（Netlify）配置
  - netlify.toml：
    - [build] base="vue-frontend"、command="npm run build"、publish="dist"
    - [[redirects]] from="/*" to="/index.html" status=200（SPA 重写）
  - Functions：未使用时保持为空，避免误判为函数项目
  - 环境变量：VITE_GOOGLE_MAPS_API_KEY（限制到 *.netlify.app 与自定义域），可选 VITE_API_BASE_URL、NODE_VERSION（遵循 package.json engines: 20.19.x 或 22.x）
  - 触发：push 到生产分支自动部署；若未触发，检查 Repository 绑定/Branch to deploy/Auto publish/Lock/Ignore/GitHub App 权限；必要时以 Build Hook 兜底


- 搜索框内嵌筛选入口（SearchBar.vue / HomeView.vue）
  - 在 el-input 的 suffix 内嵌 sliders-horizontal SVG（16×16，stroke: currentColor），颜色使用 var(--color-text-secondary) 与搜索 icon 一致；
  - 绝对定位相对 .el-input__wrapper：right: var(--search-suffix-right, 12px); top: 50%; transform: translateY(-50%);
  - wrapper 右侧 padding-right 使用令牌化计算：calc(var(--search-suffix-right, 12px) + var(--search-suffix-hit, 32px))，避免占位符/文本被覆盖；
  - 交互：button 语义 + aria-label="筛选"，点击 emit('openFilterPanel') 打开统一 FilterPanel；移除 clearable；
  - HomeView 监听 openFilterPanel 并隐藏 FilterTabs（v-if=false），维持“筛选入口单一”。

- 移动端房源卡片 full-bleed（PropertyCard.vue）
  - @media (max-width: 767px) 下：width/max-width:100vw；左右 margin: calc(50% - 50vw) 实现贴边；border-radius:0；
  - 高度不变：图片容器与轮播容器保持 250px，object-fit: cover；桌面端不受影响。

- 后端列表接口修复（backend/main.py）
  - 移除 /api/properties 列表查询中的 cover_image 字段（数据库 schema 无此列），解决 500 错误，保证分页/筛选稳定。

- 设计令牌（新增/约定）
  - --search-suffix-right: 12px（后缀右间距）
  - --search-suffix-hit: 32px（后缀命中区域宽高，可收紧为 24–28px）

### 数据库连接与池化（补充）
- 建议：Supabase 使用 PgBouncer “事务池”端口 6543，避免 Session Pool 的 MaxClients 上限阻塞。推荐 .env 示例：
  - DATABASE_URL=postgres://USER:PASSWORD@aws-0-ap-southeast-2.pooler.supabase.com:6543/postgres?sslmode=require
  - DB_POOL_MIN_SIZE=1；DB_POOL_MAX_SIZE=4（可按环境覆盖）
- 连接释放：FastAPI 依赖 get_db_conn_dependency 采用 yield + finally 确保归还；若 _db_pool.getconn() 抛 PoolError，回退直接连接，finally 统一 release_db_connection(conn)。
- 缓存键与 TTL：/api/properties 采用 URL 作为缓存键（cache_key_by_url）并设置 expire=900，彻底隔离计数（page_size=1）与列表缓存；位置统计（suggestions/all/nearby）TTL 同为 900，且查询统一 is_active = TRUE 与 COUNT(DISTINCT listing_id)。

## 运行与集成增补（2025-09-08）

### 分离式下拉定位实现（2025-09-08 修订）
- 组件契约
  - FilterDropdown.vue 新增 props: explicitPosition?: { top: number|string, left: number|string, width?: number|string }。若提供则优先用于定位。
  - updatePosition() early-return 修正：仅当“无 explicitPosition 且无 trigger”时才早退，保证显式坐标生效。
  - watch(explicitPosition, {deep:true})：面板打开时变化即触发 updatePosition。
- 触发与坐标
  - FilterTabs.vue 在 @click 时基于 event.currentTarget 计算显式坐标，存入 reactive positions，并以 :explicit-position 透传。
  - 进行视口边界保护（左右各 10px），width 取 max(rect.width, 280)。
  - 窗口 resize：若有面板打开则重算；≤768px 断点强制关闭。
- 行为与体验
  - 面板稳定定位在触发按钮正下方；滚动/缩放后位置跟随；首开追加 1–2 帧 rAF 轻量确认重算以稳住首帧。
- 回滚路径
  - 移除 explicit-position 绑定即回退到 trigger 测量模式；仍可运行但可能受 ref/布局时序影响出现 0,0。
- 溯源：activeContext 2025-09-08｜FILTER-DROPDOWN-POSITION-FIX

- 新增组件与改造
  - 新增：`src/components/FilterDropdown.vue`（通用下拉容器，teleport 到 body，支持点击外部/ESC 关闭，单例打开）
- 新增：`src/components/filter-panels/AreaFilterPanel.vue`、`BedroomsFilterPanel.vue`、`PriceFilterPanel.vue`、`AvailabilityFilterPanel.vue`（四个分离式专用筛选面板）
- 新增：`src/components/filter-panels/MoreFilterPanel.vue`（PC 高级筛选“更多”面板；仅“应用”时提交；URL 仅写入非空）
- 改造：`src/components/FilterTabs.vue`（PC 分离式下拉，内部管理 activePanel、触发 refs、:modelValue/@update:modelValue 对偶）、`src/views/HomeView.vue`（仅移动端触发统一 FilterPanel；PC 忽略该触发）
- 行为与契约
  - PC 分离式：FilterTabs 内部管理 activePanel（仅允许一个打开）；下拉定位基于触发元素 `getBoundingClientRect()`，`min-width ≥ 触发宽度`，`max-height: calc(100vh - 40px)`，`overscroll-behavior: contain` 防滚动穿透；点击外部/ESC 关闭；当切换至移动端断点（<768px）时强制关闭任何打开面板。
  - Mobile 统一面板：FilterTabs 通过 `emit('requestOpenFullPanel')` 通知父组件；HomeView 在 `windowWidth ≤ 768` 时打开统一 FilterPanel；PC 忽略该触发，避免双通道。
  - 状态与 URL：单一真源仍为 Pinia；面板内编辑仅在“应用”时调用 `applyFilters()` 提交；URL 同步仅持久化“非空参数”，进入页面从 URL 恢复；保持既有 V1→V2 渐进映射与回滚能力。
- ESLint/可维护性
  - 修复 `v-model` 左值（LHS）不合法：统一改为 `:modelValue` + `@update:modelValue`。
  - 清理未使用变量（如 emit/import）；将文案抽至 `computed` 回退，避免 `$t` 未用告警。
- 依赖与回滚
- 无新增依赖；与 Mobile 统一面板并存，按断点切换；若需回退，恢复 FilterTabs 触发统一 FilterPanel 即可。

- Store 与参数映射（补充）
  - 按需启用 V2：当 filters 含 isFurnished/bathrooms/parking/postcodes 等“高级键”时，自动切换 mapFilterStateToApiParams 到 V2 白名单输出（furnished/bathrooms_min/parking_min 等）；否则维持 V1 直传。
  - URL 同步：仅写入非空（例如 isFurnished=1、bathrooms=3+、parking=2+）；翻页与每页大小变化复用 currentFilterParams，保持幂等。
  - 回滚：关闭 enableFilterV2 或去除“更多”面板注册即可恢复旧契约/旧入口。

## 样式系统增补（2025-09-06）

- :root 新增 `--nav-hover-color: var(--juwo-primary)`，统一导航 hover 颜色令牌。
- 在 `src/style.css` 末尾追加“导航通用规则”块，仅作用于导航容器内链接：
  - hover 橙色（不加粗/不灰底）；focus/click 无外框；图标随 `currentColor`。
  - 覆写导航容器内 `.el-menu-item:hover` 灰底为透明，仅改文字颜色。
- Element Plus 交互护栏（二轮）：Select/Dropdown/Cascader/DatePicker/Input 清除/聚焦等交互态统一中性灰，CTA 按钮保留品牌橙；仅样式层，最小 diff。
- 风险与回滚：如误伤带 nav 的非导航容器，可局部覆写或精确选择器限定；整段追加块可整体删除回退。
- 溯源：activeContext 2025-09-06｜UI-NAV-GLOBAL-RULES / EP-GUARDRAIL-2ND-PASS｜pending commit

## 运行与集成增补（2025-09-05）

- 变更文件与路径
  - src/stores/properties.js：引入参数映射层（mapFilterStateToApiParams），统一 applyFilters/getFilteredCount 入参；分页/排序透传；性能埋点
  - src/components/FilterPanel.vue：URL Query 同步（读写）；错误 Toast（ElMessage）；文案 i18n（$t）；suburbs/postcodes 区分；挂载期作用域修复
- src/components/FilterTabs.vue：PC 端启用分离式 Chips + 独立面板（内部管理 activePanel、显式坐标定位）；Mobile 端不渲染，统一走 FilterPanel 入口。为何：PC 需要就地多分组编辑与分离式定位，Mobile 保持单一入口降低拥挤与复杂度。参见 systemPatterns.md：“筛选入口一致性（v2·PC 专用）”与“分离式下拉定位模式”；回滚路径：移除 explicitPosition 或关闭 V2 映射可回退。
  - src/components/SearchBar.vue：撤回移动端“筛选”按钮（仅保留搜索）
  - src/views/HomeView.vue：监听来自 SearchBar 的 openFilterPanel 打开 FilterPanel；FilterTabs 显式隐藏（v-if=false）
  - src/i18n/index.js：轻量 i18n 插件（无依赖），默认 zh-CN，提供 $t 与 inject('t')
  - src/main.js：挂载 i18n（app.use(i18n)）
- 特性开关
  - enableFilterV2 = false（默认关闭，零风险回滚）；开启后输出 V2 契约参数（suburbs/price_min/price_max/bedrooms/...），并可扩展 furnished/bathrooms_min/parking_min/postcodes 等
- URL 状态同步
  - 应用筛选后写入 URL；进入页面时从 URL 恢复（刷新/直链可复现）
  - 仅写入非空参数；写入前做幂等判断，避免 replace 循环
  - 支持 suburbs 与 postcodes 两类 CSV 参数
- 错误处理
  - 快速失败 + 就近 Toast；移除本地估算与静默置 0，所有数据以后端返回为准
- 性能观测
  - fetchProperties / applyFilters / getFilteredCount 超过 800ms 打印 [FILTER-PERF] 警告，用于观察 p95 并驱动后续优化（如轻量 count 端点或索引）
- 其它注意
  - FilterPanel 关闭图标改为内联 SVG，统一走 SVG 路线（后续全站逐步迁移至 lucide-vue-next）

## 分页参数加固与 UI 回显（2025-09-06）

- 背景：计数请求为提速使用 `page_size=1`，曾污染列表请求，出现“总数正确，但每页仅 1 条、第二页异常”的问题。
- Pinia 加固（stores/properties.js）：
  - applyFilters：保存 `currentFilterParams` 前，强制写入 `page=1`、`page_size=this.pageSize`（使用当前每页设置，禁止硬编码）。
  - fetchProperties：合并 `currentFilterParams` 与本次 `paginationParams` 后，显式覆盖：
    ```js
    requestParams.page = paginationParams.page
    requestParams.page_size = paginationParams.page_size
    ```
    以“本次分页”为最高优先级，防止任何历史值（含 1）污染。
  - setCurrentPage / setPageSize：调用 fetchProperties 时显式传 `{ page, page_size }`。
- 入口一致化（HomeView.vue）：
  - `handleLocationSelected` 统一走 `applyFilters({})` 或 `resetFilters()`，不再直接 `fetchProperties(params)`，避免绕开 Store 守卫与统一映射。
- UI 回显：
  - FilterPanel 顶部常驻 Location 区：chips 回显/单项移除/清空；清空后显示空态提示，避免“区域信息消失”；`include_nearby` 勾选常驻，URL 写入/恢复（透传参数，后端未识别时无副作用）；i18n 回退修复（`filter.location/clearAll/searchNearby` 等 key 缺失时使用中文）。
  - 搜索框内部浅灰标签（Inline Chips）：未聚焦/未输入/未打开移动 Overlay 时在输入框内部回显所选区域（前 2 项 + “+N” 汇总）；`pointer-events: none`，仅占位回显，不拦截交互。

## 样式与设计令牌护栏增强（2025-09-10）
- 目的：阻止新增硬编码颜色，强制使用 CSS 自定义属性 Design Tokens；在未安装 stylelint 的环境下不阻断提交（条件执行）。
- 新增脚本（vue-frontend/package.json）
  - "lint:style": "stylelint \"src/**/*.{css,vue}\" --fix"
- 提交钩子（scripts/git-hooks/pre-commit 摘要）
  ```bash
  if [ -x "vue-frontend/node_modules/.bin/stylelint" ]; then
    (cd vue-frontend && npm run -s lint:style)
  fi
  ```
  - 中文注释：仅当本地已安装 stylelint 时执行，以兼容干净环境；不影响其他语言栈的 pre-commit 流水线。
- Stylelint 规则（.stylelintrc.json 摘要）
  - 禁止十六进制/命名色/rgba/hsla；
  - 启用 plugin/declaration-use-variable 强制 color/background/border/outline/fill/stroke 使用 var(--*)；
  - 豁免：src/styles/design-tokens.css 与 src/style.css（令牌定义入口）。
- 合规范围扩展（本轮）
  - FilterTabs：chip 背景/hover/选中统一 --chip-bg / --chip-bg-hover / --chip-bg-selected（移除 hex fallback）。
  - PropertyCard：轮播箭头颜色使用 var(--color-text-inverse)，保证深底可读与主题可控。
  - PropertyDetail：容器/分隔/弱底/占位/地图容器等统一为 --color-bg-card / --color-border-default / --bg-hover / --surface-*；主/副文案统一 --color-text-primary/secondary。
- 主题映射
  - --juwo-primary / --link-color 对齐纯正蓝（#0057ff / hover #0047e5 / active #0036b3）；品牌色仅用于 CTA/链接，其他交互使用中性灰令牌。
- 回滚与例外
  - 发生误拦截时，优先在局部以更具体选择器限定；极端情况下可短期使用 var(--token, #xxx) 兜底，但需在下一轮清理。
  - 关闭钩子或移除脚本不影响生产构建；规则变更以 .stylelintrc.json 为准。
- 溯源：commit 9984dff..0b6e146｜progress 2025-09-10
