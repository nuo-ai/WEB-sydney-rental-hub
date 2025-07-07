import psycopg2
import os
import datetime
from dotenv import load_dotenv
import logging
from typing import List, Optional, Dict, Any, Tuple
import strawberry # Required for strawberry.ID if used in type hints here, or Property type
from models.property_models import Property # Adjusted import path
from models.commute_models import (
    PropertyInfoForCommute,
    DirectWalkToUniversityProperty,
    StationInfo,
    PropertyNearUniversityStation,
    PaginatedPropertiesWithWalkTime,
    PaginatedPropertiesNearStation,
    # UniversityCommuteProfileResponse is built by the resolver
)
from config.university_data import CORE_UNIVERSITIES # Assuming this path
import math

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants for commute calculations
WALK_SPEED_MPS = 1.333  # meters per second (approx 80 m/min or 4.8 km/h)
UNIVERSITY_TO_STATION_WALK_RADIUS_M = 1000.0 # Max walk distance from Uni to a "core" station
PROPERTY_TO_STATION_WALK_RADIUS_M = 800.0   # Max walk distance from Property to a station

def _calculate_walk_time_minutes(distance_meters: float) -> int:
    """Calculates walk time in minutes, rounded up."""
    if distance_meters <= 0:
        return 0
    return math.ceil((distance_meters / WALK_SPEED_MPS) / 60)

def _map_row_to_property_info_for_commute(prop: Property) -> PropertyInfoForCommute:
    """Helper to map a Property object to PropertyInfoForCommute."""
    return PropertyInfoForCommute(
        listing_id=str(prop.listing_id), # Ensure it's string
        address=prop.address,
        suburb=prop.suburb,
        rent_pw=prop.rent_pw,
        bedrooms=prop.bedrooms,
        property_type=prop.property_type,
        latitude=prop.latitude,
        longitude=prop.longitude,
        images=prop.images
    )

# TEMPORARILY COMMENTING OUT ALL ENVIRONMENT VARIABLE LOADING FOR DEBUGGING
# dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
# load_dotenv(dotenv_path)

# Database connection parameters - TEMPORARILY HARDCODED FOR DEBUGGING
DB_NAME = "rental_mcp_db"
DB_USER = "etl_user"
DB_PASSWORD = "051130Ll" # Hardcoding the confirmed correct password
DB_HOST = "localhost"
DB_PORT = "5432"

logging.info(
    f"TEMPORARY DEBUG: All DB connection parameters are hardcoded. "
    f"DB_NAME='{DB_NAME}', DB_USER='{DB_USER}', "
    f"DB_PASSWORD_SET={'Yes' if DB_PASSWORD else 'No'} (length: {len(DB_PASSWORD) if DB_PASSWORD else 0}), "
    f"DB_HOST='{DB_HOST}', DB_PORT='{DB_PORT}'"
)

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    # Log details used for connection, masking password for security in regular operation
    logging.info(
        f"Attempting DB connection with USER='{DB_USER}', "
        f"PASSWORD_SET={'Yes' if DB_PASSWORD else 'No'}, " # Indicate if password is set
        f"HOST='{DB_HOST}', PORT='{DB_PORT}', DBNAME='{DB_NAME}'"
    )
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        logging.info("Database connection successful.")
        return conn
    except psycopg2.Error as e:
        logging.error(f"Error connecting to the database in CRUD: {e}")
        # Log failure details, still masking password
        logging.error(
            f"Failed DB connection attempt with USER='{DB_USER}', "
            f"PASSWORD_SET={'Yes' if DB_PASSWORD else 'No'}."
        )
        raise

