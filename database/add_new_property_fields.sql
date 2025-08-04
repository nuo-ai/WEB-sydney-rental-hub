-- Migration script to add new fields from the updated crawler to the properties table

ALTER TABLE properties
ADD COLUMN IF NOT EXISTS cover_image TEXT,
ADD COLUMN IF NOT EXISTS furnishing_status VARCHAR(100),
ADD COLUMN IF NOT EXISTS air_conditioning_type VARCHAR(100),
ADD COLUMN IF NOT EXISTS has_gas_cooking BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS has_heating BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS has_intercom BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS has_lift BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS has_garbage_disposal BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS has_city_view BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS has_water_view BOOLEAN DEFAULT FALSE;

-- Rename existing columns to match new CSV headers for consistency
-- Note: Supabase/PostgreSQL might not support renaming columns if they are used in views or functions.
-- It's often safer to handle this in the ETL script, but we add it here for documentation.

-- ALTER TABLE properties RENAME COLUMN has_built_in_wardrobe TO has_wardrobes;
-- ALTER TABLE properties RENAME COLUMN has_study_room TO has_study;
-- The ETL script (process_csv.py) has been updated to handle this mapping,
-- so direct renaming in the DB is not immediately necessary.

COMMENT ON COLUMN properties.furnishing_status IS 'e.g., furnished, unfurnished, optional';
COMMENT ON COLUMN properties.air_conditioning_type IS 'e.g., general, ducted, split_system';

-- No changes needed for has_security_system, has_storage, has_garden as they are not in the new CSV
-- but we want to keep them in the DB for potential future use.

SELECT 'Migration to add new property fields completed.' AS status;
