import strawberry
from typing import Optional
from strawberry.scalars import JSON # Import the JSON scalar

@strawberry.type
class Property:
    listing_id: strawberry.ID
    address: Optional[str] = None
    suburb: Optional[str] = None
    rent_pw: Optional[int] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    property_type: Optional[str] = None
    property_url: Optional[str] = None
    postcode: Optional[str] = None
    # state: Optional[str] = None # Already in DB, can add if needed
    bond: Optional[int] = None
    parking_spaces: Optional[int] = None
    available_date: Optional[str] = None # Using str for simplicity, can be strawberry.Date
    images: Optional[JSON] = None # For JSONB from DB
    property_features: Optional[JSON] = None # For JSONB from DB
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    geom_wkt: Optional[str] = None # To return geometry as WKT string

    # Existing boolean features from DB
    has_air_conditioning: Optional[bool] = None
    is_furnished: Optional[bool] = None
    has_balcony: Optional[bool] = None
    has_dishwasher: Optional[bool] = None
    has_laundry: Optional[bool] = None
    has_built_in_wardrobe: Optional[bool] = None
    has_gym: Optional[bool] = None
    has_pool: Optional[bool] = None
    has_parking: Optional[bool] = None
    allows_pets: Optional[bool] = None
    has_security_system: Optional[bool] = None
    has_storage: Optional[bool] = None
    has_study_room: Optional[bool] = None
    has_garden: Optional[bool] = None

    # Newly added boolean features
    has_intercom: Optional[bool] = None
    has_gas: Optional[bool] = None
    has_heating: Optional[bool] = None
    has_ensuite: Optional[bool] = None
    is_north_facing: Optional[bool] = None
    is_newly_built: Optional[bool] = None
    has_water_view: Optional[bool] = None

    # Newly added text features
    furnishing_status: Optional[str] = None
    air_conditioning_type: Optional[str] = None
    description: Optional[str] = None # <-- This was missing
    property_headline: Optional[str] = None # 房源标题，如"RENOVATED, SPACIOUS & CLOSE TO TRAIN & SHOPS!"
