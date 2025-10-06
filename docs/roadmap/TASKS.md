# 筛选与计数整改路线图（P0/P1 分阶段任务清单）

说明：
- 本路线图用于跟踪“筛选与计数”专项改造。任务均可一键创建为 Issues（Jira/Trello/GitHub）。
- 每个阶段结束后必须进行一次完整回归测试。若出现回归风险，按回滚策略恢复。
- 提交规范：中文 Commit（Conventional Commits），代码注释解释“为什么”，涉及“前端表现”务必在 PR 描述中补充。

目录
- 第一阶段（P0｜低风险，可回滚）
- 第二阶段（P0 收尾与稳定）
- 第三阶段（P1｜中高风险，需评审）
- 附录：测试矩阵（最少覆盖）

最新进展（2025-09-15）
- BE-002 完成：/api/properties 增加查询参数/排序白名单校验；未知键/非法 sort 返回 400（APIResponse 错误体含 unknown_keys/allowed_keys/invalid_values）。保持 V1 行为与口径不变。
- QA-001 最小回归落地并通过：10 passed；覆盖 total 与分页累加一致、排序白名单、未知键 400、listing_id 点名过滤；为避免硬编码，从 /api/locations/all 动态选择 suburb。
- 文档更新：backend/API_ENDPOINTS.md 已对齐白名单与错误体样例，补充 QA-001 运行说明与“前端表现”。

执行记录（溯源）
- BE-002：backend/main.py（/api/properties 白名单）+ backend/API_ENDPOINTS.md（文档）；tools/playwright/tests/api/test_properties_filters.py 覆盖；本地结果 10 passed；最近 commit: 17527a4
- QA-001：核心断言包含“total 与分页累加一致”“排序白名单”“未知键 400”“listing_id 点名过滤”；动态从 /api/locations/all 选择 suburb，避免硬编码
- 关联文件：backend/main.py、backend/API_ENDPOINTS.md、tools/playwright/tests/api/test_properties_filters.py

验收口径（前端表现）
- “应用（N）/确定（N）”不回跳旧值；关闭面板后无“幽灵计数”
- 计数失败降级：返回 null → 按钮退回“应用/确定”，不误显示“0 条”
- 仅选邮编：前端展开为 suburb CSV（V1 兜底），N 与应用后列表总数一致
- URL 幂等：仅写非空有效键，刷新/直链可恢复
- 排序：白名单生效；非法值 400

下一步（建议执行顺序）
1) FE-UI-004（P0）：全分面 URL 幂等自查与修正（仅写非空有效键，“应用后列表 total 对齐”）
2) REL-001（P0）：10% 金丝雀，观察 p95、失败降级率、错误率；异常回滚
3) DOC-001（P0）：一页纸架构与 PR 模板收尾；在仓库根新增 pytest.ini 或在 dev 依赖加入 pytest-timeout 以消除测试超时告警
4) BE-003/FE-STORE-002（P1 预研）：V2 契约与前端映射双轨方案设计与影子流量对比

================================================================================

第一阶段（P0｜本周完成，低风险可回滚）

ID: BE-001
标题: 统一筛选参数构建器（数据/计数共用）
描述:
- 抽象 build_where_and_params(filters) → { whereSql, params }，列表查询与计数共享构建器，仅在 SELECT 级别区分。
- 提供 OR 子句助手，用于 bedrooms/bathrooms/parking 等“多值/下限语义”的安全参数化拼接。
涉及文件:
- backend/crud/properties_crud.py
- backend/main.py（调用改造）
验收标准:
- 同一 filters 下，列表接口 pagination.total 与“预估计数 N”一致（口径统一）。
- 生成 SQL 全部参数化，无动态字符串插值风险。
测试要点:
- V1 契约全键覆盖；空条件、单一条件、多条件组合；邮编/区域组合。
工期估算: 2d
风险: 中（覆盖面广）
回滚: 保留旧路径 behind feature flag，可快速切回。

--------------------------------------------------------------------------------

