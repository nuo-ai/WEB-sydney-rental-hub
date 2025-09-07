# 项目进展与演进

---

## 当前状态与未来规划

### 已完成的功能
- [X] 列表页“标题区”三段式（面包屑 → H1 → 操作行），390 视口对齐参考站（HomeView.vue）
- [X] 新增 IconSort / IconBell（SVG 组件化，stroke: currentColor；size/aria 可配）
- [X] 全站“焦点可见性基线”EP-GUARDRAIL-FOCUS-GLOBAL：移除 UA 橙框；输入类控件仅在 :focus-visible 时显示中性灰 ring；按钮/链接默认无 ring；Element Plus :focus 统一去除（src/style.css）
- [X] PC 恢复 FilterTabs 为筛选面板入口（仅PC显示；不直接改筛选；HomeView 接线 @requestOpen + v-model）
- [X] 移动端“筛选”药丸改造：IconFilterNarrow（自定义窄 SVG）、尺寸收紧（h=34 / px=12 / font=13 / gap=2）、去 suffix 占位 calc、移动端容器左右 16px、一致右缘对齐（margin-right=3px 补偿）
- [X] 图标系统一致性：彻底弃用 Font Awesome，移动入口用 SVG 组件替代（stroke: currentColor）
- [X] ProfileView 注释解析错误修复与 ESLint 清理（移除未使用变量/导入；不改业务逻辑）

- [X] 搜索内嵌筛选入口（sliders-horizontal 16×16，右距 12px）
- [X] 移动端房源卡片 Full-bleed（贴边但保持高度不变）
- [X] 列表接口 500 修复（移除 cover_image）
- [X] 虚拟滚动性能优化与筛选体验收束（V1→V2 基线）
- [X] FilterPanel 顶部 Location 回显区（chips/移除/清空/空态）+ include_nearby 透传 + i18n 回退修复
- [X] 搜索框内部浅灰标签回显已选区域（未聚焦/未输入/未打开 Overlay 显示；前 2 项 + “+N”）
- [X] 筛选分页参数加固（Pinia currentFilterParams + 显式覆盖 page/page_size，修复“每页仅 1 条/第二页异常”）
- [X] 导航交互统一：hover 橙色、不加粗、不灰底；点击/键盘 focus 无外框（仅导航链接）
- [X] Element Plus 交互灰阶护栏（二轮）：Select/Dropdown/快捷项/清除图标/聚焦态走中性灰；CTA 按钮保留品牌橙

### 下一步规划 (What's left to build)

- [P0/PC] 筛选入口重构：移除 PC “筛选”按钮；保留四分组 Chips（区域/卧室/价格/空出时间）+“更多”收纳高级项；点击仅打开对应面板，不直接改 store；按“筛选入口一致性 v2（PC）”规则实施，可回滚
- [P0/PC] FilterPanel.focusSection：支持接收 section 并滚动/聚焦到分组首控件（配合 Chips 锚点）

- 地图与通勤
  - [X] 放大时保持中心（固定住坐标在屏幕中心范围）
  - [X] 点击“通勤”后呈现路径
  - [X] 地图样式贴近 Google Maps 外观
  - [X] 通勤常用地址：1. 去除非大学的地址；2. 增加悉尼所有的学校地址（如有）；3. 只能选择一所大学，更符合学生单人使用的搜索需求，也防止滥用通勤查询（需先讨论）4. 即便选择地址，也只能选择一个地址；5. 地址没有连通谷歌的地址自动完成，能查到的地址很有限

- [X] 将 “找到xxx 套房源” 移出搜索框的容器，在”搜索框“下方新增一个容器，对齐不变，然后在右面加上“排序“按钮，增加：按最小价格、按空出时间、按最早看房时间、按区域（首字母）排序选项
- [ ] [P0/页面] 我的中心初步改造（收藏/历史两卡 + 统一卡片变体，先结构与样式基线）
- [ ] [P0/快修] 搜索条件保存与恢复（localStorage + URL 优先级）
- [ ] [P0/发布] MVP 部署上线（前端/后端流水线、环境变量、CORS、健康检查、README 指南）
- [ ] [P0/基础] 筛选 UI 升级（先讨论再定方案，产出 1 页 RFC：触发/层级/分组折叠/清空&应用/键盘可达/空态/移动端优先）
- [ ] [P0/基础] Design Tokens 基线统一（focus/btn/input/icon/filter-chip），消除局部硬编码

