from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import List

# Use the actual schema from graphql_schema.py
from server.api.graphql_schema import schema

# Create FastAPI app with GraphQL router
app = FastAPI()
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
    return {"message": "TEST SERVER - BRAND NEW FILE"}

import pytest
from fastapi.testclient import TestClient

def test_query_properties():
    client = TestClient(app)
    query = """
    query ($suburb: String) { # Changed to optional as per schema for allProperties
        allProperties(suburb: $suburb, limit: 1) { # Using allProperties and adding a limit
            listingId # Changed id to listingId as per Property model
            address # Changed name to address as per Property model
            suburb
        }
    }
    """
    variables = {"suburb": "Sydney"} # Keep suburb for testing, can be None
    response = client.post("/graphql", json={"query": query, "variables": variables})
    assert response.status_code == 200
    data = response.json()
    
    # Adjust assertions based on the actual fields of Property model
    # and the behavior of allProperties
    assert "data" in data
    assert "allProperties" in data["data"]
    assert isinstance(data["data"]["allProperties"], list)
    if data["data"]["allProperties"]: # Check if any property is returned
        first_property = data["data"]["allProperties"][0]
        assert "listingId" in first_property
        assert "address" in first_property
        assert "suburb" in first_property
        # If suburb was provided and results are found, check it (case-insensitive)
        if variables.get("suburb") and first_property.get("suburb"):
             assert variables["suburb"].lower() in first_property["suburb"].lower()
    else:
        # Handle case where no properties are found for the given suburb
        print(f"No properties found for suburb: {variables.get('suburb')}")


def test_query_properties_near_location():
    client = TestClient(app)
    query = """
    query ($latitude: Float!, $longitude: Float!, $radiusKm: Float!) {
        propertiesNearLocation(latitude: $latitude, longitude: $longitude, radiusKm: $radiusKm) {
            listingId
            address
            suburb
            rentPw
            bedrooms
            # Add other fields you expect to receive
        }
    }
    """
    # Example coordinates (Sydney CBD) and radius
    variables = {
        "latitude": -33.8688,
        "longitude": 151.2093,
        "radiusKm": 5.0 
    }
    response = client.post("/graphql", json={"query": query, "variables": variables})
    assert response.status_code == 200
    data = response.json()
    
    # Basic check: Ensure the query executed and returned data
    assert "data" in data
    assert "propertiesNearLocation" in data["data"]
    
    # Further checks can be added here, e.g.,
    # - Check if the number of results is as expected (if known)
    # - Check if specific properties are returned (if data is seeded/mocked)
    # - Check if properties are within the radius (requires more complex logic or DB verification)
    
    # For now, just log the number of results
    print(f"Found {len(data['data']['propertiesNearLocation'])} properties near location.")
    # Example: Assert that at least one property is returned if you expect results
    # This depends on your test database having relevant data.
    # For a generic test, you might just check that the list is not None.
    assert isinstance(data["data"]["propertiesNearLocation"], list)
