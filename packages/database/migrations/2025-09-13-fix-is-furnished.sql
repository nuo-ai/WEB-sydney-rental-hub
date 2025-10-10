-- Migration: Normalize legacy is_furnished values to boolean/NULL
-- Purpose:
--   1) 将历史 'yes'/'no'/'unknown' 等文本规范化为布尔/NULL，消除“文案无家具却被判有家具”的来源
--   2) 可选：将列强制为 BOOLEAN，彻底阻断再次写入字符串（建议在验证无误后执行）
-- Safety:
--   - 该脚本为幂等（重复执行不会改变语义结果）
--   - 请在业务低峰期执行，并在执行后清理缓存（/api/cache/invalidate）

BEGIN;

-- Step 1: 规范化历史文本值 → 布尔/NULL
-- 说明：仅把明确正例映射为 TRUE、明确负例映射为 FALSE，其余一律 NULL
UPDATE properties
SET is_furnished = CASE
  WHEN LOWER(is_furnished::text) IN ('t','true','yes','1') THEN TRUE
  WHEN LOWER(is_furnished::text) IN ('f','false','no','0') THEN FALSE
  ELSE NULL
END;

-- 可选 Step 2: 强制列类型为 BOOLEAN（推荐在确认上一步运行正常后执行）
-- 注意：如列已为 BOOLEAN，可跳过该步骤或保留无害执行
-- ALTER TABLE properties
-- ALTER COLUMN is_furnished TYPE BOOLEAN
-- USING CASE
--   WHEN LOWER(is_furnished::text) IN ('t','true','yes','1') THEN TRUE
--   WHEN LOWER(is_furnished::text) IN ('f','false','no','0') THEN FALSE
--   ELSE NULL
-- END;

-- 可选 Step 3: 针对布尔过滤建立部分索引（若尚未建立，建议使用 database/optimize_indexes.sql 中的索引脚本）
-- 示例（如需在此处一并创建，可取消注释）：
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_properties_furnished_true
--   ON properties (listing_id) WHERE is_furnished = TRUE;
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_properties_furnished_false
--   ON properties (listing_id) WHERE is_furnished = FALSE;

COMMIT;

-- 执行后建议：
-- 1) 选择性清缓存：POST /api/cache/invalidate?property_id={listing_id}（如需全量：/api/cache/invalidate?invalidate_all=true）
-- 2) 回归验证：
--    - /api/properties/{id} 应返回 data.is_furnished 为 true/false/null（不再出现 'yes'）
--    - /api/properties?listing_id={id}&isFurnished=true&page=1&page_size=1：若非 true，应返回空集合
--    - 勾选“带家具”：unknown 不应混入
