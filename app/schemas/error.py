from pydantic import BaseModel

class ErrorResponse(BaseModel):
    """Response model for errors"""
    error: str
    
