import ipaddress
from fastapi import APIRouter, Query, HTTPException
from pydantic import IPvAnyAddress
from app.schemas.location import LocationResponse
from app.core.config import settings
from http import HTTPStatus


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
    try:
        ip_address = str(ip)
        ip_object = ipaddress.ip_address(ip_address)
        
        if not ip_object.is_global:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail="Private, loopback, or link-local IP addresses are not supported"
            )
        
        ip_location = get_ip_location(ip_address)
        
        # Extract country name from IP2Location response
        country_name = getattr(ip_location, 'country_long', 'Unknown')
        city_name = getattr(ip_location, 'city', 'Unknown')
        
        # If both country and city are unknown, it might indicate an invalid or private IP
        if country_name == 'Unknown' and city_name == 'Unknown':
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail="Unable to determine location for the provided IP address. It may be private, invalid, or not in our database."
            )
        
        return LocationResponse(
            country=country_name,
            city=city_name
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as they already have proper status codes
        raise
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred while processing your request"
        )


def get_ip_location(ip_address: str) -> LocationResponse:
    ip_location = settings.ip_to_location_service.get_location(ip_address)
    
    # Check if we got valid location data
    if not ip_location:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Location information not found for the provided IP address"
        )
        
    return ip_location