### 已知问题 (Known Issues)

- [ ] 个别浏览器上地图加载偏慢（需观测与懒加载评估）
- [ ] 表单校验较为基础（需补充边界与可访问性）

### Backlog（P1/记录）

- 列表/卡片一致性
  - [ ] property features 默认显示行数策略；若全部显示则去除“View all features”按钮
  - [ ] 计数器外观统一（与 Pills 模式对齐）
  - [ ] 收藏/转发样式与列表页面统一
  - [ ] 轮播的 dots（指示器）结构与样式统一
- 交互可用性/微动效
  - [ ] 页面上滑时导航栏颤抖与页面自动向上（滚动阈值与 spacer 修正）
  - [ ] 按键点击外框统一为 :focus-visible + token 的 focus ring
- 移动端细节
  - [ ] 移动端轮播箭头垂直居中
  - [ ] 手机端 logo 上下间距（用 token 收敛）
- 视觉与文案
  - [ ] 列表页“New”标签去除
  - [ ] 开放时间颜色调整与多行显示
- 数据与内容
  - [ ] 学校地址缺失（对齐 backend/config/university_data.py 或后端透传字段）

## 关键里程碑

### 2025年9月7日：列表页标题区与全站焦点基线

- 主要成果：
  - HomeView.vue 搜索容器下新增“标题区”：面包屑（弱化灰）→ H1（英文句式，含 suburb/NSW/postcode/total）→ 操作行（左：IconBell + Property alert + Switch Off；右：IconSort + Sort 下拉触发），布局与间距对齐参考站 390 视口。
  - src/style.css 增加 EP-GUARDRAIL-FOCUS-GLOBAL：重置 UA outline；输入类控件在 :focus-visible 显示中性灰 ring（令牌化）；按钮/链接默认不显示 ring；针对导航/标题动作区/卡片可点击项做场景兜底；统一移除 Element Plus :focus outline；提供 .focus-visible-ring 作为少数按钮启用 ring 的开关。
  - 新增 IconSort.vue / IconBell.vue，统一图标系统（stroke: currentColor；size/aria 可配置）。

- 影响与价值：
  - 彻底消除“点击出现橙色焦点框”的反复问题，建立可维护的全站焦点可见性基线；键盘可达性保留在输入类控件上。
  - 标题区信息架构与参考站一致，支持 URL 同步的排序逻辑与后续扩展，UI 一致性和可读性明显提升。

### 2025年9月6日：筛选回显与分页加固（Location 区 + Inline Chips + Pagination Guard）

- 主要成果：
  - FilterPanel 顶部常驻 Location 区，支持 chips 回显/单项移除/清空；清空后显示空态提示，避免用户失去“区域”上下文；include_nearby 勾选写入/恢复 URL；i18n 回退修复（filter.location/clearAll/searchNearby）。
  - 搜索框内部浅灰标签回显所选区域（未聚焦/未输入/未打开 Overlay 时显示；pointer-events: none；前 2 项 + “+N” 汇总），替代早期“品牌色条幅”方案。
  - Pinia 分页参数加固：持久化 currentFilterParams；fetchProperties 合并并显式覆盖 page/page_size；HomeView 入口统一走 applyFilters/resetFilters。修复 page_size=1 泄漏导致“每页仅 1 条/第二页异常”，23 条场景恢复为 20 + 3。
- 影响与价值：
  - 信息连贯：区域选择→筛选面板→应用后分页，心智连续且可复现（URL）。
  - 稳定性：计数请求与列表请求彻底解耦，分页与每页条数与期望一致。
