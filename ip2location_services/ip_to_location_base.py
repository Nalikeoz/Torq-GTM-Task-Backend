from abc import ABC, abstractmethod
from typing import Dict, Any

class IPToLocationServiceBase(ABC):
    """
    Abstract base class for IP to location services.
    All IP location service implementations must inherit from this class.
    """
    
    @abstractmethod
    def get_location(self, ip_address: str) -> Dict[str, Any]:
        """
        Get location information for a given IP address.
        
        Args:
            ip_address (str): The IP address to look up
            
        Returns:
            Dict[str, Any]: Dictionary containing location information
                           Must include at least 'ip' key
        """
        pass
    
