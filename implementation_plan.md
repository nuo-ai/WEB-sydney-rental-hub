# Implementation Plan (Furnishing Semantics Fix)

TODOs（按执行顺序，一次只做一小步）
- [ ] DB 迁移（事务化）
  - [ ] 审阅/完善 migration：database/migrations/2025-09-13-fix-feature-booleans.sql（删除特征列历史 CHECK；统一特征列为 BOOLEAN）
  - [ ] 在开发库执行迁移（失败即回滚），确认所有特征列类型为 BOOLEAN（TRUE/FALSE/NULL）
- [ ] ETL 集中判定（加开关，默认启用）
  - [ ] 在 database/process_csv.py 新增函数：derive_is_furnished(row)（否定优先/模糊为未知/冲突为未知/肯定最后）
  - [ ] 新增 load_overrides()/apply_overrides()，支持 database/furnishing_overrides.json 单条热修
  - [ ] 在 clean_data() 接入集中判定与 overrides，最终 is_furnished 仅产出 True/False/None
  - [ ] 增加特征开关 USE_ETL_FURNISHED（默认 true），出现异常可一键关闭回退旧逻辑
- [ ] 重跑 ETL（开发一次跑完）
  - [ ] C:\Python313\python.exe scripts\automated_data_update_with_notifications.py --run-once
- [ ] 清缓存（避免旧数据干扰前端表现）
  - [ ] POST /api/cache/invalidate?invalidate_all=true
  - [ ] 可选：POST /api/cache/invalidate?property_id=17580846
- [ ] 验收（前端表现）
  - [ ] 详情：GET /api/properties/17580846 → is_furnished 为 true/false/null（非 'yes'/'no'）
  - [ ] 点名筛选：/api/properties?listing_id=17580846&isFurnished=true&page=1&page_size=1 → 若非有家具应为空
  - [ ] 全量：勾选“有家具”后列表显著收敛（目标≈33，以本批 CSV 为准）
- [ ] （可选）Verification SQL 增强
  - [ ] 在 database/verification_queries.sql 增加：异常值计数/分布统计/关键词一致性抽检
- [ ] 文档与记录
  - [ ] 在 reports/feature-boolean-normalization.md 记录执行步骤、结果截图/计数、fallout 与改进
- [ ] 第二阶段（可选、灰度）Crawler Minimal Changes（不判定，仅瘦身输出）
  - [ ] rent_pw/bond 输出为整数（不带小数）
  - [ ] available_date 不做“自动改 Available now”，只抄页面原文（若页面为 Available now 则保留）
  - [ ] 删除 is_furnished、has_*、image_1..4 等“结论/冗余列”；保留 images 阵列、features_raw/furnishing_status_raw 等证据
  - [ ] 增加 schema_version（如 crawler.v2）、scraped_at；ETL 双格式兼容，稳定后去旧分支
- [ ] 准备中文 Commit Message（验收 ok 后给出）

---

[Overview]
目标：在不破坏现有工作流的前提下，修复“有家具（前端表现：勾选后仅显示带家具）”的筛选准确性。重心放在 ETL 与数据库：统一特征列为 BOOLEAN、把“是否带家具”的判断集中到 ETL（爬虫只爬不判），并提供最小风险的爬虫“小补丁”以保持“原貌采集”。

范围与思路
- 第一阶段（最小侵入、可回滚）：不改爬虫逻辑、不删字段；数据库去除拦路的旧 CHECK 并统一 BOOLEAN；ETL 新增“否定优先/模糊为未知/冲突为未知/肯定最后”的推断逻辑（可一键开关），清缓存后验收。前端表现：勾选“有家具”仅返回 TRUE；17580846 若无家具则不再出现。
- 第二阶段（可选、灰度）：对爬虫输出“瘦身”，只保留“最少可用字段 + 证据（evidence）”，不输出任何布尔特征结论；ETL 继续负责判定。全程版本化、向后兼容。

[Types]  
数据库层统一特征列为 BOOLEAN（TRUE/FALSE/NULL），NULL 表示未知/不确定；移除历史 CHECK 限制，避免 ETL 回滚。
- 白名单列：has_air_conditioning, has_balcony, has_dishwasher, has_laundry, has_built_in_wardrobe, has_gym, has_pool, has_parking, allows_pets, has_security_system, has_storage, has_study_room, has_garden, has_gas_cooking, has_heating, has_intercom, has_lift, has_garbage_disposal, has_city_view, has_water_view, is_furnished
- 映射规则：('t','true','yes','1')→TRUE；('f','false','no','0')→FALSE；其余→NULL
- 可选：新增 JSONB 字段 is_furnished_evidence（保存 ETL 的判定依据，便于审计与回放），本阶段可不加。

