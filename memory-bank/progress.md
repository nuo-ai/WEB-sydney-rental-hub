# 项目进展与演进（精简版）

说明
- 仅保近 30 天里程碑（每条 ≤3 行）；超过 30 天仅保“标题 + 溯源”。
- 详细过程请查看对应 commit/PR；Memory Bank 不再复制过程性细节。

近 30 天里程碑
- 2025-09-08｜MB-SLIM-B-APPLY  
  废弃 INDEX.md（保留占位与指引）；修复 projectbrief.md 标题；activeContext 记录溯源 TASK MB-SLIM-B-APPLY
- 2025-09-08｜FILTER-DROPDOWN-POSITION-FIX  
  修复 PC 分离式下拉定位落到左上角问题；Tabs 传 explicitPosition + Dropdown early-return 修正；溯源：commit 63ac851
- 2025-09-08｜UI-EP-SCROLL-NEUTRAL-1  
  统一全站/面板滚动指示器为中性灰；降低视觉噪声；下一步：统一“主滚动职责”
- 2025-09-07｜TITLE-AREA & FOCUS-GUARDRAIL  
  列表页标题区重构；src/style.css 增加可见性护栏（:focus-visible 基线）；提升一致性与可达性
- 2025-09-06｜FILTER-PANEL-LOCATION + PAGINATION-GUARD  
  Location 回显；分页参数加固（计数/列表彻底解耦，URL 同步）；修复“每页仅 1 条/第二页异常”
- 2025-09-06｜DEPLOY-NETLIFY-CONFIG + SFC-REDLINE  
  Netlify 配置对齐（SPA 200 重写）；修复 SFC 双 template 构建红线；图标库统一 lucide-vue-next
- 2025-09-06｜UI-NAV-GLOBAL-RULES  
  导航 hover 橙色、无灰底；EP 交互灰阶护栏（二轮）
- 2025-09-05｜FILTER-EXPERIENCE-STACK  
  V1→V2 兼容层、URL 同步、错误策略与性能观测（>800ms 报警）
- 2025-09-05｜UI-PILL-COUNTER  
  图片计数器复刻（稳定 1/2 位/99+）；清理无用代码
- 2025-09-05｜UI-FILTER-ENTRY-UNIFY  
  统一筛选入口；SearchBar 撤移动端“筛选”按钮；FilterTabs 作为入口
- 2025-09-04｜COMMUTE-ACCURACY-FIX  
  Directions API 配置；前端移除本地估算与静默降级；通勤时间与 Google 对齐

> 30 天仅标题
- 2025-01-30｜VIRTUAL-SCROLL-OPTIMIZATION（溯源：历史 commit/PR）
