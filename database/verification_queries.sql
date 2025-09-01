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
