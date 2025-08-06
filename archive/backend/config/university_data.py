# server/config/university_data.py

CORE_UNIVERSITIES = {
    "UNSW": {
        "name": "University of New South Wales",
        "latitude": -33.9173,
        "longitude": 151.2313,
        "direct_walk_radius_km": 1.5  # Default direct walk radius in kilometers
    },
    "USYD": {
        "name": "University of Sydney",
        "latitude": -33.8887,
        "longitude": 151.1873,
        "direct_walk_radius_km": 1.5
    },
    "UTS": {
        "name": "University of Technology Sydney",
        "latitude": -33.8839,
        "longitude": 151.2007,
        "direct_walk_radius_km": 1.0
    },
    "MQ": {
        "name": "Macquarie University",
        "latitude": -33.7739,
        "longitude": 151.1124,
        "direct_walk_radius_km": 1.5
    },
    "WSU": { # Changed WSU_PARAMATTA to WSU to match Enum
        "name": "Western Sydney University - Parramatta City", # Assuming WSU refers to Parramatta
        "latitude": -33.8150, # Approximate, please verify
        "longitude": 151.0000, # Approximate, please verify
        "direct_walk_radius_km": 1.2
    }
    # Add other universities and their details here
    # The keys ("UNSW", "USYD", etc.) should match UniversityNameEnum
}

# You can add other configuration related to universities here if needed

def get_university_coordinates(university_name: str) -> dict | None:
    """
    Retrieves the latitude and longitude for a given university name.

    Args:
        university_name: The name/key of the university (e.g., "UNSW", "USYD").
                         The lookup is case-insensitive.

    Returns:
        A dictionary containing "latitude" and "longitude" if the university
        is found, otherwise None.
    """
    uni_key = university_name.upper() # Convert to uppercase to match keys in CORE_UNIVERSITIES
    university_data = CORE_UNIVERSITIES.get(uni_key)
    
    if university_data and "latitude" in university_data and "longitude" in university_data:
        return {
            "latitude": university_data["latitude"],
            "longitude": university_data["longitude"]
        }
    return None