- 溯源：activeContext 2025-09-06｜FILTER-PANEL-LOCATION-SECTION / SEARCHBAR-INLINE-CHIPS / FILTER-PAGINATION-GUARD｜commit 23f186f

### 2025年9月6日：Netlify 部署与构建修复 + 图标库一致化

- 主要成果：
  - 部署：对齐 Netlify 配置（monorepo 子目录构建）— base=vue-frontend、command="npm run build"、publish="dist"，并新增 SPA 重写（/* → /index.html）。
  - 构建修复：删除 PropertyDetailNew.vue 多余的第二个 `<template>`，符合 Vue SFC 单模板规范，解除 Vite 构建失败。
  - 图标库：恢复详情页使用 lucide-vue-next，新增依赖，撤回临时的 Element Plus 图标替换，保持全站视觉一致。
- 影响与价值：
  - 部署链路稳定：推送即构建上线（前提：仓库绑定/分支/Auto publish 正常），SPA 路由直刷不再 404。
  - 代码规范收敛：显式记录 SFC 单模板为“构建红线”，避免类似错误再次发生。
  - 设计一致性：图标系统统一为 lucide-vue-next，便于树摇优化与样式一致。

### 2025年9月6日：导航交互统一 + EP 护栏二轮

- 主要成果：
  - 在 `src/style.css` 末尾新增“导航通用规则”，仅作用于导航容器内链接：hover 橙色（不加粗/不灰底）、focus/click 无外框、图标随 currentColor；覆写导航内 `.el-menu-item:hover` 灰底为透明
  - 强化 Element Plus 交互护栏（二轮）：Select/Dropdown/Cascader/DatePicker/Input 清除/聚焦态走中性灰，CTA 按钮保留品牌橙
- 影响与价值：
  - 品牌色使用聚焦于 CTA，降低页面“橙色噪声”
  - 导航可读性更好；键盘交互在导航处移除外框，其它表单仍保留克制的灰色焦点
- 溯源：activeContext 2025-09-06｜UI-NAV-GLOBAL-RULES / EP-GUARDRAIL-2ND-PASS｜pending commit

### 2025年9月6日：搜索内嵌筛选入口 + 移动端卡片满屏 + 列表接口 500 修复

- 主要成果：
  - 搜索框后缀内嵌“筛选”入口（sliders-horizontal 16×16），右距 12px，点击打开统一 FilterPanel；移除 clearable，避免与后缀排序冲突；令牌化 --search-suffix-right/--search-suffix-hit。
  - 移动端房源卡片 Full-bleed：@media≤767px 设 width/max-width:100vw + 左右 margin: calc(50% - 50vw)，并去圆角 border-radius:0；图片与轮播高度保持 250px。
  - 修复 /api/properties 500：去除不存在的 cover_image 字段（数据库无该列）。
- 影响与价值：
  - 交互一致：筛选入口统一、右侧贴边、可访问性完备；移动端视觉贴边符合沉浸式预期。
  - 稳定性：列表接口恢复 200，分页与筛选功能稳定可用。
- 溯源：activeContext 2025-09-06｜UI-SEARCH-FILTER-SUFFIX / UI-CARD-FULLBLEED-MOBILE / API-LIST-500-FIX｜commit 2deb50c

### 2025年9月5日：图片计数器复刻与 ESLint 清理

- 主要成果：复刻图片计数器 Photos pill（min-width 118px、22×22 徽标、two-digits 胶囊、支持 99+），模板新增 two-digits 动态类以稳定多位数显示；清理 api.js 未使用函数，消除 ESLint no-unused-vars。
- 细节：
  - UI：容器 inline-flex 居中，背景 #fefefe、边框 #cfd1d7、文本 #3c475b、圆角 4px；数字使用 tabular-nums 防抖动；two-digits 时自动胶囊（padding: 0 4px, radius: 11px）。
  - 模板：当 images.length ≥ 10 添加 two-digits 类；99+ 场景显示“99+”。
  - 代码质量：移除 calculateDistance/estimateCommute/parseCoordinates，前端完全依赖后端 Google Directions。
- 影响与价值：保障视觉稳定并与历史“成功过”版本一致；前端通勤实现与后端契约一致，去除误导性本地估算路径。
- 溯源：activeContext 2025-09-05｜UI-PILL-COUNTER / API-CLEANUP

### 2025年9月5日：筛选入口统一（PC/Mobile）与入口回撤

- 主要成果：
  - PC 与移动端统一仅保留“筛选”一个入口。
  - FilterTabs 隐藏所有下拉/预设，仅作为“打开 FilterPanel”的触发器。
  - SearchBar 移动端撤回“筛选”按钮（SearchBar 仅负责搜索）。
  - HomeView 统一绑定 @toggleFullPanel ↔ FilterPanel v-model；移动端也渲染 FilterTabs 作为入口。
- 影响与价值：去除双通道与预设导致的状态不一致；交互对齐 Zillow 触发器模式；心智更简洁、回滚路径清晰。
- 向后兼容：旧直链 `parking=0` 视为 Any（不传）。
- 溯源：activeContext 2025-09-05｜UI-FILTER-ENTRY-UNIFY｜commit 6926962

### 2025年9月5日：筛选兼容与体验收束（V1→V2 基线）

- 主要成果：
  - 参数映射兼容层 + 特性开关 enableFilterV2（默认 off，零风险回滚）
  - 错误策略：快速失败 + 就近 Toast，移除本地估算/静默置 0
  - URL Query 同步：筛选应用→写入 query；onMounted→从 query 恢复（刷新/直链可复现）
  - i18n：FilterPanel 文案抽离到轻量 $t（默认 zh-CN），不引入外部依赖
  - postcodes 支持：前端区分 suburbs/postcodes，URL 与筛选参数双向透传
  - 性能埋点：计数/列表接口 >800ms 输出 [FILTER-PERF] 警告，便于观察 p95
  - 挂载期 bug 修复：propertiesStore 作用域问题导致 mounted 抛错，已通过显式入参与判空兜底修复
- 影响文件：src/stores/properties.js / src/components/FilterPanel.vue / src/i18n/index.js / src/main.js
- 溯源：activeContext 2025-09-05｜FILTER-EXPERIENCE-STACK｜commit d78d6def

### 2025年9月4日：通勤时间计算准确性问题修复

- **主要成果**: 彻底解决了通勤时间计算严重不准的问题。前端现在能够可靠地调用后端API，获取并展示来自Google Maps的真实、准确的通勤数据。
- **根因分析**:
  1. **P0 - API密钥缺失**: 后端 `.env` 文件中缺少 `GOOGLE_MAPS_API_KEY`，导致外部API调用失败。
  2. **P1 - 前端静默降级**: 前端 `api.js` 中存在“测试模式”下的静默降级逻辑，API调用失败时，系统会回退到一套不准确的本地估算算法，从而掩盖了后端错误。
  3. **P-dev - 开发环境缓存**: Vite开发服务器的缓存导致前端代码变更未能及时生效，延长了问题排查时间。
- **关键修复**:
  - **后端**: 在 `.env` 文件中正确配置了 `GOOGLE_MAPS_API_KEY`。
  - **前端**: 删除了 `api.js` 中的 `testMode` 开关、`estimateCommute` 本地估算函数及其相关的所有降级逻辑，确保API调用失败时会抛出明确错误。
- **验证手段**: 通过浏览器网络开发者工具，确认前端页面在计算通勤时间时，发起了对 `/api/directions` 的XHR请求，并收到了状态码为200的成功响应。
- **影响与价值**:
  - **准确性**: 通勤时间从误差高达50%-200%（基于本地估算）提升至与Google Maps官方结果一致。
  - **用户体验**: 用户可以获得可靠的通勤决策依据，显著提升产品信任度。
  - **系统可靠性**: 移除了错误的静默降级，使系统在遇到外部API问题时能够快速失败，便于监控和定位。

### 2025年1月30日：虚拟滚动性能优化
