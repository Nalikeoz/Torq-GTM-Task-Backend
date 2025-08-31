import ipaddress
from fastapi import APIRouter, Query
from pydantic import IPvAnyAddress
from app.schemas.location import LocationResponse
from app.core.config import settings

router = APIRouter(prefix="/v1", tags=["location"])

@router.get("/find-country", response_model=LocationResponse)
async def find_country(ip: IPvAnyAddress = Query(..., description="IP address to look up")):
    """
    Get country information for a given IP address.    
    Args:
        ip: The IP address to look up
    Returns:
        LocationResponse: Contains the IP address and a confirmation message
    """
    ip_address = str(ip)
    ip_location = settings.ip_to_location_service.get_location(ip_address)
    
    # Extract country name from IP2Location response
    country_name = getattr(ip_location, 'country_long', 'Unknown')
    city_name = getattr(ip_location, 'city', 'Unknown')
    
    return LocationResponse(
        country=country_name,
        city=city_name
    )
