"""
CRUD operations for university commute profile related data.

This module will contain functions to:
- Fetch properties based on direct walking distance to a university.
- Fetch properties serviceable by public transport hubs near a university.
- Combine and process data from various sources to build the commute profile.
"""
import logging
from typing import List, Optional, Dict, Any
# Placeholder for database connection/pool if needed directly
# from asyncpg.pool import PoolNamespace

# Import models and types from graphql_schema or property_models as needed
# For example, if returning PaginatedCommuteProperties or CommuteProperty directly from here
# from server.api.graphql_schema import PaginatedCommuteProperties, CommuteProperty, UniversityCommuteProfile
# from server.models.property_models import Property as DBProperty
# from server.models.commute_models import UniversityNameEnum # If needed
import math
import psycopg2 # For psycopg2.Error
from models.property_models import Property # Assuming this is a Pydantic model or dataclass for DB rows
# CommuteProperty and PaginatedCommuteProperties are GraphQL types, so we'll return dicts matching their structure.
# from server.api.graphql_schema import CommuteProperty, PaginatedCommuteProperties

# Placeholder for the main function that will be called by the resolver
async def fetch_full_university_commute_profile( # This might also need to become sync if it calls the sync CRUD
    # db_pool: PoolNamespace, # Example: if db pool is passed from resolver via info.context
    university_name: str, # Or UniversityNameEnum.value
    limit_per_category: int,
    offset_per_category: int,
    filters: Dict[str, Any] # To pass min_rent_pw, etc.
) -> Dict[str, Any]: # This will eventually be structured to match UniversityCommuteProfile
    """
    Fetches and assembles the complete university commute profile.
    This function will orchestrate calls to more specific data fetching functions
    (e.g., for direct walk, light rail, train, bus options).
    """
    logging.info(f"CRUD: Starting fetch_full_university_commute_profile for {university_name}")
    
    # TODO:
    # 1. Get university coordinates using server.config.university_data.get_university_coordinates
    # 2. Call a function to get direct walk properties.
    # 3. Call functions to get properties via different transport modes (light rail, train, bus).
    #    - This will involve getting core transport hubs for the university.
    #    - Then finding properties near those hubs.
    #    - Then calculating travel times from hubs to university.
    # 4. Consolidate all results.
    # 5. Apply pagination and filters to each category of results.
    # 6. Structure the data to match the UniversityCommuteProfile GraphQL type.

    # Placeholder return
    return {
        "directWalkOptions": {"items": [], "totalCount": 0},
        "lightRailConnectedOptions": {"items": [], "totalCount": 0},
        "trainConnectedOptions": {"items": [], "totalCount": 0},
        "busConnectedOptions": {"items": [], "totalCount": 0},
    }

# Future functions for specific parts of the logic can be added here, e.g.:
# async def get_direct_walk_properties_crud(...) -> PaginatedCommuteProperties:
#     pass

# async def get_transport_connected_properties_crud(...) -> PaginatedCommuteProperties:
#     pass

