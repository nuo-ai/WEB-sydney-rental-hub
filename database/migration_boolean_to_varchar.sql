-- Migration: Convert boolean fields to varchar for three-state logic
-- Date: 2025-08-05
-- Purpose: Convert from True/False to 'yes'/'no'/'unknown' format

BEGIN;

-- Convert boolean fields to varchar and update existing data
-- For boolean fields that represent features/amenities

-- has_air_conditioning
ALTER TABLE properties ALTER COLUMN has_air_conditioning TYPE varchar(10);
UPDATE properties SET has_air_conditioning = CASE 
    WHEN has_air_conditioning::text = 'true' THEN 'yes'
    WHEN has_air_conditioning::text = 'false' THEN 'unknown'
    ELSE 'unknown'
END;

-- is_furnished  
ALTER TABLE properties ALTER COLUMN is_furnished TYPE varchar(10);
UPDATE properties SET is_furnished = CASE 
    WHEN is_furnished::text = 'true' THEN 'yes'
    WHEN is_furnished::text = 'false' THEN 'unknown'
    ELSE 'unknown'
END;

-- has_balcony
ALTER TABLE properties ALTER COLUMN has_balcony TYPE varchar(10);
UPDATE properties SET has_balcony = CASE 
    WHEN has_balcony::text = 'true' THEN 'yes'
    WHEN has_balcony::text = 'false' THEN 'unknown'
    ELSE 'unknown'
END;

-- has_dishwasher
ALTER TABLE properties ALTER COLUMN has_dishwasher TYPE varchar(10);
UPDATE properties SET has_dishwasher = CASE 
    WHEN has_dishwasher::text = 'true' THEN 'yes'
    WHEN has_dishwasher::text = 'false' THEN 'unknown'
    ELSE 'unknown'
END;

-- has_laundry
ALTER TABLE properties ALTER COLUMN has_laundry TYPE varchar(10);
UPDATE properties SET has_laundry = CASE 
    WHEN has_laundry::text = 'true' THEN 'yes'
    WHEN has_laundry::text = 'false' THEN 'unknown'
    ELSE 'unknown'
END;

-- has_built_in_wardrobe (maps to has_wardrobes in CSV)
ALTER TABLE properties ALTER COLUMN has_built_in_wardrobe TYPE varchar(10);
UPDATE properties SET has_built_in_wardrobe = CASE 
    WHEN has_built_in_wardrobe::text = 'true' THEN 'yes'
    WHEN has_built_in_wardrobe::text = 'false' THEN 'unknown'
    ELSE 'unknown'
END;

-- has_gym
ALTER TABLE properties ALTER COLUMN has_gym TYPE varchar(10);
UPDATE properties SET has_gym = CASE 
    WHEN has_gym::text = 'true' THEN 'yes'
    WHEN has_gym::text = 'false' THEN 'unknown'
    ELSE 'unknown'
END;

-- has_pool
ALTER TABLE properties ALTER COLUMN has_pool TYPE varchar(10);
UPDATE properties SET has_pool = CASE 
    WHEN has_pool::text = 'true' THEN 'yes'
    WHEN has_pool::text = 'false' THEN 'unknown'
    ELSE 'unknown'
END;

-- has_parking
ALTER TABLE properties ALTER COLUMN has_parking TYPE varchar(10);
UPDATE properties SET has_parking = CASE 
    WHEN has_parking::text = 'true' THEN 'yes'
    WHEN has_parking::text = 'false' THEN 'unknown'
    ELSE 'unknown'
END;

-- allows_pets
ALTER TABLE properties ALTER COLUMN allows_pets TYPE varchar(10);
UPDATE properties SET allows_pets = CASE 
    WHEN allows_pets::text = 'true' THEN 'yes'
    WHEN allows_pets::text = 'false' THEN 'unknown'
    ELSE 'unknown'
END;

-- has_security_system
ALTER TABLE properties ALTER COLUMN has_security_system TYPE varchar(10);
UPDATE properties SET has_security_system = CASE 
    WHEN has_security_system::text = 'true' THEN 'yes'
    WHEN has_security_system::text = 'false' THEN 'unknown'
    ELSE 'unknown'
END;

-- has_storage
ALTER TABLE properties ALTER COLUMN has_storage TYPE varchar(10);
UPDATE properties SET has_storage = CASE 
    WHEN has_storage::text = 'true' THEN 'yes'
    WHEN has_storage::text = 'false' THEN 'unknown'
    ELSE 'unknown'
END;

-- has_study_room (maps to has_study in CSV)
ALTER TABLE properties ALTER COLUMN has_study_room TYPE varchar(10);
UPDATE properties SET has_study_room = CASE 
    WHEN has_study_room::text = 'true' THEN 'yes'
    WHEN has_study_room::text = 'false' THEN 'unknown'
    ELSE 'unknown'
END;

-- has_garden
ALTER TABLE properties ALTER COLUMN has_garden TYPE varchar(10);
UPDATE properties SET has_garden = CASE 
    WHEN has_garden::text = 'true' THEN 'yes'
    WHEN has_garden::text = 'false' THEN 'unknown'
    ELSE 'unknown'
END;

-- has_gas_cooking
ALTER TABLE properties ALTER COLUMN has_gas_cooking TYPE varchar(10);
UPDATE properties SET has_gas_cooking = CASE 
    WHEN has_gas_cooking::text = 'true' THEN 'yes'
    WHEN has_gas_cooking::text = 'false' THEN 'unknown'
    ELSE 'unknown'
