import os
from typing import ClassVar, Dict, Type
from pydantic_settings import BaseSettings
from ip2location_services.IP2Location.ip2location_service import IP2LocationService
from ip2location_services.ip_to_location_base import IPToLocationServiceBase


# Service mapping (outside the class to avoid Pydantic field issues)
SERVICE_NAME_TO_CLASS: Dict[str, Type[IPToLocationServiceBase]] = {
    "ip2location": IP2LocationService,
}


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    # IP Location Service settings
    ip_to_location_service_name: str
    
    # API settings
    title: str = "IP Location Service"
    description: str = "A simple service to find country information by IP address"
    version: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def ip_to_location_service(self) -> IPToLocationServiceBase:
        """Get the IP to location service instance."""
        service_class = SERVICE_NAME_TO_CLASS.get(self.ip_to_location_service_name)
        if not service_class:
            raise ValueError(f"Unknown service: {self.ip_to_location_service_name}")
        return service_class()

settings = Settings()
