-- 添加 last_seen_at 字段用于追踪房源最后活跃时间
-- 这个字段将在每次看到房源时更新，用于识别已下架的房源

ALTER TABLE properties 
ADD COLUMN IF NOT EXISTS last_seen_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP;

-- 为现有记录设置 last_seen_at 为 created_at 的值
UPDATE properties 
SET last_seen_at = created_at 
WHERE last_seen_at IS NULL;

-- 为 last_seen_at 创建索引，因为我们会经常查询这个字段
CREATE INDEX IF NOT EXISTS properties_last_seen_at_idx ON properties (last_seen_at);

-- 添加 bedroom_display 字段用于前端显示
ALTER TABLE properties 
ADD COLUMN IF NOT EXISTS bedroom_display VARCHAR(20);

-- 为现有记录生成 bedroom_display 值
UPDATE properties 
SET bedroom_display = CASE 
    WHEN bedrooms = 0 THEN 'Studio'
    ELSE bedrooms::VARCHAR
END
WHERE bedroom_display IS NULL;
