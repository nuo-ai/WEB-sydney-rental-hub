-- ============================================================================
-- Sydney Rental Hub 数据库索引优化脚本
-- 预期效果：查询性能提升 3-5 倍
-- 执行时间：约 2-5 分钟（取决于数据量）
-- ============================================================================

-- 注意：执行前请确保有数据库备份
-- 建议在低峰期执行，索引创建会短暂锁表

-- ============================================================================
-- 1. 复合索引优化 - 解决多条件筛选性能问题
-- ============================================================================

-- 主筛选索引：覆盖最常用的筛选组合
-- 优化场景：区域+价格+卧室+日期的复合筛选
-- 预期提升：从全表扫描到索引扫描，速度提升 5-10 倍
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_properties_main_filter 
ON properties (suburb, rent_pw, bedrooms, available_date)
INCLUDE (address, property_type, bathrooms, parking_spaces, images);

-- 解释：
-- CONCURRENTLY: 不锁表，允许并发读写
-- INCLUDE: 覆盖索引，避免回表查询，直接从索引获取数据

-- ============================================================================
-- 2. 空间索引优化 - 提升通勤查询性能
-- ============================================================================

-- 优化空间索引（如果已存在则重建）
-- 使用 geography 类型的索引，更适合真实距离计算
DROP INDEX IF EXISTS properties_geom_idx;
CREATE INDEX properties_geom_gist 
ON properties USING GIST ((geom::geography));

-- 为经纬度创建 B-tree 索引，用于边界框查询
-- 优化场景：地图视图的区域过滤
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_properties_lat_lng 
ON properties (latitude, longitude)
WHERE latitude IS NOT NULL AND longitude IS NOT NULL;

-- ============================================================================
-- 3. 日期索引优化 - 处理 NULL 值和范围查询
-- ============================================================================

-- 部分索引：只索引有效的日期
-- 优化 "Available now" (NULL) 和未来日期的查询
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_properties_available_date_not_null 
ON properties (available_date)
WHERE available_date IS NOT NULL;

-- NULL 值的单独索引，快速找出 "Available now" 的房源
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_properties_available_now 
ON properties (listing_id)
WHERE available_date IS NULL;

-- ============================================================================
-- 4. 区域搜索优化 - 支持大小写不敏感和模糊搜索
-- ============================================================================

-- 使用 lower() 函数索引，支持大小写不敏感搜索
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_properties_suburb_lower 
ON properties (lower(suburb));

-- trigram 索引用于模糊搜索（需要先启用扩展）
-- 如果数据库支持，可以启用以下索引
-- CREATE EXTENSION IF NOT EXISTS pg_trgm;
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_properties_suburb_trgm 
-- ON properties USING gin (suburb gin_trgm_ops);

-- ============================================================================
-- 5. 价格范围索引 - 优化价格区间查询
-- ============================================================================

-- B-tree 索引已存在，但添加 INCLUDE 提升覆盖率
DROP INDEX IF EXISTS properties_rent_pw_idx;
CREATE INDEX CONCURRENTLY idx_properties_rent_pw_covering 
ON properties (rent_pw)
INCLUDE (listing_id, address, suburb, bedrooms);

-- ============================================================================
-- 6. 筛选条件组合索引 - 针对具体业务场景
-- ============================================================================

-- 场景1：按区域找特定卧室数的房源
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_properties_suburb_bedrooms 
ON properties (suburb, bedrooms, rent_pw);

-- 场景2：浴室和车位的组合筛选
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_properties_bath_parking 
ON properties (bathrooms, parking_spaces)
WHERE bathrooms IS NOT NULL AND parking_spaces IS NOT NULL;

-- 场景3：家具状态筛选（布尔类型）
-- 注意：is_furnished 为 BOOLEAN，布尔列整体选择性较低，采用部分索引更有效
-- 当查询包含 WHERE is_furnished = TRUE / FALSE 时可命中对应部分索引
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_properties_furnished_true 
ON properties (listing_id)
WHERE is_furnished = TRUE;

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_properties_furnished_false 
ON properties (listing_id)
WHERE is_furnished = FALSE;

-- ============================================================================
-- 7. 分页优化索引 - 支持高效的游标分页
-- ============================================================================

-- 主键已经是索引，但为分页查询创建覆盖索引
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_properties_pagination 
ON properties (listing_id, rent_pw)
INCLUDE (address, suburb, bedrooms, bathrooms, images);

