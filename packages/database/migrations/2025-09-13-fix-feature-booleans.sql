-- Migration: Unify feature columns to BOOLEAN (Phase 1: is_furnished only, minimal-risk)
-- Why: 历史字符串(如 'yes'/'no')导致筛选不准；统一为 BOOLEAN（TRUE/FALSE/NULL）以保证前后端一致
-- Scope: 最小化变更，先处理 is_furnished（其余特征列留待下一次小步补丁，避免误伤未知列/约束命名差异）
-- Safety:
--   - 事务化：失败即回滚
--   - 幂等：重复执行不改变语义
--   - 兼容：后端筛选已使用稳健文本匹配，布尔化后继续兼容

BEGIN;

-- Step 0: 预清洗（如果历史还有 'yes'/'no' 等文本，先规范化为布尔/NULL）
-- 注：若列已是 BOOLEAN 类型，此 UPDATE 语义安全（is_furnished::text 仍可取到 't'/'f'）
UPDATE properties
SET is_furnished = CASE
  WHEN LOWER(is_furnished::text) IN ('t','true','yes','1') THEN TRUE
  WHEN LOWER(is_furnished::text) IN ('f','false','no','0') THEN FALSE
  ELSE NULL
END;

-- Step 1: 尝试删除与 is_furnished 相关的历史 CHECK 约束（命名不确定，做宽松匹配，IF EXISTS 保守防护）
-- 说明：某些早期版本可能有如下命名模式：properties_is_furnished_check 或 is_furnished_check
ALTER TABLE properties DROP CONSTRAINT IF EXISTS properties_is_furnished_check;
ALTER TABLE properties DROP CONSTRAINT IF EXISTS is_furnished_check;

-- Step 2: 强制列类型为 BOOLEAN（使用 USING CASE 确保安全转换）
-- 若列已为 BOOLEAN，此语句不会改变语义
ALTER TABLE properties
ALTER COLUMN is_furnished TYPE BOOLEAN
USING CASE
  WHEN LOWER(is_furnished::text) IN ('t','true','yes','1') THEN TRUE
  WHEN LOWER(is_furnished::text) IN ('f','false','no','0') THEN FALSE
  ELSE NULL
END;

-- 可选 Step 3: 针对布尔过滤建立部分索引（如列表页经常用 is_furnished=true 过滤，可提升命中）
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_properties_furnished_true
--   ON properties (listing_id) WHERE is_furnished = TRUE;

COMMIT;

-- 执行后建议：
-- 1) 清缓存：POST /api/cache/invalidate?invalidate_all=true
-- 2) 验收：
--    - /api/properties/{id} → "is_furnished": true/false/null（不应再出现 'yes'/'no' 字符串）
--    - /api/properties?isFurnished=true&page=1&page_size=20 仅返回 TRUE 项
-- 3) 记录：将本次执行与统计写入 reports/furnishing-normalization.md

-- 备注（后续小步补丁计划）：
-- 其余特征列（如 has_air_conditioning/has_balcony/...）建议分批、逐列统一为 BOOLEAN，
-- 每次变更 3–5 列，遵循相同 USING CASE 映射规则，并在变更前以信息架构脚本核对现存列名与约束名，降低风险。