ID: BE-002
标题: 排序/字段白名单校验与未知过滤键处理
描述:
- sort_direction 仅允许 ASC/DESC；sort 字段限定白名单。
- 未知过滤键直接返回 400（含明确错误信息），提高契约可观测性。
涉及文件:
- backend/crud/properties_crud.py
- backend/main.py
- backend/API_ENDPOINTS.md（文档同步）
验收标准:
- 非法参数被拒绝且记录日志；合法请求不受影响。
测试要点:
- 白名单正/反例；错误码/错误体断言；兼容无 sort 的请求。
工期估算: 0.5d
风险: 低
回滚: 关闭白名单校验开关。

--------------------------------------------------------------------------------

ID: FE-STORE-001
标题: 计数失败可观测化（返回 null，非 0）与缓存兜底
描述:
- stores/properties.js：getFilteredCount/getPreviewCount 失败返回 null，不再返回 0；保留/强化 FILTER-PERF 日志。
- 缺少 areasCache 时先 getAllAreas() 再进行“postcode→suburbs”展开，避免重复远端成本。
前端表现:
- 当 previewCount=null：“应用（N）/确定（N）”退回“应用/确定”，显示轻量错误提示，不刷新列表。
涉及文件:
- vue-frontend/src/stores/properties.js
验收标准:
- 计数失败不再误导为“0 条”；列表不会被误清空；性能日志可追踪失败率。
测试要点:
- 模拟 API 失败；按钮文案降级与轻量提示；不误显示“0 条”。
工期估算: 0.5d
风险: 低
回滚: 恢复旧返回 0（不推荐）。

--------------------------------------------------------------------------------

ID: FE-UI-001
标题: 提取 useFilterPreviewCount 可复用逻辑（并发守卫 + 防抖 + 卸载清理）
描述:
- 新建 composable：useFilterPreviewCount(section, buildDraftFn, options?) → { previewCount, loading, compute, cleanup }
- 统一“更新草稿→标记分组→发起计数→_seq 并发守卫→onUnmounted 清理定时器/状态”。
- 首批接入 PriceFilterPanel.vue、BedroomsFilterPanel.vue（最小 diff 保留前端表现）。
涉及文件:
- vue-frontend/src/composables/useFilterPreviewCount.js（新建）
- vue-frontend/src/components/filter-panels/PriceFilterPanel.vue
- vue-frontend/src/components/filter-panels/BedroomsFilterPanel.vue
验收标准:
- 快速点击不同选项时旧响应不覆盖新状态；组件卸载后不再发请求。
测试要点:
- 并发请求序号守卫；卸载清理；计数失败降级。
工期估算: 1d
风险: 中
回滚: 组件级别撤回到本地实现。

--------------------------------------------------------------------------------

ID: FE-UI-002
标题: 迁移 Availability/More 分面并接入失败降级
描述:
- AvailabilityFilterPanel.vue、MoreFilterPanel.vue 使用 useFilterPreviewCount。
- 当 previewCount=null：禁用依赖 N 的文案，显示“应用/确定”与轻量错误提示。
涉及文件:
- vue-frontend/src/components/filter-panels/AvailabilityFilterPanel.vue
- vue-frontend/src/components/filter-panels/MoreFilterPanel.vue
验收标准:
- 计数口径一致；失败降级表现统一；移动端/PC 一致。
测试要点:
- 日期“交换两端”逻辑；More 的勾选/清除；失败降级。
工期估算: 0.75d
风险: 低
回滚: 撤回到本地实现。

--------------------------------------------------------------------------------

ID: FE-UI-003
标题: AreaFilterPanel 计数节流与请求合并
描述:
- 对 AreasSelector 的 @requestCount 增加 200–300ms 节流或微任务收敛，降低 API 压力。
- 接入 useFilterPreviewCount；保持 selectedLocations 草稿逻辑不变。
涉及文件:
- vue-frontend/src/components/filter-panels/AreaFilterPanel.vue
- vue-frontend/src/components/AreasSelector.vue（若需）
验收标准:
- 频繁选择/移除时计数请求次数显著下降；结果准确；无旧值回写。
测试要点:
- 批量选择/移除的体验与性能；并发守卫生效。
工期估算: 0.75d
风险: 低
回滚: 移除节流/合并策略。

--------------------------------------------------------------------------------

ID: QA-001
标题: 第一阶段回归测试与 Playwright 场景化
描述:
- 覆盖 PC/移动端主用例矩阵（区域/价格/卧室/浴室/车位/日期/家具、URL 恢复、分页/排序、并发、卸载清理、失败降级）。
产出:
- 测试报告与问题清单；必要时修复补丁。
工期估算: 1d
风险: 中
回滚: 按问题清单逐一修复后复测。

