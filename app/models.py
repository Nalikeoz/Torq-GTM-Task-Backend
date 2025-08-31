from pydantic import BaseModel

class LocationResponse(BaseModel):
    """Response model for location lookup."""
    ip: str
    message: str
