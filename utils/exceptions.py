"""Custom exceptions for the Weatherstack API framework."""


class WeatherAPIException(Exception):
    """Base exception for Weather API errors."""

    def __init__(self, message: str, status_code: int = None, error_code: int = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)


class InvalidAPIKeyException(WeatherAPIException):
    """Raised when the API key is invalid or missing."""
    pass


class InvalidLocationException(WeatherAPIException):
    """Raised when the location is invalid or not found."""
    pass


class APIRequestException(WeatherAPIException):
    """Raised when the API request fails."""
    pass


class UsageLimitException(WeatherAPIException):
    """Raised when API usage limit is reached."""
    pass


class TimeoutException(WeatherAPIException):
    """Raised when the API request times out."""
    pass

