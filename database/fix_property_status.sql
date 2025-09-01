-- ============================================
-- 修复房源状态脚本
-- 目的：重置所有房源的is_active状态，准备重新运行ETL
-- 执行时间：2025-02-01
-- ============================================

-- 步骤1：查看当前状态分布（执行前）
SELECT 
    is_active,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM properties
GROUP BY is_active
ORDER BY is_active;

-- 步骤2：备份当前状态（可选，用于回滚）
-- CREATE TABLE properties_status_backup_20250201 AS
-- SELECT listing_id, is_active, last_seen_at, last_updated
-- FROM properties;

-- 步骤3：重置所有房源为不活跃
-- 这样下次运行ETL时，只有爬虫爬到的房源会被标记为活跃
UPDATE properties 
SET 
    is_active = FALSE,
    last_updated = NOW()
WHERE is_active = TRUE;

-- 显示更新结果
SELECT 
    'Updated ' || COUNT(*) || ' properties to inactive' as result
FROM properties 
WHERE is_active = FALSE;

-- 步骤4：验证更新后的状态
SELECT 
    is_active,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM properties
GROUP BY is_active
ORDER BY is_active;

-- 提示：执行此脚本后，需要运行 python database/update_database.py 
-- 来根据最新的爬虫数据重新设置正确的房源状态