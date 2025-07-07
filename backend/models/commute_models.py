import strawberry
from typing import List, Optional, NewType
from .property_models import Property  # Assuming Property is defined here

# Define a new type for Listing ID for clarity, if not already globally defined
ListingId = NewType("ListingId", str)

@strawberry.type
class PropertyInfoForCommute:
    listing_id: strawberry.ID # Changed from ListingId to strawberry.ID
    address: str
    suburb: str
    rent_pw: float
    bedrooms: int
    property_type: str
    latitude: float
    longitude: float
    images: Optional[List[str]] # Or just the first image: Optional[str]

    @strawberry.field
    def first_image(self) -> Optional[str]:
        if self.images and len(self.images) > 0:
            return self.images[0]
        return None

@strawberry.type
class DirectWalkToUniversityProperty:
    property_info: PropertyInfoForCommute
    walk_time_to_university_minutes: int
    distance_to_university_km: float

@strawberry.type
class StationInfo:
    stop_id: str # Added stop_id for potential future use
    stop_name: str
    transport_mode: str
    # walk_to_university_minutes: int # This seems more relevant if station is linked to uni
    serviced_routes_preview: Optional[List[str]]

@strawberry.type
class PropertyNearUniversityStation:
    property_info: PropertyInfoForCommute
    connected_via_station: StationInfo
    walk_time_to_station_minutes: int
    # Optional: walk_time_station_to_university_minutes: int # If you calculate and pass this

@strawberry.type
class PaginatedPropertiesWithWalkTime:
    items: List[DirectWalkToUniversityProperty]
    total_count: int
    limit: int
    offset: int

@strawberry.type
class PaginatedPropertiesNearStation:
    items: List[PropertyNearUniversityStation]
    total_count: int
    limit: int
    offset: int

@strawberry.type
class UniversityCommuteProfileResponse:
    university_name: str
    direct_walk_options: Optional[PaginatedPropertiesWithWalkTime]
    light_rail_connected_properties: Optional[PaginatedPropertiesNearStation]
    train_connected_properties: Optional[PaginatedPropertiesNearStation]
    bus_connected_properties: Optional[PaginatedPropertiesNearStation]

import enum # Import the standard enum module

# You might need an Enum for University Names if not already defined
# This should ideally be dynamically generated or synced with your config
@strawberry.enum
class UniversityNameEnum(enum.Enum): # Inherit from enum.Enum
    UNSW = "UNSW"
    USYD = "USYD"
    UTS = "UTS"
    MQ = "MQ"
    WSU = "WSU" # Western Sydney University
    # Add other universities from your CORE_UNIVERSITIES config