def get_all_properties_from_db(
    suburb: Optional[str] = None,
    property_type: Optional[str] = None,
    min_bedrooms: Optional[int] = None,
    max_bedrooms: Optional[int] = None,
    min_rent_pw: Optional[int] = None,
    max_rent_pw: Optional[int] = None,
    available_after: Optional[datetime.date] = None,
    available_before: Optional[datetime.date] = None,
    limit: Optional[int] = 20, # Default from GQL schema
    offset: Optional[int] = 0, # Default from GQL schema
    sort_by: Optional[str] = None, 
    sort_direction: Optional[str] = "ASC"
) -> dict: # Changed return type to dict for items and totalCount
    """Fetches properties from the database with multiple filter options, sorting, and pagination."""
    conn = get_db_connection()
    properties_list = []
    params_data = [] # Parameters for the data query
    params_count = [] # Parameters for the count query
    
    select_clause = """
        SELECT 
            listing_id, address, suburb, rent_pw, bedrooms, bathrooms, property_type,
            property_url, postcode, bond, parking_spaces, 
            CAST(available_date AS TEXT), images, property_features, 
            latitude, longitude, ST_AsText(geom) AS geom_wkt
        FROM properties
    """
    count_select_clause = "SELECT COUNT(*) FROM properties"
    
    conditions = []
    # Build conditions and params for both data and count queries
    # Ensure params_data and params_count are populated identically for the WHERE clause
    if suburb:
        conditions.append("suburb ILIKE %s")
        params_data.append(f"%{suburb}%")
        params_count.append(f"%{suburb}%")
    
    if property_type:
        conditions.append("TRIM(LOWER(property_type)) LIKE TRIM(LOWER(%s))")
        params_data.append(f"%{property_type}%")
        params_count.append(f"%{property_type}%")
        logging.info(f"Filtering by property_type: {property_type}")
    
    if min_bedrooms is not None:
        conditions.append("bedrooms >= %s")
        params_data.append(min_bedrooms)
        params_count.append(min_bedrooms)
    
    if max_bedrooms is not None:
        conditions.append("bedrooms <= %s")
        params_data.append(max_bedrooms)
        params_count.append(max_bedrooms)
    
    if min_rent_pw is not None:
        conditions.append("rent_pw >= %s")
        params_data.append(min_rent_pw)
        params_count.append(min_rent_pw)
    
    if max_rent_pw is not None:
        conditions.append("rent_pw <= %s")
        params_data.append(max_rent_pw)
        params_count.append(max_rent_pw)
    
    if available_after is not None:
        conditions.append("available_date >= %s")
        params_data.append(available_after)
        params_count.append(available_after)
        logging.info(f"Filtering by available_after: {available_after}")
    
    if available_before is not None:
        conditions.append("available_date <= %s")
        params_data.append(available_before)
        params_count.append(available_before)
        logging.info(f"Filtering by available_before: {available_before}")

    where_clause_str = ""
    if conditions:
        where_clause_str = " WHERE " + " AND ".join(conditions)
        
    data_query = select_clause + where_clause_str
    count_query_str = count_select_clause + where_clause_str
    
    order_by_clause_str = " ORDER BY listing_id ASC" # Default sort
    if sort_by == "rentPw":
        order_by_clause_str = f" ORDER BY rent_pw {sort_direction}"
    
    data_query += order_by_clause_str
    
    if limit is not None:
        data_query += " LIMIT %s"
        params_data.append(limit)
    if offset is not None:
        data_query += " OFFSET %s"
        params_data.append(offset)

    total_count = 0
    try:
        with conn.cursor() as cur:
            # Execute count query
            logging.info(f"Executing count query: {count_query_str} with params: {params_count}")
            cur.execute(count_query_str, tuple(params_count))
            total_count_result = cur.fetchone()
            if total_count_result:
                total_count = total_count_result[0]
            logging.info(f"Total matching properties: {total_count}")

            # Execute data query
            logging.info(f"Executing data query: {data_query} with params: {params_data}")
            cur.execute(data_query, tuple(params_data))
            rows = cur.fetchall()
            for row in rows:
                properties_list.append(Property(
                    listing_id=strawberry.ID(str(row[0])),
                    address=row[1],
                    suburb=row[2],
                    rent_pw=row[3],
                    bedrooms=row[4],
                    bathrooms=row[5],
                    property_type=row[6],
                    property_url=row[7],
                    postcode=row[8],
                    bond=row[9],
                    parking_spaces=row[10],
                    available_date=row[11],
                    images=row[12],
                    property_features=row[13],
                    latitude=row[14],
                    longitude=row[15],
                    geom_wkt=row[16]
                ))
        logging.info(f"Fetched {len(properties_list)} properties for the current page.")
    except psycopg2.Error as e:
        logging.error(f"Error fetching all properties: {e}")
        # In case of error, return empty list and 0 count to avoid breaking GQL response
        return {"items": [], "totalCount": 0}
    finally:
        if conn:
            conn.close()
    return {"items": properties_list, "totalCount": total_count}

