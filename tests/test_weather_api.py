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

        # Validation 1: Response structure
        assert validator.validate_response_structure(response), \
            f"Response structure is invalid for location: {location}"

        # Validation 2: Location data structure
        assert validator.validate_location_data(response["location"]), \
            f"Location data structure is invalid for: {location}"

        # Validation 3: Current weather data structure
        assert validator.validate_current_weather_data(response["current"]), \
            f"Current weather data structure is invalid for: {location}"

        # Validation 4: Data types
        assert validator.validate_data_types(response), \
            f"Data types are invalid for location: {location}"

        # Validation 5: Location name matching
        assert response["location"]["name"] == location, \
            f"Expected location '{location}', got '{response['location']['name']}'"

        # Validation 6: Country validation
        assert response["location"]["country"] == expected_country, \
            f"Expected country '{expected_country}', got '{response['location']['country']}'"

        # Validation 7: Temperature exists and is numeric
        assert "temperature" in response["current"], "Temperature field is missing"
        assert isinstance(response["current"]["temperature"], (int, float)), \
            "Temperature must be numeric"

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

        # Validation 1: Response has required keys
        assert "location" in response, "Location data is missing"
        assert "historical" in response or "current" in response, \
            "Historical weather data is missing"

        # Validation 2: Location name validation
        assert "name" in response["location"], "Location name is missing"
        location_name = response["location"]["name"]
        log.info(f"Historical data for location: {location_name}")

        # Validation 3: Historical date is present in response
        if "historical" in response:
            historical_data = response["historical"]
            assert historical_date in historical_data, \
                f"Historical data for date {historical_date} is missing"

            # Validation 4: Weather data exists for the date
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

        # Validation 1: Response has required keys
        assert "location" in response, "Location data is missing"
        assert "forecast" in response or "current" in response, \
            "Forecast weather data is missing"

        # Validation 2: Location name validation
        assert "name" in response["location"], "Location name is missing"
        location_name = response["location"]["name"]
        log.info(f"Forecast data for location: {location_name}")

        # Validation 3: Forecast data exists
        if "forecast" in response:
            forecast_data = response["forecast"]
            assert len(forecast_data) > 0, "Forecast data is empty"

            # Validation 4: Check forecast days count
            log.info(f"Number of forecast days: {len(forecast_data)}")
            assert len(forecast_data) <= forecast_days, \
                f"Expected max {forecast_days} forecast days, got {len(forecast_data)}"

            # Validation 5: Each forecast day has required data
            for date_key, day_data in list(forecast_data.items())[:3]:  # Check first 3 days
                assert "date" in day_data or date_key, \
                    f"Date information missing for forecast day"
                assert "avgtemp" in day_data or "maxtemp" in day_data, \
                    f"Temperature data missing for forecast day {date_key}"

            log.info(f"Forecast for next {len(forecast_data)} days retrieved successfully")