[Files]
- New
  - database/migrations/2025-09-13-fix-feature-booleans.sql
    - 删除“仅与特征列相关”的历史 CHECK
    - 将白名单特征列 ALTER TYPE→BOOLEAN（USING CASE 按映射规则）
  - reports/feature-boolean-normalization.md
    - 执行顺序、缓存失效方法、API/SQL 验收清单、失败排查（重点说明：冲突→NULL 策略）
- Modify
  - database/process_csv.py
    - clean_data()：接入“集中判定”结果写库（新开关控制）
    - New: derive_is_furnished(row) 依据 title/description/features/furnishing_status 进行判定
    - New: load_overrides()/apply_overrides() 支持单条热修（开发期方便点名校准）
  - database/verification_queries.sql（可选增强）
    - 异常值统计、分布统计、关键词一致性抽检 SQL

[Functions]
- New（database/process_csv.py）
  - derive_is_furnished(row: pandas.Series) -> Optional[bool]
    - 优先级：否定 > 模糊/条件 > 肯定；冲突→None；无证据→None
    - 否定：unfurnished|no furniture|without furniture|不带家具 → FALSE
    - 模糊/条件：partly/partial/semi‑furnished|optional|can be furnished|部分带家具/可配 → NULL
    - 肯定：fully furnished|furnished|带家具（且未命中否定/模糊）→ TRUE
    - 仅将 title/description/features/furnishing_status 作为证据；“内置/固定装置/公共配套”（A/C、balcony、gym、dishwasher、built‑in 等）不得当家具
  - load_overrides(path="database/furnishing_overrides.json") -> Dict[int, Optional[bool]]
  - apply_overrides(listing_id: int, inferred: Optional[bool], overrides: Dict) -> Optional[bool]
- Modified
  - clean_data(df)：最终 is_furnished = apply_overrides(listing_id, derive_is_furnished(row), overrides)；只产出 True/False/None

[Classes]
- 无新增/修改/删除（函数化实现即可）。

[Dependencies]
- 无新增三方依赖；正则与 JSON 读取使用标准库。数据库操作沿用现有 psycopg2；迁移使用纯 SQL。

[Testing]
- API（前端表现）
  - 详情：GET /api/properties/17580846 → "is_furnished": true/false/null（不出现 'yes'/'no' 字符串）
  - 点名筛选：/api/properties?listing_id=17580846&isFurnished=true&page=1&page_size=1 → 若非有家具，应返回空
  - 全量：勾选“有家具”（前端表现：筛选按钮高亮，列表显著变短）→ 期望 ≈33（以本批 CSV 为准）
- SQL（可选）
  - 异常值：任一特征列不存在非 {TRUE,FALSE,NULL}
  - 分布：COUNT(*) FILTER (WHERE is_furnished IS TRUE/FALSE/NULL)
  - 一致性抽检：含“furnished”短语但判 NULL 的样本、含“unfurnished”短语但判 TRUE 的样本，人工复核校正规则/overrides

[Implementation Order]
1) 数据库迁移（事务化，可回滚）
2) ETL 集中判定（加开关，默认启用）
3) 重跑 ETL（本地一次跑完）
4) 清缓存
5) 验收（点名 + 全量）
6) 观察期（overrides 热修、记录报告）
7) 第二阶段（可选，灰度）爬虫瘦身（只爬不判，保留证据字段；ETL 双格式兼容）

[风险与回滚]
- 爬虫：第一阶段零改动，风险≈0
- 数据库：迁移全事务，失败即回滚；如需，可反向 ALTER 或从备份恢复
- ETL：新增开关 USE_ETL_FURNISHED，异常可一键关闭回退旧行为
- 前端表现：仅“有家具”更准确，其它功能不受影响；如数量异常，优先核查 ETL 日志与缓存状态

[附：Crawler Minimal Changes（第二阶段字段建议）]
- 保留最小集合：listing_id, property_url, source, scraped_at, schema_version, address, suburb, state, postcode_raw, property_type_raw, rent_pw_raw, bond_raw, bedrooms_raw, bathrooms_raw, parking_spaces_raw, available_date_raw, inspection_times_raw, images（数组或 JSON 字符串）, latitude_raw, longitude_raw, property_headline, description_raw, features_raw（数组原文）, furnishing_status_raw（若有）
- 移除：任何布尔特征结论（is_furnished/has_*）与 image_1..4；由 ETL 统一判定/解析
- 版本化灰度：ETL 在 schema_version 期间双格式兼容，稳定后去旧分支
