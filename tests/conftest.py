import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.main import create_app
from app.core.config import settings


@pytest.fixture
def app():
    """Create a test FastAPI application instance."""
    return create_app()


@pytest.fixture
def client(app):
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def mock_ip2location_service():
    """Mock IP2Location service for testing."""
    mock_service = Mock()
    
    # Mock successful response for public IPs
    mock_location = Mock()
    mock_location.country_long = "United States"
    mock_location.city = "New York"
    
    mock_service.get_location.return_value = mock_location
    return mock_service


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    with patch('app.core.config.settings') as mock_settings:
        mock_settings.ip_to_location_service_name = "ip2location"
        mock_settings.ip_to_location_service = Mock()
        yield mock_settings


@pytest.fixture
def sample_private_ips():
    """Sample private IP addresses for testing."""
    return [
        "192.168.1.1",   # Private network
        "10.0.0.1",      # Private network
        "172.16.0.1",    # Private network
        "127.0.0.1",     # Loopback
        "::1",           # IPv6 loopback
        "fe80::1",       # IPv6 link-local
    ]


@pytest.fixture
def sample_invalid_ips():
    """Sample invalid IP addresses for testing."""
    return [
        "256.256.256.256",  # Invalid octet
        "192.168.1.256",    # Invalid octet
        "192.168.1",        # Missing octet
        "not.an.ip",        # Not an IP
        "192.168.1.1.1",    # Too many octets
        "",                  # Empty string
    ]