def get_property_by_id_from_db(listing_id: strawberry.ID) -> Optional[Property]:
    """Fetches a single property by its listing_id from the database."""
    conn = get_db_connection()
    prop = None
    try:
        with conn.cursor() as cur:
            # Expand selected fields
            query = """
                SELECT 
                    listing_id, address, suburb, rent_pw, bedrooms, bathrooms, property_type,
                    property_url, postcode, bond, parking_spaces, 
                    CAST(available_date AS TEXT), images, property_features, 
                    latitude, longitude, ST_AsText(geom) AS geom_wkt
                FROM properties 
                WHERE listing_id = %s
            """
            cur.execute(query, (int(listing_id),))
            row = cur.fetchone()
            if row:
                prop = Property(
                    listing_id=strawberry.ID(str(row[0])),
                    address=row[1],
                    suburb=row[2],
                    rent_pw=row[3],
                    bedrooms=row[4],
                    bathrooms=row[5],
                    property_type=row[6],
                    property_url=row[7],
                    postcode=row[8],
                    bond=row[9],
                    parking_spaces=row[10],
                    available_date=row[11], # Already cast to TEXT in query
                    images=row[12],
                    property_features=row[13],
                    latitude=row[14],
                    longitude=row[15],
                    geom_wkt=row[16]
                )
                logging.info(f"Fetched property with ID {listing_id} from DB.")
            else:
                logging.info(f"No property found with ID {listing_id} in DB.")
    except psycopg2.Error as e:
        logging.error(f"Error fetching property by ID {listing_id}: {e}")
    finally:
        if conn:
            conn.close()
    return prop

def get_properties_near_location_from_db(
    latitude: float, 
    longitude: float, 
    radius_km: float, 
    limit: Optional[int] = 20, # Default from GQL schema
    offset: Optional[int] = 0, # Default from GQL schema
    sort_by: Optional[str] = None, 
    sort_direction: Optional[str] = "ASC"
) -> dict: # Changed return type to dict
    """Fetches properties within a given radius (in km) from a central point with sorting and pagination."""
    conn = get_db_connection()
    properties_list = []
    radius_meters = radius_km * 1000.0
    
    # Base for data query
    data_query_base = """
        SELECT 
            listing_id, address, suburb, rent_pw, bedrooms, bathrooms, property_type,
            property_url, postcode, bond, parking_spaces, 
            CAST(available_date AS TEXT), images, property_features, 
            latitude, longitude, ST_AsText(geom) AS geom_wkt,
            ST_Distance(geom::geography, ST_MakePoint(%s, %s)::geography) AS distance_meters
        FROM properties
        WHERE ST_DWithin(geom::geography, ST_MakePoint(%s, %s)::geography, %s)
    """
    # Base for count query
    count_query_base = """
        SELECT COUNT(*)
        FROM properties
        WHERE ST_DWithin(geom::geography, ST_MakePoint(%s, %s)::geography, %s)
    """
    
    where_params_dwithin = [longitude, latitude, radius_meters]
    select_distance_params = [longitude, latitude]

    order_by_clause_str = " ORDER BY distance_meters ASC" 
    if sort_by == "rentPw":
        order_by_clause_str = f" ORDER BY rent_pw {sort_direction}, distance_meters ASC"
        
    data_query_str = data_query_base + order_by_clause_str
    
    params_data_list = select_distance_params + where_params_dwithin

    if limit is not None:
        data_query_str += " LIMIT %s"
        params_data_list.append(limit)
    if offset is not None:
        data_query_str += " OFFSET %s"
        params_data_list.append(offset)
        
    params_for_data_query = tuple(params_data_list)
    params_for_count_query = tuple(where_params_dwithin)

    total_count = 0
    try:
        with conn.cursor() as cur:
            logging.info(f"Executing count query for nearLocation: {count_query_base} with params: {params_for_count_query}")
            cur.execute(count_query_base, params_for_count_query)
            total_count_result = cur.fetchone()
            if total_count_result:
                total_count = total_count_result[0]
            logging.info(f"Total matching properties near location: {total_count}")

            logging.info(f"Executing data query for nearLocation: {data_query_str} with params: {params_for_data_query}")
            cur.execute(data_query_str, params_for_data_query)
            rows = cur.fetchall()
            for row_idx, row_data in enumerate(rows):
                properties_list.append(Property(
                    listing_id=strawberry.ID(str(row_data[0])),
                    address=row_data[1],
                    suburb=row_data[2],
                    rent_pw=row_data[3],
                    bedrooms=row_data[4],
                    bathrooms=row_data[5],
                    property_type=row_data[6],
                    property_url=row_data[7],
                    postcode=row_data[8],
                    bond=row_data[9],
                    parking_spaces=row_data[10],
                    available_date=row_data[11],
                    images=row_data[12],
                    property_features=row_data[13],
                    latitude=row_data[14],
                    longitude=row_data[15],
                    geom_wkt=row_data[16]
                    # distance_meters is row_data[17] but not directly part of Property model
                ))
        logging.info(f"Fetched {len(properties_list)} properties near location ({latitude}, {longitude}) within {radius_km} km for the current page.")
    except psycopg2.Error as e:
        logging.error(f"Error fetching properties near location: {e}")
        return {"items": [], "totalCount": 0}
    finally:
        if conn:
            conn.close()
    return {"items": properties_list, "totalCount": total_count}

