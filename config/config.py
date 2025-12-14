"""Configuration settings for the Weatherstack API framework."""

import os

# API Configuration
API_BASE_URL = "https://api.weatherstack.com"
API_KEY = os.getenv("WEATHERSTACK_API_KEY")

# Request Configuration
TIMEOUT = 10  # seconds
MAX_RETRIES = 3

# API Endpoints
ENDPOINTS = {
    "current": "/current",
    "historical": "/historical",
    "forecast": "/forecast"
}

