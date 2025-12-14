"""Test suite for Weatherstack API client."""

import pytest
from api_client.weather_client import WeatherAPIClient
from utils.helpers import ResponseValidator
from config.config import API_KEY
import logging
import json

log = logging.getLogger(__name__)

class TestWeatherAPIClient:
    """Test cases for WeatherAPIClient."""

    @pytest.fixture(scope="class")
    def client(self):
        """Create a client instance for testing."""
        return WeatherAPIClient(api_key=API_KEY)

    @pytest.fixture(scope="class")
    def validator(self):
        """Create a validator instance for testing."""
        return ResponseValidator()

    # Helper methods for common validations (DRY principle)

    def validate_basic_response_structure(self, response, validator, location_name=None):
        """
        Validate basic response structure common to all weather responses.

        Args:
            response: API response dictionary
            validator: ResponseValidator instance
            location_name: Optional location name for additional context
        """
        context = f" for {location_name}" if location_name else ""

        # Validate response structure
        assert validator.validate_response_structure(response), \
            f"Response structure is invalid{context}"

        # Validate location data structure
        assert validator.validate_location_data(response["location"]), \
            f"Location data structure is invalid{context}"

        # Validate data types
        assert validator.validate_data_types(response), \
            f"Data types are invalid{context}"

    def validate_location_presence(self, response, context=""):
        """
        Validate that location data is present in response.

        Args:
            response: API response dictionary
            context: Optional context string for error messages
        """
        assert "location" in response, f"Location data is missing{context}"
        assert "name" in response["location"], f"Location name is missing{context}"

        location_name = response["location"]["name"]
        log.info(f"Location validated: {location_name}{context}")
        return location_name

    def validate_location_match(self, response, expected_location, expected_country=None):
        """
        Validate that location and country match expected values.

        Args:
            response: API response dictionary
            expected_location: Expected location name
            expected_country: Optional expected country name
        """
        actual_location = response["location"]["name"]
        assert actual_location == expected_location, \
            f"Expected location '{expected_location}', got '{actual_location}'"

        if expected_country:
            actual_country = response["location"]["country"]
            assert actual_country == expected_country, \
                f"Expected country '{expected_country}', got '{actual_country}'"

    def validate_temperature_field(self, weather_data, field_name="current"):
        """
        Validate temperature field exists and is numeric.

        Args:
            weather_data: Dictionary containing weather data
            field_name: Context name for error messages
        """
        assert "temperature" in weather_data, \
            f"Temperature field is missing in {field_name} data"
        assert isinstance(weather_data["temperature"], (int, float)), \
            f"Temperature must be numeric in {field_name} data"

    @pytest.mark.parametrize("location,expected_country", [
        ("London", "United Kingdom"),
        ("New York", "United States of America"),
        ("Tokyo", "Japan"),
        ("Paris", "France")
    ])
    def test_get_current_weather_valid_locations(self, client, validator, location, expected_country):
        """
        Verify API returns correct weather data for valid locations.
        Validation:
        1. Response structure validation
        2. Location name matching
        3. Country validation
        4. Data type validation
        """
        # Make API request
        response = client.get_current_weather(location)
        log.info(f"Response:\n{json.dumps(response, indent=2)}")

        # Use helper methods for common validations (DRY)
        self.validate_basic_response_structure(response, validator, location)
        self.validate_location_match(response, location, expected_country)

        # Validate current weather data structure
        assert validator.validate_current_weather_data(response["current"]), \
            f"Current weather data structure is invalid for: {location}"

        # Validate temperature field
        self.validate_temperature_field(response["current"], "current")


    def test_get_historical_weather(self, client, validator):
        """
        Test historical weather data for Cluj on 24.12.2024.
        Validation:
        1. Response structure validation
        2. Location name matching
        3. Historical data presence
        4. Date validation
        """
        location = "Cluj"
        historical_date = "2024-12-24"

        # Make API request
        response = client.get_historical_weather(location, historical_date)
        log.info(f"Historical Weather Response:\n{json.dumps(response, indent=2)}")

        # Validate historical data presence
        assert "historical" in response or "current" in response, \
            "Historical weather data is missing"

        # Validate historical date is present in response
        if "historical" in response:
            historical_data = response["historical"]
            assert historical_date in historical_data, \
                f"Historical data for date {historical_date} is missing"

            # Validate weather data exists for the date
            date_weather = historical_data[historical_date]
            assert "temperature" in date_weather or "avgtemp" in date_weather, \
                "Temperature data is missing for historical date"

        log.info(f"Historical weather for {historical_date} retrieved successfully")

    def test_get_forecast_weather(self, client):
        """
        Test weather forecast for the next week.
        Validation:
        1. Response structure validation
        2. Forecast data presence
        3. Number of forecast days
        4. Forecast data completeness
        """
        location = "Cluj"
        forecast_days = 7

        # Make API request
        response = client.get_forecast_weather(location, forecast_days=forecast_days)
        log.info(f"Forecast Weather Response:\n{json.dumps(response, indent=2)}")

        # Validate forecast data presence
        assert "forecast" in response or "current" in response, \
            "Forecast weather data is missing"

        # Validate forecast data exists
        if "forecast" in response:
            forecast_data = response["forecast"]
            assert len(forecast_data) > 0, "Forecast data is empty"
            log.info(f"Forecast for next {len(forecast_data)} days retrieved successfully")

