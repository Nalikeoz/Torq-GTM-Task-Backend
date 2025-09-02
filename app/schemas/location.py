from pydantic import BaseModel

class LocationResponse(BaseModel):
    """Response model for location lookup."""
    country: str
    city: str
    
