"""Utility functions for API validation and helpers."""

from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ResponseValidator:
    """Validates API response structure and data."""

    @staticmethod
    def validate_response_structure(response: Dict[str, Any]) -> bool:
        """
        Validate the basic structure of the API response.
        Args:
            response: API response dictionary
        Returns:
            True if response structure is valid, False otherwise
        """
        required_keys = ["request", "location", "current"]

        if not all(key in response for key in required_keys):
            missing_keys = [key for key in required_keys if key not in response]
            logger.error(f"Missing required keys: {missing_keys}")
            return False

        return True

    @staticmethod
    def validate_location_data(location_data: Dict[str, Any]) -> bool:
        """
        Validate location data structure.
        Args:
            location_data: Location data dictionary
        Returns:
            True if valid, False otherwise
        """
        required_keys = ["name", "country", "region", "lat", "lon", "timezone_id"]

        if not all(key in location_data for key in required_keys):
            missing_keys = [key for key in required_keys if key not in location_data]
            logger.error(f"Missing location keys: {missing_keys}")
            return False

        return True

    @staticmethod
    def validate_current_weather_data(current_data: Dict[str, Any]) -> bool:
        """
        Validate current weather data structure.
        Args:
            current_data: Current weather data dictionary
        Returns:
            True if valid, False otherwise
        """
        required_keys = [
            "temperature",
            "weather_descriptions",
            "wind_speed",
            "wind_degree",
            "pressure",
            "humidity",
            "cloudcover",
            "feelslike",
            "visibility"
        ]

        if not all(key in current_data for key in required_keys):
            missing_keys = [key for key in required_keys if key not in current_data]
            logger.error(f"Missing current weather keys: {missing_keys}")
            return False

        return True

    @staticmethod
    def validate_data_types(response: Dict[str, Any]) -> bool:
        """
        Validate data types in the response.
        Args:
            response: API response dictionary
        Returns:
            True if data types are valid, False otherwise
        """
        try:
            # Validate location data types
            location = response.get("location", {})
            assert isinstance(location.get("name"), str)
            assert isinstance(location.get("country"), str)
            assert isinstance(location.get("lat"), str)
            assert isinstance(location.get("lon"), str)

            # Validate current weather data types
            current = response.get("current", {})
            assert isinstance(current.get("temperature"), (int, float))
            assert isinstance(current.get("weather_descriptions"), list)
            assert isinstance(current.get("wind_speed"), (int, float))
            assert isinstance(current.get("humidity"), (int, float))
            assert isinstance(current.get("pressure"), (int, float))

            return True
        except (AssertionError, TypeError, AttributeError) as e:
            logger.error(f"Data type validation failed: {e}")
            return False


class DataHelper:
    """Helper functions for data manipulation and formatting."""


    @staticmethod
    def extract_error_info(response: Dict[str, Any]) -> tuple:
        """
        Extract error information from response.

        Args:
            response: API response dictionary

        Returns:
            Tuple of (error_code, error_info)
        """
        if "error" in response:
            error = response["error"]
            return error.get("code"), error.get("info")
        return None, None

    @staticmethod
    def log_response(response: Dict[str, Any], endpoint: str):
        """Log API response for debugging."""
        logger.info(f"Response from {endpoint}:")
        logger.info(f"Status: {'Success' if 'location' in response else 'Error'}")
        if "location" in response:
            logger.info(f"Location: {response['location'].get('name')}, {response['location'].get('country')}")
        if "error" in response:
            logger.error(f"Error: {response['error']}")

