# 当前上下文与紧急焦点
最后更新：2025-09-09

今日快照（精简版，≤10行）
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
- [P0] 设计系统第二阶段：应用到 PriceFilterPanel.vue 和 BedroomsFilterPanel.vue（高优先级）
- [P1] 设计系统第二阶段：应用到 AvailabilityFilterPanel.vue 和 MoreFilterPanel.vue
- [P2] 与后端确认家具契约（V1/V2 对齐），据此启用 enableFilterV2 或在 V1 分支添加映射｜溯源：27b9cf6..a84f3ac
- [回归] 多组合验证：区域+价格/卧室+家具；计数与列表 pagination.total 一致

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