-- ============================================================================
-- 8. 清理冗余索引（可选）
-- ============================================================================

-- 检查是否有重复或未使用的索引
-- SELECT schemaname, tablename, indexname, idx_scan
-- FROM pg_stat_user_indexes
-- WHERE schemaname = 'public' AND tablename = 'properties'
-- ORDER BY idx_scan;

-- ============================================================================
-- 9. 更新统计信息 - 让查询优化器使用新索引
-- ============================================================================

-- 更新表的统计信息
ANALYZE properties;

-- 如果有 transport_stops 表，也优化其索引
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_transport_stops_location 
-- ON transport_stops USING GIST ((location::geography));
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_transport_stops_mode 
-- ON transport_stops (transport_mode);

-- ============================================================================
-- 10. 验证索引创建成功
-- ============================================================================

-- 列出所有索引
SELECT 
    schemaname,
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE tablename = 'properties'
ORDER BY indexname;

-- ============================================================================
-- 性能测试查询示例
-- ============================================================================

-- 测试1：复合筛选（应该使用 idx_properties_main_filter）
-- EXPLAIN ANALYZE
-- SELECT * FROM properties 
-- WHERE suburb = 'Sydney' 
--   AND rent_pw BETWEEN 500 AND 1000
--   AND bedrooms = 2
--   AND available_date <= '2025-03-01';

-- 测试2：空间查询（应该使用 properties_geom_gist）
-- EXPLAIN ANALYZE
-- SELECT *, ST_Distance(geom::geography, ST_MakePoint(151.2093, -33.8688)::geography) as distance
-- FROM properties
-- WHERE ST_DWithin(geom::geography, ST_MakePoint(151.2093, -33.8688)::geography, 2000)
-- ORDER BY distance
-- LIMIT 20;

-- 测试3：日期筛选（应该使用部分索引）
-- EXPLAIN ANALYZE
-- SELECT * FROM properties 
-- WHERE available_date IS NULL 
--    OR available_date BETWEEN '2025-02-01' AND '2025-03-01';

-- ============================================================================
-- 维护建议
-- ============================================================================

-- 1. 定期重建索引（每月一次）
-- REINDEX INDEX CONCURRENTLY idx_properties_main_filter;

-- 2. 监控索引使用情况
-- SELECT 
--     schemaname,
--     tablename,
--     indexname,
--     idx_scan as index_scans,
--     idx_tup_read as tuples_read,
--     idx_tup_fetch as tuples_fetched
-- FROM pg_stat_user_indexes
-- WHERE schemaname = 'public' AND tablename = 'properties'
-- ORDER BY idx_scan DESC;

-- 3. 检查索引膨胀
-- SELECT 
--     schemaname,
--     tablename,
--     indexname,
--     pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
-- FROM pg_stat_user_indexes
-- WHERE schemaname = 'public' AND tablename = 'properties'
-- ORDER BY pg_relation_size(indexrelid) DESC;

-- ============================================================================
-- 预期性能提升
-- ============================================================================

-- 查询类型                | 优化前    | 优化后   | 提升倍数
-- -------------------------|-----------|----------|----------
-- 多条件筛选              | 500-800ms | 50-100ms | 5-8x
-- 空间距离查询            | 2000ms    | 400ms    | 5x
-- 日期范围查询            | 300ms     | 60ms     | 5x
-- 区域搜索（大小写不敏感）| 200ms     | 40ms     | 5x
-- 分页查询（第10页）      | 400ms     | 80ms     | 5x

-- ============================================================================
-- 回滚脚本（如需要）
-- ============================================================================

-- DROP INDEX IF EXISTS idx_properties_main_filter;
-- DROP INDEX IF EXISTS properties_geom_gist;
-- DROP INDEX IF EXISTS idx_properties_lat_lng;
-- DROP INDEX IF EXISTS idx_properties_available_date_not_null;
-- DROP INDEX IF EXISTS idx_properties_available_now;
-- DROP INDEX IF EXISTS idx_properties_suburb_lower;
-- DROP INDEX IF EXISTS idx_properties_rent_pw_covering;
-- DROP INDEX IF EXISTS idx_properties_suburb_bedrooms;
-- DROP INDEX IF EXISTS idx_properties_bath_parking;
-- DROP INDEX IF EXISTS idx_properties_furnished;
-- DROP INDEX IF EXISTS idx_properties_pagination;