END;

-- has_heating
ALTER TABLE properties ALTER COLUMN has_heating TYPE varchar(10);
UPDATE properties SET has_heating = CASE 
    WHEN has_heating::text = 'true' THEN 'yes'
    WHEN has_heating::text = 'false' THEN 'unknown'
    ELSE 'unknown'
END;

-- has_intercom
ALTER TABLE properties ALTER COLUMN has_intercom TYPE varchar(10);
UPDATE properties SET has_intercom = CASE 
    WHEN has_intercom::text = 'true' THEN 'yes'
    WHEN has_intercom::text = 'false' THEN 'unknown'
    ELSE 'unknown'
END;

-- has_lift
ALTER TABLE properties ALTER COLUMN has_lift TYPE varchar(10);
UPDATE properties SET has_lift = CASE 
    WHEN has_lift::text = 'true' THEN 'yes'
    WHEN has_lift::text = 'false' THEN 'unknown'
    ELSE 'unknown'
END;

-- has_garbage_disposal
ALTER TABLE properties ALTER COLUMN has_garbage_disposal TYPE varchar(10);
UPDATE properties SET has_garbage_disposal = CASE 
    WHEN has_garbage_disposal::text = 'true' THEN 'yes'
    WHEN has_garbage_disposal::text = 'false' THEN 'unknown'
    ELSE 'unknown'
END;

-- has_city_view
ALTER TABLE properties ALTER COLUMN has_city_view TYPE varchar(10);
UPDATE properties SET has_city_view = CASE 
    WHEN has_city_view::text = 'true' THEN 'yes'
    WHEN has_city_view::text = 'false' THEN 'unknown'
    ELSE 'unknown'
END;

-- has_water_view
ALTER TABLE properties ALTER COLUMN has_water_view TYPE varchar(10);
UPDATE properties SET has_water_view = CASE 
    WHEN has_water_view::text = 'true' THEN 'yes'
    WHEN has_water_view::text = 'false' THEN 'unknown'
    ELSE 'unknown'
END;

-- Add constraints to ensure only valid values
ALTER TABLE properties ADD CONSTRAINT check_has_air_conditioning CHECK (has_air_conditioning IN ('yes', 'no', 'unknown'));
ALTER TABLE properties ADD CONSTRAINT check_is_furnished CHECK (is_furnished IN ('yes', 'no', 'unknown'));
ALTER TABLE properties ADD CONSTRAINT check_has_balcony CHECK (has_balcony IN ('yes', 'no', 'unknown'));
ALTER TABLE properties ADD CONSTRAINT check_has_dishwasher CHECK (has_dishwasher IN ('yes', 'no', 'unknown'));
ALTER TABLE properties ADD CONSTRAINT check_has_laundry CHECK (has_laundry IN ('yes', 'no', 'unknown'));
ALTER TABLE properties ADD CONSTRAINT check_has_built_in_wardrobe CHECK (has_built_in_wardrobe IN ('yes', 'no', 'unknown'));
ALTER TABLE properties ADD CONSTRAINT check_has_gym CHECK (has_gym IN ('yes', 'no', 'unknown'));
ALTER TABLE properties ADD CONSTRAINT check_has_pool CHECK (has_pool IN ('yes', 'no', 'unknown'));
ALTER TABLE properties ADD CONSTRAINT check_has_parking CHECK (has_parking IN ('yes', 'no', 'unknown'));
ALTER TABLE properties ADD CONSTRAINT check_allows_pets CHECK (allows_pets IN ('yes', 'no', 'unknown'));
ALTER TABLE properties ADD CONSTRAINT check_has_security_system CHECK (has_security_system IN ('yes', 'no', 'unknown'));
ALTER TABLE properties ADD CONSTRAINT check_has_storage CHECK (has_storage IN ('yes', 'no', 'unknown'));
ALTER TABLE properties ADD CONSTRAINT check_has_study_room CHECK (has_study_room IN ('yes', 'no', 'unknown'));
ALTER TABLE properties ADD CONSTRAINT check_has_garden CHECK (has_garden IN ('yes', 'no', 'unknown'));
ALTER TABLE properties ADD CONSTRAINT check_has_gas_cooking CHECK (has_gas_cooking IN ('yes', 'no', 'unknown'));
ALTER TABLE properties ADD CONSTRAINT check_has_heating CHECK (has_heating IN ('yes', 'no', 'unknown'));
ALTER TABLE properties ADD CONSTRAINT check_has_intercom CHECK (has_intercom IN ('yes', 'no', 'unknown'));
ALTER TABLE properties ADD CONSTRAINT check_has_lift CHECK (has_lift IN ('yes', 'no', 'unknown'));
ALTER TABLE properties ADD CONSTRAINT check_has_garbage_disposal CHECK (has_garbage_disposal IN ('yes', 'no', 'unknown'));
ALTER TABLE properties ADD CONSTRAINT check_has_city_view CHECK (has_city_view IN ('yes', 'no', 'unknown'));
ALTER TABLE properties ADD CONSTRAINT check_has_water_view CHECK (has_water_view IN ('yes', 'no', 'unknown'));

COMMIT;

-- Verification queries
SELECT 'Migration completed successfully. Sample data after migration:' as status;
SELECT listing_id, has_air_conditioning, is_furnished, has_parking, allows_pets 
FROM properties 
LIMIT 5;
