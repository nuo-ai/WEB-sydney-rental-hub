# 家具判定契约与质量闭环（is_furnished）

本文档用于统一“有无家具（is_furnished）”在全链路中的口径与操作手册，覆盖：REST/GraphQL 契约、数据库索引策略、日常质量核查与回滚指引。

- 面向读者：前后端工程师、ETL/Crawler 维护者、运营/数据质检。
- 变更范围：不改变前端表现，仅修复和补充内部逻辑与观测能力。

## 1. 背景与目标

- 历史问题：不同层对“家具”采用不一致口径（字符串三态 'yes'/'no'/'unknown' vs 数据库 BOOLEAN），导致筛选永不命中、索引无效、GraphQL 不返回等。
- 目标：全链路统一为布尔标准（True/False/NULL），REST/GraphQL 契约一致，索引与查询对齐，新增可观测的“关键词 vs 布尔”一致性核查报告。

## 2. 前端契约（不改动“前端表现”）

- 参数：`isFurnished`（布尔）
  - 未传：不加家具过滤
  - `true`：只返回带家具（DB 条件 `is_furnished = TRUE`）
  - `false`：只返回不带家具（DB 条件 `is_furnished = FALSE`）
- 兜底：ETL 不再写入 `'yes'/'no'/'unknown'` 字符串，统一标准化为布尔；未知写 `NULL`。

## 3. REST 契约

- 列表：`GET /api/properties?isFurnished=true`
  - 仅返回 `is_furnished = TRUE`。
- 列表：`GET /api/properties`（未传）
  - 不加家具条件。
- 详情：`GET /api/properties/{id}`
  - 返回体包含 `is_furnished`（true/false/null）。

说明（为什么这样做）：与 DB 布尔字段一致，避免字符串比较导致条件永不命中，确保索引可用且结果正确。

## 4. GraphQL 契约

- 模型字段：`Property.is_furnished: Boolean`
- 列表/详情查询统一回填该字段。

示例：
```graphql
query {
  properties {
    listing_id
    address
    is_furnished   # true / false / null
  }
}
```

## 5. 数据库索引策略（与查询对齐）

- 布尔列选择性低，采用“部分索引”覆盖常见过滤：
  - `WHERE is_furnished = TRUE`
  - `WHERE is_furnished = FALSE`
- 已在 `database/optimize_indexes.sql` 中加入：
  ```sql
  CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_properties_furnished_true 
  ON properties (listing_id) WHERE is_furnished = TRUE;

  CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_properties_furnished_false
  ON properties (listing_id) WHERE is_furnished = FALSE;
  ```

## 6. 质量闭环 v1（关键词 vs 布尔一致性核查）

- 文件：`database/verification_queries.sql`
- 新增内容：基于文案关键词（positive/negative/neutral）与 `is_furnished` 的对照报表：
  - A：positive 命中但 `is_furnished ≠ TRUE`（疑似漏判）
  - B：negative 命中但 `is_furnished = TRUE`（疑似错判）
  - C：neutral 命中但 `is_furnished IS NOT NULL`（建议保持 NULL）
  - D：近 7 日异常 TopN（聚合）
  - E：分布汇总（各极性 vs 布尔分布）
- v1 规则集内嵌于 SQL（后续可外部化为配置/表供 ETL 与 SQL 共享）。

运行（示例）：
```bash
# 使用 psql 执行（请替换连接串/环境变量）
psql "$DATABASE_URL" -f database/verification_queries.sql
```

## 7. 运维步骤与命令（建议在低峰期）

1) 运行索引脚本（CONCURRENTLY）
```bash
# 仅示例：请确认有 psql/权限及 $DATABASE_URL
psql "$DATABASE_URL" -f database/optimize_indexes.sql
```

2) 触发缓存失效（确保“前端表现”与新查询一致）
```bash
# 让列表与详情缓存失效（按需二选一）
# 全部属性列表相关缓存
curl -X POST http://localhost:8000/api/cache/invalidate

# 指定某个房源详情缓存
curl -X POST "http://localhost:8000/api/cache/invalidate?property_id=12345"

# 全量缓存（仅调试用）
curl -X POST "http://localhost:8000/api/cache/invalidate" -d '{"invalidate_all": true}' -H "Content-Type: application/json"
```

3) 生成并保存质量报告（基线）
```bash
# 输出截断到文件：供对比回归
psql "$DATABASE_URL" -f database/verification_queries.sql > reports/furnishing_audit_$(date +%F).txt
```

备注：以上命令仅为运行示例。生产执行请遵从变更流程与权限控制。

## 8. 验证清单

- SQL 快查：
  ```sql
  SELECT is_furnished, COUNT(*) FROM properties GROUP BY is_furnished;
  SELECT indexname FROM pg_indexes WHERE tablename='properties' AND indexname LIKE '%furnished%';
  ```
- REST：
  - `GET /api/properties?isFurnished=true` 仅返回带家具；
  - `GET /api/properties` 不加家具过滤。
- GraphQL：
  - `Property.is_furnished` 字段能正常返回（true/false/null）。
- 质量核查：
  - 执行 `database/verification_queries.sql`，产出 A/B/C 分类样本与 D/E 统计。

## 9. 回滚与风控

- 文档与核查 SQL：新增型变更，无需回滚；
- 索引：可按需 `DROP INDEX CONCURRENTLY idx_properties_furnished_true/false` 回退；
- 缓存：失效操作为幂等，不涉及回滚风险。

## 10. FAQ

- Q：为什么不提供 `furnishing_status` 三态？  
  A：当前以布尔为准（True/False/NULL），契约更简单且与 DB 对齐；未来可在不破坏兼容的前提下扩展三态描述。

- Q：`false` 是否包括“unknown”？  
  A：否。`false` 仅表示明确“不带家具”；`unknown` 用 `NULL` 表示，未勾选时不参与过滤。

- Q：为什么 neutral 命中建议写 NULL？  
  A：如 `whitegoods/partly/optional` 语义模糊、不可直接判定有/无家具，为避免误导，建议保持 `NULL` 并在 UI/筛选逻辑上保守处理。

---

变更记录
- 2025-09-13 v1：建立质量闭环（关键词规则 CTE + 一致性报表），统一 REST/GraphQL 契约描述，记录索引与运维指引。