# New function starts here
def fetch_university_commute_profile_data(
    university_name: str,
    limit_per_category: int,
    offset_per_category: int
) -> Optional[Dict[str, Any]]:
    """
    Fetches a commute profile for a given university, including direct walk options
    and properties connected via different transport modes.
    """
    uni_details = CORE_UNIVERSITIES.get(university_name)
    if not uni_details:
        logging.error(f"University details not found for: {university_name}")
        return None

    uni_lat = uni_details["latitude"]
    uni_lon = uni_details["longitude"]
    uni_direct_walk_radius_km = uni_details["direct_walk_radius_km"]
    uni_direct_walk_radius_m = uni_direct_walk_radius_km * 1000.0

    conn = get_db_connection()
    profile_result: Dict[str, Any] = {
        "university_name": university_name,
        "direct_walk_options": None,
        "light_rail_connected_properties": None,
        "train_connected_properties": None,
        "bus_connected_properties": None,
    }

    try:
        with conn.cursor() as cur:
            # 1. Direct Walk Options
            direct_walk_items: List[DirectWalkToUniversityProperty] = []
            
            # Query for properties within direct walk radius of university
            # Includes distance calculation
            # Note: ST_MakePoint expects longitude, latitude
            sql_direct_walk_props_base = """
                SELECT
                    p.listing_id, p.address, p.suburb, p.rent_pw, p.bedrooms, p.bathrooms, p.property_type,
                    p.property_url, p.postcode, p.bond, p.parking_spaces,
                    CAST(p.available_date AS TEXT), p.images, p.property_features,
                    p.latitude, p.longitude, ST_AsText(p.geom) AS geom_wkt,
                    ST_Distance(p.geom::geography, ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography) AS distance_to_uni_meters
                FROM properties p
                WHERE ST_DWithin(p.geom::geography, ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography, %s)
            """
            sql_direct_walk_count = """
                SELECT COUNT(*) FROM properties p
                WHERE ST_DWithin(p.geom::geography, ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography, %s)
            """
            
            direct_walk_params_where = (uni_lon, uni_lat, uni_direct_walk_radius_m)
            direct_walk_params_select_distance = (uni_lon, uni_lat)
            
            # Count for direct walk
            cur.execute(sql_direct_walk_count, direct_walk_params_where)
            total_direct_walk = cur.fetchone()[0] if cur.rowcount > 0 else 0

            # Data for direct walk
            sql_direct_walk_props_data = sql_direct_walk_props_base + " ORDER BY distance_to_uni_meters ASC LIMIT %s OFFSET %s"
            # Params: ST_Distance(lon,lat), ST_DWithin(lon,lat,radius), limit, offset
            cur.execute(sql_direct_walk_props_data, direct_walk_params_select_distance + direct_walk_params_where + (limit_per_category, offset_per_category))
            
            direct_walk_fetched_rows = cur.fetchall()
            for row in direct_walk_fetched_rows:
                # prop_obj = Property(*row[:17]) # Create Property object from first 17 fields
                # Corrected instantiation with keyword arguments:
                prop_obj = Property(
                    listing_id=strawberry.ID(str(row[0])),
                    address=row[1],
                    suburb=row[2],
                    rent_pw=row[3],
                    bedrooms=row[4],
                    bathrooms=row[5],
                    property_type=row[6],
                    property_url=row[7],
                    postcode=row[8],
                    bond=row[9],
                    parking_spaces=row[10],
                    available_date=row[11], # Already cast to TEXT in query
                    images=row[12],
                    property_features=row[13],
                    latitude=row[14],
                    longitude=row[15],
                    geom_wkt=row[16]
                )
                distance_m = row[17]
                walk_time_min = _calculate_walk_time_minutes(distance_m)
                direct_walk_items.append(
                    DirectWalkToUniversityProperty(
                        property_info=_map_row_to_property_info_for_commute(prop_obj),
                        walk_time_to_university_minutes=walk_time_min,
                        distance_to_university_km=round(distance_m / 1000, 2)
                    )
                )
            profile_result["direct_walk_options"] = PaginatedPropertiesWithWalkTime(
                items=direct_walk_items, total_count=total_direct_walk, limit=limit_per_category, offset=offset_per_category
            )
            logging.info(f"Direct walk: Found {total_direct_walk} properties, returning {len(direct_walk_items)} for {university_name}")

            # 2. Transport Connected Properties (Light Rail, Train, Bus)
            # Keys here must match the snake_case attributes of UniversityCommuteProfileResponse
            transport_modes_map = {
                "light_rail": "LIGHT_RAIL", # Match DB: LIGHT_RAIL
                "train": "TRAIN",           # Match DB: TRAIN
                "bus": "BUS"                # Match DB: BUS
            }

            for mode_key_snake_case, db_transport_mode in transport_modes_map.items():
                connected_properties_for_mode: List[PropertyNearUniversityStation] = []
                # Using a dictionary to handle deduplication: property_listing_id -> best PropertyNearUniversityStation
                deduped_props_for_mode: Dict[str, PropertyNearUniversityStation] = {}

                # Step 2a: Find core stations near university for the current mode
                sql_stations_near_uni = """
                    SELECT
                        ts.stop_id,
                        ts.stop_name,
                        ts.transport_mode,
                        ST_Distance(ts.location::geography, ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography) AS distance_uni_to_station_m,
                        ts.serviced_routes_details,
                        ts.latitude AS station_lat,
                        ts.longitude AS station_lon
                    FROM transport_stops ts
                    WHERE ts.transport_mode = %s
                      AND ST_DWithin(ts.location::geography, ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography, %s)
                    ORDER BY distance_uni_to_station_m ASC; 
                """ # Limit stations? For now, get all relevant ones.
                # Params: uni_lon, uni_lat, db_transport_mode, uni_lon, uni_lat, UNIVERSITY_TO_STATION_WALK_RADIUS_M
                cur.execute(sql_stations_near_uni, (uni_lon, uni_lat, db_transport_mode, uni_lon, uni_lat, UNIVERSITY_TO_STATION_WALK_RADIUS_M))
                core_stations_for_mode = cur.fetchall()
                logging.info(f"Mode {db_transport_mode}: Found {len(core_stations_for_mode)} core stations near {university_name}")

                all_properties_near_stations_of_mode: List[Tuple[Property, StationInfo, float]] = []

                for station_row in core_stations_for_mode:
                    station_id, station_name, station_transport_mode, _, serviced_routes_json, station_lat, station_lon = station_row
                    
                    routes_preview = []
                    if serviced_routes_json and 'routes' in serviced_routes_json:
                        for route_info in serviced_routes_json['routes']:
                            if 'shortName' in route_info:
                                routes_preview.append(route_info['shortName'])
                    
                    current_station_info = StationInfo(
                        stop_id=station_id,
                        stop_name=station_name,
                        transport_mode=station_transport_mode,
                        serviced_routes_preview=list(set(routes_preview))[:5] # Unique, limit to 5 for preview
                    )

                    # Step 2b: For each core station, find nearby properties
                    sql_props_near_station_base = """
                        SELECT
                            p.listing_id, p.address, p.suburb, p.rent_pw, p.bedrooms, p.bathrooms, p.property_type,
                            p.property_url, p.postcode, p.bond, p.parking_spaces,
                            CAST(p.available_date AS TEXT), p.images, p.property_features,
                            p.latitude, p.longitude, ST_AsText(p.geom) AS geom_wkt,
                            ST_Distance(p.geom::geography, ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography) AS distance_prop_to_station_m
                        FROM properties p
                        WHERE ST_DWithin(p.geom::geography, ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography, %s)
                        ORDER BY distance_prop_to_station_m ASC
                    """ # No pagination here yet, will apply after deduplication
                    # Params: station_lon, station_lat, station_lon, station_lat, PROPERTY_TO_STATION_WALK_RADIUS_M
                    cur.execute(sql_props_near_station_base, (station_lon, station_lat, station_lon, station_lat, PROPERTY_TO_STATION_WALK_RADIUS_M))
                    
                    props_near_current_station_rows = cur.fetchall()
                    for prop_row in props_near_current_station_rows:
                        # prop_obj = Property(*prop_row[:17])
                        # Corrected instantiation with keyword arguments:
                        prop_obj = Property(
                            listing_id=strawberry.ID(str(prop_row[0])),
                            address=prop_row[1],
                            suburb=prop_row[2],
                            rent_pw=prop_row[3],
                            bedrooms=prop_row[4],
                            bathrooms=prop_row[5],
                            property_type=prop_row[6],
                            property_url=prop_row[7],
                            postcode=prop_row[8],
                            bond=prop_row[9],
                            parking_spaces=prop_row[10],
                            available_date=prop_row[11], # Already cast to TEXT in query
                            images=prop_row[12],
                            property_features=prop_row[13],
                            latitude=prop_row[14],
                            longitude=prop_row[15],
                            geom_wkt=prop_row[16]
                        )
                        distance_prop_to_station_m = prop_row[17]
                        walk_time_prop_to_station_min = _calculate_walk_time_minutes(distance_prop_to_station_m)
                        
                        p_near_station = PropertyNearUniversityStation(
                            property_info=_map_row_to_property_info_for_commute(prop_obj),
                            connected_via_station=current_station_info,
                            walk_time_to_station_minutes=walk_time_prop_to_station_min
                        )

                        # Deduplication logic: if property already found via another station of the same mode,
                        # keep the one with the shorter walk time to *a* station.
                        listing_id_str = str(prop_obj.listing_id)
                        if listing_id_str not in deduped_props_for_mode or \
                           walk_time_prop_to_station_min < deduped_props_for_mode[listing_id_str].walk_time_to_station_minutes:
                            deduped_props_for_mode[listing_id_str] = p_near_station
                
                # After checking all stations for the current mode, get the final list of unique properties
                final_items_for_mode = sorted(list(deduped_props_for_mode.values()), key=lambda x: x.walk_time_to_station_minutes)
                total_for_mode = len(final_items_for_mode)
                paginated_items_for_mode = final_items_for_mode[offset_per_category : offset_per_category + limit_per_category]

                # 直接使用预定义的键名，避免任何名称构造问题
                if mode_key_snake_case == "light_rail":
                    profile_result_key = "light_rail_connected_properties"
                elif mode_key_snake_case == "train":
                    profile_result_key = "train_connected_properties"
                elif mode_key_snake_case == "bus":
                    profile_result_key = "bus_connected_properties"
                else:
                    profile_result_key = f"{mode_key_snake_case}_connected_properties"
                
                # DEBUGGING PRINT STATEMENT ADDED HERE
                logging.info(f"DEBUG: Constructing profile_result with key: '{profile_result_key}' for mode '{db_transport_mode}'")
                
                profile_result[profile_result_key] = PaginatedPropertiesNearStation(
                    items=paginated_items_for_mode, total_count=total_for_mode, limit=limit_per_category, offset=offset_per_category
                )
                logging.info(f"Mode {db_transport_mode}: Found {total_for_mode} unique properties, returning {len(paginated_items_for_mode)} for {university_name} under key {profile_result_key}")

    except psycopg2.Error as e:
        logging.error(f"Database error in fetch_university_commute_profile_data for {university_name}: {e}")
        # Depending on desired behavior, could return partial results or None
        return None # Or re-raise, or return profile_result with whatever was populated
    except Exception as e:
        logging.error(f"Unexpected error in fetch_university_commute_profile_data for {university_name}: {e}")
        return None
    finally:
        if conn:
            conn.close()
            
    return profile_result
