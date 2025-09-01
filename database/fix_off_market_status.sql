-- 修复数据库中 off-market 房源的 is_active 状态
-- 问题：4071条房源标记为 off-market 但 is_active 仍然是 TRUE
-- 解决：将所有 status = 'off-market' 的房源设置为 is_active = FALSE

-- 1. 查看当前状态分布（执行前检查）
SELECT 
    status,
    is_active,
    COUNT(*) as count
FROM properties
GROUP BY status, is_active
ORDER BY status, is_active;

-- 2. 执行修复：将所有 off-market 房源设置为 inactive
BEGIN;

UPDATE properties 
SET 
    is_active = FALSE,
    last_updated = CURRENT_TIMESTAMP
WHERE 
    status = 'off-market' 
    AND is_active = TRUE;

-- 显示影响的行数
GET DIAGNOSTICS @row_count = ROW_COUNT;
DO $$ 
BEGIN 
    RAISE NOTICE 'Updated % rows', @row_count;
END $$;

COMMIT;

-- 3. 验证修复结果
SELECT 
    'Total properties' as category,
    COUNT(*) as count
FROM properties
UNION ALL
SELECT 
    'Active (is_active = TRUE)' as category,
    COUNT(*) as count
FROM properties
WHERE is_active = TRUE
UNION ALL
SELECT 
    'Inactive (is_active = FALSE)' as category,
    COUNT(*) as count
FROM properties
WHERE is_active = FALSE
UNION ALL
SELECT 
    'Off-market with is_active = TRUE (should be 0)' as category,
    COUNT(*) as count
FROM properties
WHERE status = 'off-market' AND is_active = TRUE;

-- 4. 查看修复后各状态的分布
SELECT 
    status,
    COUNT(*) as total,
    COUNT(CASE WHEN is_active = TRUE THEN 1 END) as active,
    COUNT(CASE WHEN is_active = FALSE THEN 1 END) as inactive
FROM properties
GROUP BY status
ORDER BY total DESC;

-- 5. 检查具体数值（应该匹配你的观察）
-- 预期结果：
-- new: 20条 (is_active = TRUE)
-- relisted: 18条 (is_active = TRUE)  
-- updated: 12条 (is_active = TRUE)
-- off-market: 4071条 (is_active = FALSE)
SELECT 
    CASE 
        WHEN status IN ('new', 'relisted', 'updated') THEN status
        ELSE 'off-market'
    END as status_group,
    COUNT(*) as count,
    SUM(CASE WHEN is_active = TRUE THEN 1 ELSE 0 END) as active_count,
    SUM(CASE WHEN is_active = FALSE THEN 1 ELSE 0 END) as inactive_count
FROM properties
GROUP BY status_group
ORDER BY 
    CASE status_group
        WHEN 'new' THEN 1
        WHEN 'relisted' THEN 2
        WHEN 'updated' THEN 3
        WHEN 'off-market' THEN 4
    END;