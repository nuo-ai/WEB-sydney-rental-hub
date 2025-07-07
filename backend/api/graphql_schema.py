import strawberry
import datetime
import logging
from typing import List, Optional, Any # Added Any for db_conn type hint if needed
from enum import Enum as PythonEnum
import asyncio # Added import
from strawberry.schema.config import StrawberryConfig

from models.property_models import Property # GraphQL type
from models.commute_models import (
    UniversityNameEnum
    # UniversityCommuteProfileResponse, # Likely removable now
)
from config.university_data import get_university_coordinates, CORE_UNIVERSITIES
from crud.commute_crud import get_direct_walk_properties_crud # Specific import
from crud.properties_crud import (
    get_all_properties_from_db,
    get_property_by_id_from_db,
    get_properties_near_location_from_db,
    fetch_university_commute_profile_data # Placeholder for the new CRUD function
)

@strawberry.enum
class PropertySortByField(PythonEnum): # Using PythonEnum base
    RENT_PW = "rent_pw"
    # AVAILABLE_DATE = "available_date" # Explicitly not adding for 1.0

@strawberry.enum
class SortDirection(PythonEnum): # Using PythonEnum base
    ASC = "ASC"
    DESC = "DESC"

@strawberry.type
class PaginatedProperties:
    items: List[Property]
    totalCount: int

@strawberry.type
class CommuteProperty:
    property: Property
    walkTimeToUniversityMinutes: Optional[int]
    distanceToUniversityKm: Optional[float]
    walkToStationMinutes: Optional[int]
    stationName: Optional[str]
    stationTransportMode: Optional[str]
    stationServicedRoutes: Optional[List[str]]
    stationToUniversityWalkMinutes: Optional[int]

@strawberry.type
class PaginatedCommuteProperties:
    items: List[CommuteProperty]
    totalCount: int

@strawberry.type
class UniversityCommuteProfile:
    directWalkOptions: PaginatedCommuteProperties
    lightRailConnectedOptions: PaginatedCommuteProperties
    trainConnectedOptions: PaginatedCommuteProperties
    busConnectedOptions: PaginatedCommuteProperties