def get_direct_walk_properties_crud( # Changed to sync
    db_conn: Any, # Represents a psycopg2 connection object
    university_latitude: float,
    university_longitude: float,
    radius_km: float,
    limit: int,
    offset: int,
    filters: Dict[str, Any]
) -> Dict[str, Any]: # Returns a dict matching PaginatedCommuteProperties structure
    """
    Fetches properties within direct walking distance of a university using psycopg2.

    Args:
        db_conn: psycopg2 database connection object.
        university_latitude: Latitude of the university.
        university_longitude: Longitude of the university.
        radius_km: Walking radius in kilometers.
        limit: Max number of properties to return.
        offset: Number of properties to skip.
        filters: Dictionary of additional property filters.

    Returns:
        A dictionary matching the PaginatedCommuteProperties GraphQL type structure.
    """
    logging.info(
        f"CRUD: Fetching direct walk properties for uni at {university_latitude},{university_longitude} "
        f"within {radius_km}km. Limit: {limit}, Offset: {offset}, Filters: {filters}"
    )

    # a. Prepare work
    radius_meters = radius_km * 1000
    
    # Parameters for the WHERE clause, starting with ST_DWithin's needs
    # ST_MakePoint(%s, %s) -> lon, lat for university
    # ST_DWithin(geom, ST_MakePoint, %s) -> radius_meters
    query_params_for_where = [university_longitude, university_latitude, radius_meters]
    
    # b. Dynamically build filter clauses for the WHERE clause
    where_clauses = [f"ST_DWithin(p.geom, ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s)"] 

    valid_filters_map = {
        "min_rent_pw": ("p.rent_pw", ">="), "max_rent_pw": ("p.rent_pw", "<="),
        "min_bedrooms": ("p.bedrooms", ">="), "max_bedrooms": ("p.bedrooms", "<="),
        "property_type": ("p.property_type", "ILIKE"), "suburb": ("p.suburb", "ILIKE"),
    }

    for key, value in filters.items():
        if key in valid_filters_map and value is not None:
            column, operator = valid_filters_map[key]
            where_clauses.append(f"{column} {operator} %s")
            if operator == "ILIKE":
                query_params_for_where.append(f"%{value}%")
            else:
                query_params_for_where.append(value)
    
    full_where_clause = " AND ".join(where_clauses)

    total_count = 0
    commute_properties_list = []

    try:
        with db_conn.cursor() as cursor:
            # c. Query total record count
            count_sql = f"SELECT COUNT(p.listing_id) FROM properties p WHERE {full_where_clause};"
            logging.debug(f"Count SQL attempt: {cursor.mogrify(count_sql, tuple(query_params_for_where)).decode('utf-8', errors='ignore') if hasattr(cursor, 'mogrify') else count_sql}")
            cursor.execute(count_sql, tuple(query_params_for_where))
            total_count_record = cursor.fetchone()
            total_count = total_count_record[0] if total_count_record else 0
            logging.info(f"CRUD: Total direct walk properties found (pre-pagination): {total_count}")

            if total_count == 0:
                return {"items": [], "totalCount": 0}

            # d. Query paginated data
            # Parameters for ST_Distance (lon, lat)
            params_for_st_distance = [university_longitude, university_latitude]
            # Parameters for pagination (limit, offset)
            params_for_pagination = [limit, offset]
            
            # final_execute_params for data_sql:
            # ST_Distance params + WHERE clause params (which includes ST_DWithin params & filter params) + Pagination params
            final_execute_params = params_for_st_distance + query_params_for_where + params_for_pagination
            
            data_sql = f"""
                SELECT 
                    p.listing_id, p.address, p.suburb, p.rent_pw, p.bedrooms, p.bathrooms, 
                    p.property_type, p.property_url, p.postcode, p.bond, p.parking_spaces, 
                    p.available_date, p.images, p.property_features, p.latitude, p.longitude, 
                    ST_AsText(p.geom) AS geom_wkt,
                    ST_Distance(
                        p.geom,
                        ST_SetSRID(ST_MakePoint(%s, %s), 4326) -- for ST_Distance
                    ) AS distance_meters
                FROM properties p
                WHERE {full_where_clause} -- for ST_DWithin and filters
                ORDER BY distance_meters ASC
                LIMIT %s OFFSET %s; -- for pagination
            """
            logging.debug(f"Data SQL attempt: {cursor.mogrify(data_sql, tuple(final_execute_params)).decode('utf-8', errors='ignore') if hasattr(cursor, 'mogrify') else data_sql}")
            cursor.execute(data_sql, tuple(final_execute_params))
            property_rows = cursor.fetchall()

            # e. Data conversion
            column_names = [desc[0] for desc in cursor.description]
            for row in property_rows:
                row_dict = dict(zip(column_names, row))

                db_property_dict = {
                    "listing_id": str(row_dict['listing_id']),
                    "address": row_dict['address'],
                    "suburb": row_dict['suburb'],
                    "rent_pw": row_dict['rent_pw'],
                    "bedrooms": row_dict['bedrooms'],
                    "bathrooms": row_dict['bathrooms'],
                    "property_type": row_dict['property_type'],
                    "property_url": row_dict['property_url'],
                    "postcode": row_dict['postcode'],
                    "bond": row_dict['bond'],
                    "parking_spaces": row_dict['parking_spaces'],
                    "available_date": row_dict['available_date'], # Keep as date object if it is
                    "images": row_dict['images'],
                    "property_features": row_dict['property_features'],
                    "latitude": row_dict['latitude'],
                    "longitude": row_dict['longitude'],
                    "geom_wkt": row_dict['geom_wkt']
                }

                distance_meters = row_dict.get('distance_meters')
                distance_km = None
                walk_time_minutes = None
                if distance_meters is not None:
                    distance_km = distance_meters / 1000.0
                    walk_time_minutes = math.ceil(distance_meters / 80)

                commute_prop_dict = {
                    "property": db_property_dict,
                    "walkTimeToUniversityMinutes": walk_time_minutes,
                    "distanceToUniversityKm": round(distance_km, 2) if distance_km is not None else None,
                    "walkToStationMinutes": None,
                    "stationName": None,
                    "stationTransportMode": None,
                    "stationServicedRoutes": None,
                    "stationToUniversityWalkMinutes": None
                }
                commute_properties_list.append(commute_prop_dict)
        
        # f. Return result
        return {"items": commute_properties_list, "totalCount": total_count}

    except psycopg2.Error as e:
        logging.error(f"Database error in get_direct_walk_properties_crud: {e}", exc_info=True)
        if db_conn: 
            try:
                db_conn.rollback()
            except Exception as rb_e: 
                logging.error(f"Error during rollback: {rb_e}", exc_info=True)
        return {"items": [], "totalCount": 0}
    except Exception as e:
        logging.error(f"Unexpected error in get_direct_walk_properties_crud: {e}", exc_info=True)
        return {"items": [], "totalCount": 0}
    # Removed finally block as 'with' statement handles cursor closing.
