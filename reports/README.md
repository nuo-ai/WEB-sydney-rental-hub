# Furnishing (is_furnished) 审计与运行手册

目的：指导在本地/服务器运行“家具判定质量闭环 v1”，生成审计报告，并在必要时手工核验索引与缓存失效。此流程不改变前端表现，仅用于内部质量监控。

目录结构
- reports/
  - README.md（本说明）
  - furnishing_audit_YYYY-MM-DD.txt（执行后生成的审计报告）

前置条件
- 已配置数据库连接环境变量：`$DATABASE_URL`
- 可用的命令行工具：
  - psql（PostgreSQL 客户端）
  - curl（调用缓存失效接口）
- 处于仓库根目录（包含 database/ 和 backend/ 等目录）

一键执行（建议在低峰期）
以下命令依次执行：
1) 创建/更新索引（CONCURRENTLY，不锁表）
2) 触发缓存失效（确保“前端表现”立即与新查询一致）
3) 生成审计报告并输出到 reports 目录

Linux / macOS / WSL
```bash
mkdir -p reports
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f database/optimize_indexes.sql
# 让属性列表相关缓存失效（如需全量失效见下文）
curl -sS -X POST http://localhost:8000/api/cache/invalidate || true
# 生成审计报告（关键词 vs 布尔的一致性核查）
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f database/verification_queries.sql > "reports/furnishing_audit_$(date +%F).txt"
```

Windows（PowerShell）
```powershell
New-Item -ItemType Directory -Force -Path reports | Out-Null
psql "$env:DATABASE_URL" -v ON_ERROR_STOP=1 -f database/optimize_indexes.sql
# 让属性列表相关缓存失效
curl -sS -X POST http://localhost:8000/api/cache/invalidate
# 生成审计报告
$today = Get-Date -UFormat "%Y-%m-%d"
psql "$env:DATABASE_URL" -v ON_ERROR_STOP=1 -f database/verification_queries.sql | Out-File -Encoding utf8 "reports/furnishing_audit_$today.txt"
```

缓存失效接口说明
- 仅失效属性列表缓存（常用）
```bash
curl -X POST http://localhost:8000/api/cache/invalidate
```
- 仅失效某个房源详情缓存
```bash
curl -X POST "http://localhost:8000/api/cache/invalidate?property_id=12345"
```
- 全量缓存（仅调试用，慎用）
```bash
curl -X POST "http://localhost:8000/api/cache/invalidate" -H "Content-Type: application/json" -d '{"invalidate_all": true}'
```

索引与数据快速核验
- 查看当前家具相关索引
```sql
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'properties' AND indexname LIKE '%furnished%';
```
- 查看 is_furnished 分布（NULL 表示未知/不确定）
```sql
SELECT is_furnished, COUNT(*) FROM properties GROUP BY is_furnished;
```

报告内容与解读（来自 database/verification_queries.sql）
- A_positive_mismatch：文案肯定“有家具”，但 `is_furnished ≠ TRUE`（疑似漏判）
- B_negative_mismatch：文案否定“无家具”，但 `is_furnished = TRUE`（疑似错判）
- C_neutral_should_be_null：文案中性（如 `whitegoods/partly/optional`），但 `is_furnished IS NOT NULL`（建议保持 NULL）
- 近 7 日异常 TopN：最近更新的异常关键词分布，便于每日巡检
- 分布汇总：各极性命中文案在布尔分布上的统计

常见问题（FAQ）
- 未生成审计文件？
  - 确认已安装 psql 且 `$DATABASE_URL` 有效
  - 确认命令是在仓库根目录执行（存在 database/verification_queries.sql）
  - Windows 环境使用 PowerShell 版本命令
- 运行索引脚本失败？
  - 确认权限与连接；脚本已使用 CONCURRENTLY，理论上不锁表
  - 可根据回滚段落中的 DROP INDEX 指令逐步回退

回滚与幂等性
- 文档与核查 SQL：新增型变更，无需回滚
- 索引：脚本中所有 CREATE 都是 IF NOT EXISTS；如需回退可使用 `DROP INDEX CONCURRENTLY` 指定索引名
- 缓存失效：幂等操作，无需回滚

版本
- 2025-09-13 v1：建立质量闭环（关键词规则 CTE + 一致性报表），与 REST/GraphQL 契约和索引策略对齐