@strawberry.type
class Query:
    @strawberry.field
    def all_properties(
        self,
        suburb: Optional[str] = None,
        propertyType: Optional[str] = None,
        minBedrooms: Optional[int] = None,
        maxBedrooms: Optional[int] = None,
        minRentPw: Optional[int] = None,
        maxRentPw: Optional[int] = None,
        availableAfter: Optional[datetime.date] = None,
        availableBefore: Optional[datetime.date] = None,
        limit: Optional[int] = 20, #strawberry.argument(default_value=20, description="Number of items to return per page."),
        offset: Optional[int] = 0, #strawberry.argument(default_value=0, description="Number of items to skip for pagination."),
        sortBy: Optional[PropertySortByField] = None,
        sortDirection: Optional[SortDirection] = SortDirection.ASC
    ) -> PaginatedProperties:
        result = get_all_properties_from_db(
            suburb=suburb,
            property_type=propertyType,
            min_bedrooms=minBedrooms,
            max_bedrooms=maxBedrooms,
            min_rent_pw=minRentPw,
            max_rent_pw=maxRentPw,
            available_after=availableAfter,
            available_before=availableBefore,
            limit=limit,
            offset=offset, # Added offset
            sort_by=sortBy.value if sortBy else None,
            sort_direction=sortDirection.value if sortDirection else SortDirection.ASC.value
        )
        return PaginatedProperties(items=result["items"], totalCount=result["totalCount"])

    @strawberry.field
    def property_by_id(self, listing_id: strawberry.ID) -> Optional[Property]:
        return get_property_by_id_from_db(listing_id=str(listing_id)) # Ensure listing_id is string

    @strawberry.field(name="propertiesNearLocation")
    def properties_near_location(
        self,
        latitude: float,
        longitude: float,
        radiusKm: float,
        limit: Optional[int] = 20,
        offset: Optional[int] = 0,
        sortBy: Optional[PropertySortByField] = None,
        sortDirection: Optional[SortDirection] = SortDirection.ASC
    ) -> PaginatedProperties:
        result = get_properties_near_location_from_db(
            latitude=latitude,
            longitude=longitude,
            radius_km=radiusKm,
            limit=limit,
            offset=offset,
            sort_by=sortBy.value if sortBy else None,
            sort_direction=sortDirection.value if sortDirection else SortDirection.ASC.value
        )
        return PaginatedProperties(items=result["items"], totalCount=result["totalCount"])

    @strawberry.field
    async def get_university_commute_profile( # Added async
        self,
        info: strawberry.Info, # Added info parameter
        university_name: UniversityNameEnum,
        limit: Optional[int] = 10, # Corrected default value assignment
        offset: Optional[int] = 0, # Corrected default value assignment
        min_rent_pw: Optional[int] = None, # Corrected default value assignment
        max_rent_pw: Optional[int] = None, # Corrected default value assignment
        min_bedrooms: Optional[int] = None, # Corrected default value assignment
        property_type: Optional[str] = None # Corrected default value assignment
    ) -> UniversityCommuteProfile:
        # Step 1: Get university coordinates
        logging.info(f"Resolver: Fetching coordinates for {university_name.value}")
        coordinates = get_university_coordinates(university_name.value) # Use .value for Enum
        if not coordinates:
            logging.error(f"Resolver: University '{university_name.value}' not found in configuration.")
            raise strawberry.GraphQLError(f"University '{university_name.value}' not found.")
        
        uni_latitude = coordinates["latitude"]
        uni_longitude = coordinates["longitude"]
        logging.info(f"Resolver: Coordinates for {university_name.value}: Lat={uni_latitude}, Lon={uni_longitude}")

        # Placeholder for calling commute_crud.py and assembling the response
        # For now, we'll return a dummy/empty profile
        # This will be replaced by actual call to commute_crud.fetch_full_university_commute_profile
        
        # Example of how filters would be collected:
        # property_filters = {
        #     "min_rent_pw": min_rent_pw,
        #     "max_rent_pw": max_rent_pw,
        #     "min_bedrooms": min_bedrooms,
        #     "property_type": property_type,
        # }
        
        # TODO: Call the main CRUD function from commute_crud.py
        # from server.crud import commute_crud # Import when ready
        # profile_data = await commute_crud.fetch_full_university_commute_profile(
        #     university_name=university_name.value,
        #     limit_per_category=limit, # Note: parameter name mapping
        #     offset_per_category=offset, # Note: parameter name mapping
        #     filters=property_filters
        # )
        # return UniversityCommuteProfile(**profile_data) # Or however it's structured

        # Step 2: Initialize the result object
        result = UniversityCommuteProfile(
            directWalkOptions=PaginatedCommuteProperties(items=[], totalCount=0),
            lightRailConnectedOptions=PaginatedCommuteProperties(items=[], totalCount=0),
            trainConnectedOptions=PaginatedCommuteProperties(items=[], totalCount=0),
            busConnectedOptions=PaginatedCommuteProperties(items=[], totalCount=0)
        )

        # TODO: Populate result.directWalkOptions, result.lightRailConnectedOptions, etc.
        # by calling functions in commute_crud.py

        # Get synchronous database connection from context (placeholder)
        # PLEASE REPLACE THIS WITH YOUR ACTUAL WAY OF GETTING A SYNC DB CONNECTION
        sync_db_conn: Optional[Any] = info.context.get('sync_db_conn') 
        if not sync_db_conn:
            logging.error("Resolver: Synchronous database connection ('sync_db_conn') not found in context.")
            raise strawberry.GraphQLError("Internal server error: DB connection not configured correctly.")

        # Prepare filters for the CRUD function, only including non-None values
        property_filters = {}
        if min_rent_pw is not None:
            property_filters["min_rent_pw"] = min_rent_pw
        if max_rent_pw is not None:
            property_filters["max_rent_pw"] = max_rent_pw
        if min_bedrooms is not None:
            property_filters["min_bedrooms"] = min_bedrooms
        if property_type is not None:
            property_filters["property_type"] = property_type
        
        # Get walk radius for the university
        uni_key = university_name.value.upper()
        uni_config = CORE_UNIVERSITIES.get(uni_key)
        # Coordinates check already happened, so uni_config should exist.
        # If direct_walk_radius_km is missing, use a default or raise error.
        if not uni_config or "direct_walk_radius_km" not in uni_config:
            logging.warning(f"Resolver: 'direct_walk_radius_km' not configured for university {uni_key}. Using default 1.0km.")
            walk_radius_km = 1.0 
        else:
            walk_radius_km = uni_config["direct_walk_radius_km"]
        logging.info(f"Resolver: Using walk_radius_km={walk_radius_km} for {university_name.value}")

        # Call the synchronous CRUD function in a separate thread
        try:
            direct_walk_result_dict = await asyncio.to_thread(
                get_direct_walk_properties_crud,
                db_conn=sync_db_conn,
                university_latitude=uni_latitude,
                university_longitude=uni_longitude,
                radius_km=walk_radius_km,
                limit=limit,
                offset=offset,
                filters=property_filters
            )
        except Exception as e:
            logging.error(f"Resolver: Error calling get_direct_walk_properties_crud: {e}", exc_info=True)
            # Depending on how db_conn is managed, you might need to ensure it's closed/released
            # For now, assume asyncio.to_thread handles thread-local resources or db_conn is managed elsewhere
            raise strawberry.GraphQLError("Error fetching direct walk properties.")


        # Process the dictionary returned by CRUD and build GraphQL types
        processed_commute_properties = []
        if direct_walk_result_dict and isinstance(direct_walk_result_dict.get("items"), list):
            for item_dict in direct_walk_result_dict["items"]:
                prop_data = item_dict.get("property", {})
                
                # Instantiate Property GraphQL type
                # Ensure available_date (datetime.date from CRUD) is converted to str for GraphQL Property type
                gql_property = Property(
                    listing_id=strawberry.ID(prop_data.get("listing_id", "")),
                    address=prop_data.get("address"),
                    suburb=prop_data.get("suburb"),
                    rent_pw=prop_data.get("rent_pw"),
                    bedrooms=prop_data.get("bedrooms"),
                    bathrooms=prop_data.get("bathrooms"),
                    property_type=prop_data.get("property_type"),
                    property_url=prop_data.get("property_url"),
                    postcode=prop_data.get("postcode"),
                    bond=prop_data.get("bond"),
                    parking_spaces=prop_data.get("parking_spaces"),
                    available_date=str(prop_data["available_date"]) if prop_data.get("available_date") else None,
                    images=prop_data.get("images"), # Assuming JSON compatible
                    property_features=prop_data.get("property_features"), # Assuming JSON compatible
                    latitude=prop_data.get("latitude"),
                    longitude=prop_data.get("longitude"),
                    geom_wkt=prop_data.get("geom_wkt")
                )
                
                # Instantiate CommuteProperty GraphQL type
                gql_commute_property = CommuteProperty(
                    property=gql_property,
                    walkTimeToUniversityMinutes=item_dict.get("walkTimeToUniversityMinutes"),
                    distanceToUniversityKm=item_dict.get("distanceToUniversityKm"),
                    walkToStationMinutes=item_dict.get("walkToStationMinutes"),
                    stationName=item_dict.get("stationName"),
                    stationTransportMode=item_dict.get("stationTransportMode"),
                    stationServicedRoutes=item_dict.get("stationServicedRoutes"),
                    stationToUniversityWalkMinutes=item_dict.get("stationToUniversityWalkMinutes")
                )
                processed_commute_properties.append(gql_commute_property)
        
        result.directWalkOptions = PaginatedCommuteProperties(
            items=processed_commute_properties,
            totalCount=direct_walk_result_dict.get("totalCount", 0) if direct_walk_result_dict else 0
        )

        # Other options (lightRail, train, bus) remain as initialized (empty)
        # TODO: Implement calls for other transport options

        return result


    # Future: Add more queries here
    # e.g., properties_by_suburb etc.

# 导出 schema 供 main.py 使用
schema = strawberry.Schema(
    query=Query,
    config=StrawberryConfig(auto_camel_case=False)
)
