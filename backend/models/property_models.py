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
    # Fields like inspection_times, agency details can be added later if needed