--------------------------------------------------------------------------------

ID: DOC-001
标题: 文档与 PR 模板
描述:
- 一页纸架构图（数据流/口径/降级策略） + composable README + PR 检查清单（触达分组/删键/URL/降级/前端表现）。
- 更新 backend/API_ENDPOINTS.md 的错误码与白名单说明。
工期估算: 0.5d
风险: 低

================================================================================

风险与回滚
- 风险：契约误用（未知键/非法 sort）、灰度期间计数失败率上升、URL 幂等遗漏导致条件漂移
- 回滚：关闭白名单校验；恢复旧 UI 参数写入策略；禁用新排序项；必要时回退至上一个稳定 commit

第二阶段（P0 收尾与稳定｜下周前半）

ID: FE-UI-004
标题: 全分面接入与样式/URL 幂等核对
描述:
- 逐一核对各分面 URL 写入/清理仅针对非空有效键；“应用”后列表 total 对齐。
工期估算: 0.5d
风险: 低

--------------------------------------------------------------------------------

ID: REL-001
标题: 金丝雀发布与指标监控
描述:
- 10% 用户灰度，观察 p95、错误率、计数失败率；异常触发回滚。
工期估算: 0.5d
风险: 低

--------------------------------------------------------------------------------

ID: QA-002
标题: 第二轮完整回归
描述:
- 复跑 QA-001；重点覆盖灰度阶段反馈的边缘场景。
工期估算: 0.75d
风险: 中

================================================================================

第三阶段（P1｜中高风险，需评审）

ID: BE-003
标题: V2 契约支持（向后兼容）
描述:
- 支持 suburbs/postcodes/price_min/price_max/bedrooms/bathrooms_min/parking_min/furnished/include_nearby；以 flag 或 API 版本门控。
涉及文件:
- backend/crud/properties_crud.py
- backend/main.py
- backend/API_ENDPOINTS.md
验收标准:
- V1/V2 并行可用；相同语义结果一致；影子流量对比无偏差。
工期估算: 2d
风险: 高
回滚: 关闭 V2 开关。

--------------------------------------------------------------------------------

ID: FE-STORE-002
标题: 切换到 V2 映射并移除 postcode→suburbs 展开
描述:
- enableFilterV2=true；更新 SECTION_KEY_MAP 含 V2 键名；移除前端 postcode 展开逻辑。
涉及文件:
- vue-frontend/src/stores/properties.js 等
工期估算: 1d
风险: 中

--------------------------------------------------------------------------------

ID: NODE-001
标题: 移除 Node 层重复过滤
描述:
- production-server.js 不再做二次过滤/计数，仅转发。
工期估算: 0.5d
风险: 中

--------------------------------------------------------------------------------

ID: BE-004
标题: 可选 /count 端点（仅返回 total）
描述:
- 减少列表字段序列化与网络体积；若后端实现成本可控则落地。
工期估算: 1d
风险: 低

--------------------------------------------------------------------------------

ID: QA-003
标题: P1 影子流量对比 & 完整回归
描述:
- V1/V2 对照；移除 Node 再过滤后的端到端一致性验证。
工期估算: 1.5d
风险: 高

================================================================================

附录：最少测试矩阵（节选）
- 条件覆盖：价格（0/5000/≥/≤/区间）、卧室（0/4+）、浴室（any/3+）、车位（0/2+）、日期（交换两端）、区域（suburb/postcode/混合/仅 postcode）、家具（on/off）
- 形态：PC 分离式、移动端统一面板
- URL：直链恢复/应用后幂等
- 并发：快速切换选项，旧响应不得覆盖新状态（_seq）
- 卸载：关闭面板后不再有残留计时器/请求
- 失败降级：计数失败 -> 按钮文案退回“应用/确定”，轻量错误提示，不刷新列表
- 分页与排序：white-list 有效，非法被拒且记录日志

测试基座配置
- 建议引入 pytest-timeout 或新增 pytest.ini 注册 markers=timeout，设定默认超时，消除 PytestUnknownMarkWarning
- CI 建议：采集 HTML 报告/失败快照/慢用例统计；暴露 p95/失败率指标
