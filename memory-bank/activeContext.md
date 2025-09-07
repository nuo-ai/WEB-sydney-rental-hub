![1757283835886](image/activeContext/1757283835886.png)![1757284076673](image/activeContext/1757284076673.png)# 当前上下文与紧急焦点
最后更新：2025-09-08

今日快照（精简版，≤10行）
- FILTER-MORE-PANEL-PC：新增“更多”分离式面板（furnished/bathrooms_min/parking_min）；FilterTabs 接入；store 按需启用 V2 映射；URL 同步非空；溯源：commit 7535437
- FILTER-DROPDOWN-POSITION-FIX：PC 分离式筛选面板定位异常（左上角 0,0）已修复；策略= FilterTabs 显式坐标 explicitPosition + Dropdown early-return 修正；溯源：commit 63ac851
- UI-EP-SCROLL-NEUTRAL-1：全局/面板滚动指示器中性化已完成；下一步待定：统一“主滚动职责”
- MB-SLIM-B：Memory Bank 采用“保6文件 + 硬阈值”方案；INDEX.md 已废弃占位（保留兼容链接）；activeContext 仅保当日 ≤8–10 行；progress 近30天里程碑单条 ≤3 行
- MB-SLIM-B-APPLY：废弃 INDEX.md（写入指引与溯源）+ 修复 projectbrief.md 标题；溯源：TASK MB-SLIM-B-APPLY
- FILTER-BEDROOMS-PANEL-EXT：卧室面板并入“浴室/车位”，统一“最少 N”语义；PC 宽度 380，面板内不滚动；“应用（N）”实时计数；URL 同步仅非空；溯源：TASK FILTER-BEDROOMS-PANEL-EXT 2025-09-08
- FILTER-PRICE-SIMPLE-380：价格面板极简（仅数字展示 + 双手柄滑轨 + 清除/应用（N））；PC 宽度 380，无内滚；URL 仅写非空；溯源：commit 5e4baf5

- MB-VERIFY-2025-09-08｜全量校验完成；提出 3 处文档对齐提案（无破坏性变更）
服务状态
- 前端 :5173 / 后端 :8000 正常；数据库连接正常；Directions API 配置完好

下一步
- [P0] 无内滚与 380 宽度在多分辨率回归；键盘可达性复测（首控聚焦/Tab/ESC）；后续按需恢复 Studio
- [Policy] 持续执行 MB-SLIM-B（不新增 MB 文件、强制溯源）
