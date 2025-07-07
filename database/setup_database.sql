CREATE TABLE IF NOT EXISTS properties (
    listing_id BIGINT PRIMARY KEY,
    property_url TEXT,
    address TEXT,
    suburb VARCHAR(255),
    state VARCHAR(50),
    postcode VARCHAR(10),
    property_type VARCHAR(100),
    rent_pw INTEGER,
    bond INTEGER,
    bedrooms SMALLINT,
    bathrooms SMALLINT,
    parking_spaces SMALLINT,
    available_date DATE,
    inspection_times TEXT,
    agency_name TEXT,
    agent_name TEXT,
    agent_phone VARCHAR(50),
    agent_email VARCHAR(255),
    property_headline TEXT,
    property_description TEXT,
    has_air_conditioning BOOLEAN,
    is_furnished BOOLEAN,
    has_balcony BOOLEAN,
    has_dishwasher BOOLEAN,
    has_laundry BOOLEAN,
    has_built_in_wardrobe BOOLEAN,
    has_gym BOOLEAN,
    has_pool BOOLEAN,
    has_parking BOOLEAN,
    allows_pets BOOLEAN,
    has_security_system BOOLEAN,
    has_storage BOOLEAN,
    has_study_room BOOLEAN,
    has_garden BOOLEAN,
    latitude NUMERIC(10, 7),
    longitude NUMERIC(10, 7),
    images JSONB,
    property_features JSONB,
    agent_profile_url TEXT,
    agent_logo_url TEXT,
    enquiry_form_action TEXT,
    geom GEOMETRY(Point, 4326), -- For PostGIS spatial data
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create an index on the geometry column for faster spatial queries
CREATE INDEX IF NOT EXISTS properties_geom_idx ON properties USING GIST (geom);

-- Create indexes on commonly queried columns
CREATE INDEX IF NOT EXISTS properties_suburb_idx ON properties (suburb);
CREATE INDEX IF NOT EXISTS properties_rent_pw_idx ON properties (rent_pw);
CREATE INDEX IF NOT EXISTS properties_bedrooms_idx ON properties (bedrooms);
CREATE INDEX IF NOT EXISTS properties_property_type_idx ON properties (property_type);
CREATE INDEX IF NOT EXISTS properties_is_active_idx ON properties (is_active);

-- Trigger function to update last_updated timestamp
CREATE OR REPLACE FUNCTION update_last_updated_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.last_updated = NOW();
   RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE TRIGGER update_properties_last_updated
BEFORE UPDATE ON properties
FOR EACH ROW
EXECUTE FUNCTION update_last_updated_column();
