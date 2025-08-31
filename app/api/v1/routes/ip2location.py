from fastapi import APIRouter, Query
from pydantic import IPvAnyAddress
from app.schemas.location import LocationResponse

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
    ip_str = str(ip)
    print(f"Received request for IP address: {ip_str}")
    
    return LocationResponse(
        ip=ip_str,
        message=f"IP address {ip_str} received successfully"
    )

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
