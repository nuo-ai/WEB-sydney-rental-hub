-- 检查当前数据库中的房源状态分布
SELECT 
    is_active,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM properties
GROUP BY is_active
ORDER BY is_active;

-- 显示活跃房源总数
SELECT COUNT(*) as active_properties FROM properties WHERE is_active = TRUE;

-- 显示最近的更新记录
SELECT 
    DATE(last_updated) as update_date,
    COUNT(*) as count
FROM properties
WHERE last_updated IS NOT NULL
GROUP BY DATE(last_updated)
ORDER BY update_date DESC
LIMIT 5;