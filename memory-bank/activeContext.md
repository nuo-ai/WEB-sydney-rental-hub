# 当前上下文与紧急焦点
最后更新：2025-09-10

今日快照（精简版，≤10行）
- FILTER-PANELS-HOVER-NEUTRAL：AreaFilterPanel 优先完成 chips/按钮 hover/focus 中性化（--chip-bg/--chip-bg-hover/--color-border-*），清理散点 hex；与 FilterTabs 统一。前端表现：面板交互反馈一致，无彩色跳变。溯源：commit 0b6e146..806d3a3
- SEARCH-ENTRY-CHIPS-TOKENIZED：SearchBar 内嵌/回显标签去除 var(--*, #hex) 兜底，统一 --chip-* 与 --color-text-*；移动端 active 改 --bg-hover。前端表现：搜索入口与筛选标签完全同源。溯源：commit 0b6e146..806d3a3
- DETAIL-DIVIDER-TOKEN：PropertyDetail 统一 --divider-color → var(--color-border-default)，移除品牌色/分隔线兜底。前端表现：详情页线条全中性灰，CTA/链接保留品牌蓝。溯源：commit 0b6e146..806d3a3
- OVERLAY+NAME-MODAL：SearchOverlay 去除品牌/文字兜底；NameLocationModal“跳过”改为 --juwo-primary（去旧红）。前端表现：移动覆盖层与 CTA 色域一致。溯源：commit 0b6e146..806d3a3
- DESIGN-TOKENS-COMPLIANCE-SPRINT：PropertyDetail 二/三批全面令牌化（卡片/容器背景、分隔线、弱底 hover、占位与地图容器等），主/副文案统一 --color-text-primary/secondary，交互弱底用 --bg-hover，容器/边框用 --color-bg-card/--color-border-default。前端表现：详情页视觉与交互反馈一致、中性化，品牌色仅用于 CTA/链接。溯源：commit 9984dff..0b6e146
- FILTERTABS-FALLBACK-REMOVAL：移除 Chip 类样式 var(--chip-*, #hex) 的十六进制兜底，统一使用 --chip-bg/--chip-bg-hover/--chip-bg-selected。前端表现：筛选标签在不同主题/深浅底下表现一致，不再出现遗留浅绿/米色。溯源：commit 9984dff..0b6e146
- GUARDRAIL-STYLELINT+HOOK：新增 npm script "lint:style" 与 pre-commit 条件执行 stylelint（存在即运行），配合 .stylelintrc.json 禁止 hex/rgb/hsla/命名色并强制 var(--*)；design-tokens.css、style.css 保持豁免。前端表现：新/改代码禁止硬编码颜色，设计令牌落地有保障。溯源：commit 9984dff..0b6e146
- ADD-LOCATION-UNI-ZH：AddLocationModal/NameLocationModal 接入 i18n；大学名称中文映射（USYD/UNSW/UTS 等，校区括注保留英文），地址 formatted_address 保持英文；热门与选择回传 name=中文、address=英文；修复告警分支。前端表现：添加地址流程中文化，大学中文名 + 英文地址。溯源：commit ee6e006..9984dff
- COMMUTE-I18N-TYPO：CommuteTimes/TransportModes/LocationCard 接入 $t 与 .typo-*；统一空状态/按钮/提示文案；ElMessage/ElMessageBox 使用 t()。前端表现：通勤页中文化一致、文字节奏与详情页对齐。溯源：commit 43f943e..ee6e006
- TYPOGRAPHY+I18N-V1：新增 typography.css（基础/语义文字令牌与 .typo-* 工具类）；扩展轻量 i18n（locales/zh-CN.js + 合并策略）；PropertyCard 首批接入 $t 与 .typo-*（价格/单位/标签/菜单/辅助）。前端表现：UI 中文化，文字节奏统一，动态地址仍英文。溯源：commit 3e4ea72..c45d86a
- UI-COLOR-BLUE-NEW-BADGE & ADD-LOCATION-SECONDARY：PropertyCard“New”徽标改为品牌蓝 var(--brand-primary)，文字用 var(--color-text-inverse)；CommuteTimes“Add location”按钮硬编码红替换为次要按钮令牌（secondary），补充 hover/focus 可达性。前端表现：新标签为蓝色、按钮中性灰一致化。溯源：commit 3c7c150..3e4ea72
- UI-TOKENS-PC-FILTER-LOCATION：PC 分离式筛选标签与 Add/Name Location 弹窗全面令牌化；FilterTabs 激活态→中性选中底；弹窗头部/输入/列表 hover/active 改中性令牌；价格滑块清理硬编码，统一走 tokens。前端表现：点击“卧室/价格/更多”与弹窗流程不再出现旧色。溯源：commit 82c3f37..3c7c150
- LINT-GUARDRAIL-COLOR：stylelint 扩展拦截 background/border/outline/fill/stroke 的硬编码色与 rgba/hsla，强制使用 var(--*)；保留 design-tokens.css 与 style.css 的定义豁免。目的：杜绝新增页面颜色硬编码回归。溯源：commit 82c3f37..3c7c150
- DESIGN-TOKEN-COLOR-3：新增全局语义色令牌集（link visited/disabled、success/warn/danger/info soft-bg/border、favorite 三态、badge、divider、inverse/弱底/brand 别名）；首批等价替换：建议项边框/悬浮、次要文案、筛选按钮激活态统一 tokens。前端表现：自动补全 hover/分隔线中性化，卡片副文为次级灰，筛选激活为中性选中底色。溯源：commit ff73605..69c3e0e
- DESIGN-TOKEN-FAVORITE-P0：收藏按钮与 PropertyCard 颜色 Token 化，未收藏=中性灰，hover=中性加深，已收藏=品牌蓝；卡片地址/副文案/分隔线/规格/操作按钮/图片计数器等硬编码改 Token；叠加遮罩改 overlay 令牌。溯源：commit ff73605
- THEME-BRAND-BLUE-PURE：品牌主色切换为纯正蓝 #0057ff（hover #0047e5 / active #0036b3），令牌映射 --juwo-primary/--link-color 等已对齐；前端表现：主按钮/导航 hover/文本链接统一蓝色系，页面结构与焦点仍为中性灰；向后兼容，可回滚。溯源：commit d7ac639..1f0b27e
- PC-MOBILE-FILTER-OPTIONS-UNIFY：统一 PC 端与移动端浴室和车位筛选选项。修改 BedroomsFilterPanel.vue 中 bathroomOptions 添加 'any' 选项，parkingOptions 将 '0' 替换为 'any' 并将 '2+' 改为 '3+'，与移动端 FilterPanel.vue 保持一致。前端表现：PC 端浴室和车位选项现与移动端完全统一，提升用户体验一致性。溯源：commit 04bd237
- INSPECTION-TIME-NAN-FIX：修复房源列表卡片显示"开放时间：NaN"问题。新增 hasValidInspectionTime 计算属性严格验证数据有效性，增强 formatInspectionTime 函数添加输入验证，更新模板条件渲染。前端表现：无有效看房时间时完全隐藏开放时间模块，与详情页修复保持一致。溯源：commit 7ff2e6c
- SUPABASE-DATA-SYNC-P0：修复 Supabase 同步滞后与邮编小数点；ETL 扩展更新判定（available_date/inspection_times/postcode/property_headline），统一 postcode 4位字符串；前端表现：看房时间/空出日期与CSV一致，“NSW 2010.0”→“NSW 2010”。溯源：commit 53ff509..1b96baa
- REGION-FILTER-P0-FIX：区域筛选彻底修复（V1 契约）。当仅选择“邮编”时，自动展开为其下属多个 suburb 并注入 suburb CSV；计数(getFilteredCount)与列表(applyFilters)口径一致；本地区域目录聚合 postcode.suburbs 作为兜底。溯源：commit a331c69..27b9cf6
- FURNISHED-FILTER-FIX-V1：前端改为直接传 isFurnished=true（容错 true/'1'/1/'true'/'yes'），与后端 /api/properties 接口契约一致（SQL 基于 is_furnished yes/no/unknown）；添加 FILTER-DEBUG 输出以核对最终请求参数；ESLint 清理完毕。溯源：commit bade186（范围 48bad16..bade186）
- PREVIEW-DRAFT-UNIFY-DONE：Area/Bedrooms/Price/Availability/More 五个面板全部接入全局 previewDraft + getPreviewCount，清除/应用时清理分组草稿，确保“应用（N）”与列表总数统一口径。溯源：bade186
- FIX-FILTERS-COUNT-P0：禁用“按需 V2 映射”，统一走 V1 契约；V1 分支移除 isFurnished，避免后端不识别导致计数暴涨；计数与列表一致性恢复。溯源：commit 48bad16（范围 9627f69..48bad16）
- MORE-PANEL-SIMPLIFY：仅保“带家具”开关；接入计数器（300ms 防抖）；按钮“清除/应用（N）”；aria-live 播报；URL 仅在 true 时写 isFurnished=1（保持“仅非空参数”）。溯源：48bad16
- DROPDOWN-A11Y-TRAP：FilterDropdown 加固（锁定 body 滚动、Esc 关闭、Tab/Shift+Tab 焦点陷阱、关闭后焦点还原至触发器、首控聚焦）。溯源：48bad16
- AREA/MORE：面板关闭按钮 tabindex="-1"，避免首焦点误落在关闭按钮。溯源：48bad16
- V2 映射：保留白名单透传与 suburb→suburbs 兜底，但默认不开启（enableFilterV2=false）；待后端契约（furnished/布尔取值）对齐后再启用。溯源：48bad16
- FILTER-TABS 定位：explicitPosition + early-return 修正已稳定（无 0,0 回归）。溯源：63ac851

服务状态
- 前端 :5173 / 后端 :8000 正常；数据库连接正常；Directions API 配置完好

下一步
- [P0] 详情页 PropertyDetail* 全量颜色令牌化：去除 #f5f5f5/#e5e5e5/#007bff/#ff5722 等散点；引入 info/warning/danger-soft 令牌统一反馈弱底/边框。
- [P1] 通勤/对比等组件残留令牌化：CommuteCalculator.vue / CompareToolbar.vue / commute/LocationCard.vue 等（hover/active/标签色族）。
- [P2] 渐进移除 var(--token, #xxx) fallback；新组件模板要求 icon 用 currentColor + 外层 class 控制颜色。
- [Guard] CI 验证 stylelint 新规则拦截效果；新增页面 PR 提示必须使用设计令牌。

最新完成
- 2025-09-08｜SORT-P0
  列表排序功能落地：后端 /api/properties 支持 sort 白名单（price_asc/available_date_asc/suburb_az/inspection_earliest；inspection_earliest 暂等价 available_date_asc），稳定次序 listing_id ASC；前端 fetchProperties 统一兜底跨页保留排序。溯源：commit 7bd269b..54ba6c1
- 2025-09-08｜MOBILE-SEARCH-DIRECT-FILTER
  移动端搜索框直连筛选面板功能完成：移除中间 SearchOverlay 步骤，点击搜索框直接打开筛选面板；优化可访问性（aria-label/role 区分移动/桌面角色）；添加移动端点击反馈效果；保留内嵌标签回显；移除未使用变量，ESLint 合规。用户体验更直接高效｜溯源：commit 7bd269b
- 2025-09-08｜SEARCH-OVERLAY-COMPONENT-REFACTOR
  SearchOverlay 组件化重构完成：使用 BaseChip/BaseListItem 替换自定义样式，彻底移除 location 图标（MapPin/Hash），与筛选面板风格完全统一。清理冗余样式代码，保留容器布局与特有功能（光标动画/徽标），ESLint 合规。用户验收通过｜溯源：SearchOverlay 组件化任务
- 2025-09-08｜MOBILE-FILTER-PANEL-OPTIMIZATION
  移动端筛选面板细节优化完成：全面迁移到设计令牌系统，优化触摸目标尺寸(44px+)，添加滚动锁定防穿透，完善键盘导航(ESC关闭)，增强可访问性支持(focus-visible)，优化iOS安全区适配。所有样式统一使用filter-*设计令牌，移动端按钮最小48px触摸目标，底部按钮52px。用户验收通过｜溯源：移动端筛选面板优化任务
- 2025-09-08｜DESIGN-SYSTEM-COMPLETE
  设计系统全面完成：阶段1-创建设计令牌文件与基础组件；阶段2-应用到所有筛选面板(Price/Bedrooms/Availability/More)；阶段3-创建组件库文档。所有筛选面板现已遵循统一的现代化设计标准，使用中性灰色调、微妙圆角、一致间距系统｜溯源：设计系统实施任务
