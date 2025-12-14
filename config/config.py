"""Configuration settings for the Weatherstack API framework."""

import os

# API Configuration
API_BASE_URL = "https://api.weatherstack.com"
API_KEY = "b6c3ba2323249a96c37b7eff8c1c2d89"

# Request Configuration
TIMEOUT = 10  # seconds
MAX_RETRIES = 3

# API Endpoints
ENDPOINTS = {
    "current": "/current",
    "historical": "/historical",
    "forecast": "/forecast"
}

