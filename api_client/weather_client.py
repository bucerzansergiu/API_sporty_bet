"""Weatherstack API client for making API requests."""

import requests
from typing import Dict, Any
import time
from config.config import (
    API_BASE_URL,
    API_KEY,
    TIMEOUT,
    MAX_RETRIES,
    ENDPOINTS
)
from utils.exceptions import (
    InvalidAPIKeyException,
    InvalidLocationException,
    APIRequestException,
    UsageLimitException,
    TimeoutException
)
from utils.helpers import logger, DataHelper


class WeatherAPIClient:
    """Client for interacting with the Weatherstack API."""

    def __init__(self, api_key: str = API_KEY):
        """
        Initialize the Weather API client.

        Args:
            api_key: API key for authentication
        """
        self.api_key = api_key
        self.base_url = API_BASE_URL
        self.timeout = TIMEOUT
        self.max_retries = MAX_RETRIES
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Weatherstack-API-Framework/1.0'
        })

    def _make_request(
        self,
        endpoint: str,
        params: Dict[str, Any],
        retry_count: int = 0
    ) -> Dict[str, Any]:
        """
        Make HTTP request to the API with retry logic.

        Args:
            endpoint: API endpoint
            params: Query parameters
            retry_count: Current retry attempt

        Returns:
            API response as dictionary

        Raises:
            TimeoutException: If request times out
            APIRequestException: If request fails
        """
        url = f"{self.base_url}{endpoint}"

        try:
            logger.info(f"Making request to {url} with params: {params}")
            response = self.session.get(url, params=params, timeout=self.timeout)

            # Parse JSON response before raising HTTP errors
            # Weatherstack API returns JSON with error info even on HTTP errors
            try:
                data = response.json()
            except ValueError:
                # If can't parse JSON, raise HTTP error
                response.raise_for_status()
                raise APIRequestException(f"Invalid JSON response from API")

            DataHelper.log_response(data, endpoint)

            return data

        except requests.exceptions.Timeout:
            if retry_count < self.max_retries:
                logger.warning(f"Request timeout. Retrying... (Attempt {retry_count + 1}/{self.max_retries})")
                time.sleep(1)
                return self._make_request(endpoint, params, retry_count + 1)
            raise TimeoutException("Request timeout after maximum retries")

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            raise APIRequestException(f"Request failed: {str(e)}")

    def _handle_error_response(self, data: Dict[str, Any]):
        """
        Handle error responses from the API.

        Args:
            data: API response dictionary

        Raises:
            Appropriate exception based on error code
        """
        if "error" not in data:
            return

        error_code, error_info = DataHelper.extract_error_info(data)
        logger.error(f"API Error - Code: {error_code}, Info: {error_info}")

        if error_code in [101, 102]:
            raise InvalidAPIKeyException(
                f"Invalid API key: {error_info}",
                error_code=error_code
            )
        elif error_code in [601, 615]:
            raise InvalidLocationException(
                f"Invalid location: {error_info}",
                error_code=error_code
            )
        elif error_code == 104:
            raise UsageLimitException(
                f"Usage limit reached: {error_info}",
                error_code=error_code
            )
        else:
            raise APIRequestException(
                f"API error {error_code}: {error_info}",
                error_code=error_code
            )

    def get_current_weather(
        self,
        location: str,
        units: str = "m",
    ) -> Dict[str, Any]:
        """
        Get current weather for a location.

        Args:
            location: City name, coordinates, IP address, or zipcode
            units: Temperature units - 'm' (Celsius), 'f' (Fahrenheit), 's' (Kelvin)
            language: Response language code (default: en)

        Returns:
            Dictionary containing weather data

        Raises:
            InvalidAPIKeyException: If API key is invalid
            InvalidLocationException: If location is not found
            APIRequestException: If the request fails
            TimeoutException: If request times out
        """
        endpoint = ENDPOINTS["current"]
        params = {
            "access_key": self.api_key,
            "query": location,
            "units": units,
        }

        data = self._make_request(endpoint, params)
        self._handle_error_response(data)

        return data

    def get_historical_weather(
        self,
        location: str,
        historical_date: str,
        units: str = "m"
    ) -> Dict[str, Any]:
        """
        Get historical weather for a location on a specific date.

        Args:
            location: City name
            historical_date: Date in format YYYY-MM-DD
            units: Temperature units - 'm' (Celsius), 'f' (Fahrenheit), 's' (Kelvin)

        Returns:
            Dictionary containing historical weather data

        Raises:
            InvalidAPIKeyException: If API key is invalid
            InvalidLocationException: If location is not found
            APIRequestException: If the request fails
            TimeoutException: If request times out
        """
        endpoint = ENDPOINTS["historical"]
        params = {
            "access_key": self.api_key,
            "query": location,
            "historical_date": historical_date,
            "units": units,
        }

        data = self._make_request(endpoint, params)
        self._handle_error_response(data)

        return data

    def get_forecast_weather(
        self,
        location: str,
        forecast_days: int = 7,
        units: str = "m"
    ) -> Dict[str, Any]:
        """
        Get weather forecast for a location.

        Args:
            location: City name
            forecast_days: Number of days to forecast (1-7)
            units: Temperature units - 'm' (Celsius), 'f' (Fahrenheit), 's' (Kelvin)

        Returns:
            Dictionary containing forecast weather data

        Raises:
            InvalidAPIKeyException: If API key is invalid
            InvalidLocationException: If location is not found
            APIRequestException: If the request fails
            TimeoutException: If request times out
        """
        endpoint = ENDPOINTS["forecast"]
        params = {
            "access_key": self.api_key,
            "query": location,
            "forecast_days": forecast_days,
            "units": units,
        }

        data = self._make_request(endpoint, params)
        self._handle_error_response(data)

        return data


