CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS transport_stops (
    stop_id VARCHAR(255) PRIMARY KEY,
    stop_name TEXT,
    latitude DECIMAL(9,6),
    longitude DECIMAL(10,6),
    location GEOMETRY(Point, 4326),
    location_type INTEGER,
    parent_station VARCHAR(255),
    transport_mode VARCHAR(50) DEFAULT NULL,
    serviced_routes_details JSONB DEFAULT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_transport_stops_location ON transport_stops USING GIST (location);

CREATE INDEX IF NOT EXISTS idx_transport_stops_parent_station ON transport_stops (parent_station);

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = NOW();
   RETURN NEW;
END;
$$ language 'plpgsql';

DO $$
BEGIN
   IF NOT EXISTS (
       SELECT 1
       FROM pg_trigger
       WHERE tgname = 'trigger_update_transport_stops_updated_at'
   ) THEN
       CREATE TRIGGER trigger_update_transport_stops_updated_at
       BEFORE UPDATE ON transport_stops
       FOR EACH ROW
       EXECUTE FUNCTION update_updated_at_column();
   END IF;
END;
$$;

COMMENT ON COLUMN transport_stops.stop_id IS 'Unique identifier for a stop or station, from GTFS stops.txt (stop_id).';
COMMENT ON COLUMN transport_stops.stop_name IS 'Name of the stop or station, from GTFS stops.txt (stop_name).';
COMMENT ON COLUMN transport_stops.latitude IS 'Latitude of the stop or station, from GTFS stops.txt (stop_lat).';
COMMENT ON COLUMN transport_stops.longitude IS 'Longitude of the stop or station, from GTFS stops.txt (stop_lon).';
COMMENT ON COLUMN transport_stops.location IS 'Geographic location of the stop/station as a PostGIS POINT geometry (SRID 4326). Generated from latitude and longitude.';
COMMENT ON COLUMN transport_stops.location_type IS 'Type of location, from GTFS stops.txt (location_type). 0 or empty: stop/platform. 1: station. 2: entrance/exit. 3: generic node. 4: boarding area.';
COMMENT ON COLUMN transport_stops.parent_station IS 'Identifier of the parent station, if this stop is part of a station complex. From GTFS stops.txt (parent_station).';
COMMENT ON COLUMN transport_stops.transport_mode IS 'Primary transport mode serving this stop (e.g., Bus, Train, Ferry, Light Rail). To be populated later.';
COMMENT ON COLUMN transport_stops.serviced_routes_details IS 'JSONB array of route details serving this stop. To be populated later.';
