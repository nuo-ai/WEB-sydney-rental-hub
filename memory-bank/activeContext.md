# 当前上下文与紧急焦点
最后更新：2025-09-08

今日快照（精简版，≤10行）
- REGION-FILTER-P0-FIX：区域筛选彻底修复（V1 契约）。当仅选择“邮编”时，自动展开为其下属多个 suburb 并注入 suburb CSV；计数(getFilteredCount)与列表(applyFilters)口径一致；本地区域目录聚合 postcode.suburbs 作为兜底。溯源：commit a331c69..27b9cf6
- FURNISHED-FILTER-FIX-V1：前端改为直接传 isFurnished=true（容错 true/'1'/1/'true'/'yes'），与后端 /api/properties 接口契约一致（SQL 基于 is_furnished yes/no/unknown）；添加 FILTER-DEBUG 输出以核对最终请求参数；ESLint 清理完毕。溯源：commit bade186（范围 48bad16..bade186）
- PREVIEW-DRAFT-UNIFY-DONE：Area/Bedrooms/Price/Availability/More 五个面板全部接入全局 previewDraft + getPreviewCount，清除/应用时清理分组草稿，确保“应用（N）”与列表总数统一口径。溯源：bade186
- FIX-FILTERS-COUNT-P0：禁用“按需 V2 映射”，统一走 V1 契约；V1 分支移除 isFurnished，避免后端不识别导致计数暴涨；计数与列表一致性恢复。溯源：commit 48bad16（范围 9627f69..48bad16）
- MORE-PANEL-SIMPLIFY：仅保“带家具”开关；接入计数器（300ms 防抖）；按钮“清除/应用（N）”；aria-live 播报；URL 仅在 true 时写 isFurnished=1（保持“仅非空参数”）。溯源：48bad16
- DROPDOWN-A11Y-TRAP：FilterDropdown 加固（锁定 body 滚动、Esc 关闭、Tab/Shift+Tab 焦点陷阱、关闭后焦点还原至触发器、首控聚焦）。溯源：48bad16
- AREA/MORE：面板关闭按钮 tabindex="-1"，避免首焦点误落在关闭按钮。溯源：48bad16
- V2 映射：保留白名单透传与 suburb→suburbs 兜底，但默认不开启（enableFilterV2=false）；待后端契约（furnished/布尔取值）对齐后再启用。溯源：48bad16
- FILTER-TABS 定位：explicitPosition + early-return 修正已稳定（无 0,0 回归）。溯源：63ac851
- PC 面板统一宽 380、内部不滚动目标维持（价格/卧室面板已对齐）。溯源：9627f697 等
- URL 同步：仅写入非空；分页参数守卫生效（防 page_size=1 串扰）。溯源：既有策略

服务状态
- 前端 :5173 / 后端 :8000 正常；数据库连接正常；Directions API 配置完好

下一步
- [P0] 与后端确认家具契约：V1 键名/取值（如 is_furnished=1）或 V2（furnished=1/true）；据此启用 enableFilterV2 或在 V1 分支添加映射
- [回归] 多组合验证：区域+价格/卧室+家具；计数与列表 pagination.total 一致
