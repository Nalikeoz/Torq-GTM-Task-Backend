import os
import IP2Location
from ip2location_services.ip_to_location_base import IPToLocationServiceBase


class IP2LocationService(IPToLocationServiceBase):
    def __init__(self, db_path = "IP2LOCATION-LITE-DB3.BIN"):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        database_path = os.path.join(current_dir, db_path)
        self._database = IP2Location.IP2Location(database_path)

    def get_location(self, ip_address: str):
        return self._database.get_all(ip_address)