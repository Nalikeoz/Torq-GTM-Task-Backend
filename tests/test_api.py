import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from http import HTTPStatus


class TestFindCountryEndpoint:
    """Test cases for the /v1/find-country endpoint."""

    def test_find_country_success(self, client, mock_ip2location_service):
        """Test successful country lookup for a public IP address."""
        with patch('app.core.config.settings') as mock_settings:
            mock_settings.ip_to_location_service = mock_ip2location_service
            
            response = client.get("/v1/find-country?ip=8.8.8.8")
            
            assert response.status_code == 200
            data = response.json()
            assert data["country"] == "United States of America"
            assert data["city"] == "Mountain View"

    def test_find_country_missing_ip_parameter(self, client):
        """Test that missing IP parameter returns validation error."""
        response = client.get("/v1/find-country")
        
        assert response.status_code == 422
        data = response.json()
        assert "error" in data

    def test_find_country_private_ip_rejected(self, client, sample_private_ips):
        """Test that private IP addresses are rejected."""
        for ip in sample_private_ips:
            response = client.get(f"/v1/find-country?ip={ip}")
            
            assert response.status_code == 422
            data = response.json()
            assert "Private, loopback, or link-local IP addresses are not supported" in data["error"]

    def test_find_country_invalid_ip_format(self, client, sample_invalid_ips):
        """Test that invalid IP formats return validation errors."""
        for ip in sample_invalid_ips:
            response = client.get(f"/v1/find-country?ip={ip}")
            
            assert response.status_code == 422
            data = response.json()
            assert "error" in data

    def test_find_country_service_not_found(self, client):
        """Test handling when IP2Location service returns no location data."""
        mock_service = Mock()
        mock_service.get_location.return_value = None
        
        with patch('app.core.config.settings') as mock_settings:
            mock_settings.ip_to_location_service = mock_service
            
            response = client.get("/invalid-page")
            
            assert response.status_code == 404

    def test_find_country_multiple_requests(self, client, mock_ip2location_service):
        """Test that multiple requests work correctly."""
        with patch('app.core.config.settings') as mock_settings:
            mock_settings.ip_to_location_service = mock_ip2location_service
            
            # Make multiple requests
            ips = ["8.8.8.8", "1.1.1.1", "208.67.222.222"]
            
            for ip in ips:
                response = client.get(f"/v1/find-country?ip={ip}")
                assert response.status_code == 200

    def test_find_country_edge_case_very_long_ip(self, client):
        """Test handling of extremely long IP-like strings."""
        long_ip = "1" * 1000
        
        response = client.get(f"/v1/find-country?ip={long_ip}")
        
        assert response.status_code == 422

    def test_find_country_special_characters_in_ip(self, client, sample_private_ips):
        """Test handling of IP addresses with special characters."""
        for ip in sample_private_ips:
            response = client.get(f"/v1/find-country?ip={ip}")
            assert response.status_code == 422
