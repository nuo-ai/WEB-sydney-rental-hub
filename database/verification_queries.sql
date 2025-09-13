-- This file contains common SQL queries for verifying the integrity and freshness of the property data.

-- 1. Check the Most Recent Update
-- Shows the timestamp of the latest updated property, confirming the last time the data pipeline ran successfully.
SELECT MAX(last_updated) AS latest_update_time
FROM properties;

-- 2. Count New Listings in a Recent Time Window
-- Helps verify that new data is being added. The INTERVAL can be adjusted (e.g., '1 DAY', '1 WEEK').
-- Count listings added in the last 8 hours
SELECT COUNT(*) AS new_listings_count
FROM properties
WHERE created_at >= NOW() - INTERVAL '8 HOURS';

-- 3. Check for "Stale" Listings
-- Can help identify if the crawler is missing updates for certain properties.
-- Find listings not updated in the last 7 days
SELECT listing_id, address, last_updated
FROM properties
WHERE last_updated < NOW() - INTERVAL '7 DAYS'
ORDER BY last_updated ASC
LIMIT 100;

-- 4. Analyze the Distribution of Updates
-- Groups updates by day, which can help you spot inconsistencies in the data pipeline's execution schedule.
SELECT
  DATE(last_updated) AS update_day,
  COUNT(*) AS number_of_updates
FROM properties
GROUP BY update_day
ORDER BY update_day DESC;

-- 5. Check for Data Quality Issues (NULL Timestamps)
-- Ensures that essential timestamp fields are always populated.
SELECT COUNT(*)
FROM properties
WHERE created_at IS NULL OR last_updated IS NULL;

-- 6. 家具判定一致性核查（关键词 vs 布尔 is_furnished）
-- 目的：用房源文案关键词（正/负/中性）与布尔字段 is_furnished 做对照，发现潜在误判与数据质量问题
-- 前端表现：不影响页面，仅生成内部核查报告；用于提升“只显示带家具”开关的可靠性

-- 规则集（v1 内嵌，后续可外部化为配置/表），polarity：positive/negative/neutral
WITH rules(keyword, polarity, priority) AS (
  VALUES
    ('fully furnished', 'positive', 10),
    ('comes furnished', 'positive', 9),
    ('furnished', 'positive', 8),
    ('with furniture', 'positive', 7),

    ('unfurnished', 'negative', 10),
    ('no furniture', 'negative', 9),
    ('bring your own furniture', 'negative', 8),

    ('whitegoods', 'neutral', 8),
    ('appliances', 'neutral', 7),
    ('fridge only', 'neutral', 7),
    ('washer', 'neutral', 6),
    ('partly furnished', 'neutral', 9),
    ('optional', 'neutral', 5)
),
-- 抽取文本源与关键字段（仅活跃房源）
props AS (
  SELECT 
    listing_id,
    address,
    suburb,
    rent_pw,
    property_url,
    COALESCE(property_headline,'') || ' ' || COALESCE(property_description,'') AS text_blob,
    is_furnished,
    created_at,
    last_updated
  FROM properties
  WHERE is_active = TRUE
),
-- 文案匹配（大小写不敏感，使用 ILIKE + 通配）
matches AS (
  SELECT 
    p.listing_id,
    p.address,
    p.suburb,
    p.rent_pw,
    p.property_url,
    p.is_furnished,
    r.keyword,
    r.polarity,
    r.priority,
    p.created_at,
    p.last_updated
  FROM props p
  JOIN rules r
    ON lower(p.text_blob) ILIKE '%' || lower(r.keyword) || '%'
)

-- A：positive（肯定有家具）命中文案，但 is_furnished ≠ TRUE（疑似漏判）
SELECT 'A_positive_mismatch' AS category, m.*
FROM matches m
WHERE m.polarity = 'positive' AND (m.is_furnished IS DISTINCT FROM TRUE)
ORDER BY m.priority DESC, m.last_updated DESC
LIMIT 200;

-- B：negative（明确无家具）命中文案，但 is_furnished = TRUE（疑似错判）
SELECT 'B_negative_mismatch' AS category, m.*
FROM matches m
WHERE m.polarity = 'negative' AND m.is_furnished IS TRUE
ORDER BY m.priority DESC, m.last_updated DESC
LIMIT 200;

-- C：neutral（中性/保留，如 whitegoods/partly/optional）命中文案，但 is_furnished 非 NULL（建议保持 NULL）
SELECT 'C_neutral_should_be_null' AS category, m.*
FROM matches m
WHERE m.polarity = 'neutral' AND m.is_furnished IS NOT NULL
ORDER BY m.priority DESC, m.last_updated DESC
LIMIT 200;

-- D：近7日异常 TopN（按关键词/极性聚合），用于每日巡检
WITH anomalies AS (
  SELECT * FROM (
    SELECT 'A' AS cat, m.* FROM matches m WHERE m.polarity='positive' AND (m.is_furnished IS DISTINCT FROM TRUE)
    UNION ALL
    SELECT 'B' AS cat, m.* FROM matches m WHERE m.polarity='negative' AND m.is_furnished IS TRUE
    UNION ALL
    SELECT 'C' AS cat, m.* FROM matches m WHERE m.polarity='neutral' AND m.is_furnished IS NOT NULL
  ) t
  WHERE GREATEST(COALESCE(last_updated, created_at), created_at) >= NOW() - INTERVAL '7 days'
)
SELECT polarity, keyword, COUNT(*) AS cnt
FROM anomalies
GROUP BY polarity, keyword
ORDER BY cnt DESC, polarity, keyword
LIMIT 50;

-- E：汇总分布（正/负/中性 文案命中次数 与 is_furnished 布尔分布）
SELECT
  polarity,
  COUNT(*) AS occurrences,
  COUNT(*) FILTER (WHERE is_furnished IS TRUE) AS furnished_true,
  COUNT(*) FILTER (WHERE is_furnished IS FALSE) AS furnished_false,
  COUNT(*) FILTER (WHERE is_furnished IS NULL) AS furnished_null
FROM matches
GROUP BY polarity
ORDER BY polarity;
