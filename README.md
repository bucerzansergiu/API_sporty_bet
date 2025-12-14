# Weatherstack API Automation Framework

A comprehensive, clean, and maintainable Python API automation framework for testing the [Weatherstack API](https://weatherstack.com/).

## 📋 Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Test Cases](#test-cases)
- [Validation Strategy](#validation-strategy)
- [Design Principles](#design-principles)

## ✨ Features

- **Clean Architecture**: Separation of concerns with dedicated modules for client, config, utilities, and tests
- **Multiple Endpoints**: Support for current weather, historical data, and forecasts
- **Comprehensive Testing**: 6 test cases covering current, historical, and forecast weather data
- **Robust Validation**: Multi-layered validation including structure, data types, and location matching
- **Exception Handling**: Custom exceptions for different error scenarios
- **Logging**: Detailed logging for debugging and monitoring
- **Retry Logic**: Automatic retry mechanism for handling transient failures
- **Type Safety**: Type hints throughout the codebase for better IDE support

## 📁 Project Structure

```
API-automation/
├── README.md                          # Project documentation
├── requirements.txt                   # Python dependencies
├── config/
│   ├── __init__.py
│   └── config.py                      # Configuration settings and constants
├── api_client/
│   ├── __init__.py
│   └── weather_client.py              # Main API client implementation
├── utils/
│   ├── __init__.py
│   ├── exceptions.py                  # Custom exception classes
│   └── helpers.py                     # Validation and helper functions
└── tests/
    ├── __init__.py
    └── test_weather_api.py            # Test suite
```

## 🚀 Installation

1. **Clone the repository** (if applicable)
   ```bash
   cd /Users/lianabucerzan/Documents/sergiu/sportybet/API-automation
   ```

2. **Create and activate virtual environment** (recommended)
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

The API key is configured in `config/config.py`:

```python
API_KEY = "b6c3ba2323249a96c37b7eff8c1c2d89"
```

You can also set it as an environment variable:
```bash
export WEATHERSTACK_API_KEY="your_api_key_here"
```

## 💻 Usage

### Basic Usage Example

```python
from api_client import WeatherAPIClient

# Initialize client
client = WeatherAPIClient()

# Get current weather (default units: Celsius)
weather = client.get_current_weather("London")
print(f"Temperature: {weather['current']['temperature']}°C")
print(f"Weather: {weather['current']['weather_descriptions'][0]}")

# Get weather with different units
weather_f = client.get_current_weather("New York", units="f")
print(f"Temperature: {weather_f['current']['temperature']}°F")

# Get historical weather data
historical = client.get_historical_weather("Cluj", "2024-12-24")
print(f"Historical data for Cluj on Christmas Eve 2024")

# Get weather forecast
forecast = client.get_forecast_weather("Cluj", forecast_days=7)
print(f"7-day weather forecast for Cluj")
```

## 🧪 Running Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test Class
```bash
pytest tests/test_weather_api.py::TestWeatherAPIClient -v
```

### Run Specific Test Method
```bash
pytest tests/test_weather_api.py::TestWeatherAPIClient::test_get_current_weather_valid_locations -v
```

### Run with Coverage Report
```bash
pytest tests/ --cov=api_client --cov=utils --cov-report=html
```

### Run with HTML Report
```bash
pytest tests/ --html=report.html --self-contained-html
```

## 📊 Test Cases

### Test Case Summary Table

| Test ID | Test Name | Test Method | Input Parameters | Expected Outcome | Validation Type | Priority |
|---------|-----------|-------------|------------------|------------------|-----------------|----------|
| TC-01 | Valid Location - London | `test_get_current_weather_valid_locations` | location="London", expected_country="United Kingdom" | Returns accurate weather data for London, UK | Structure, Location Match, Data Types, Country | High |
| TC-02 | Valid Location - New York | `test_get_current_weather_valid_locations` | location="New York", expected_country="United States of America" | Returns accurate weather data for New York, USA | Structure, Location Match, Data Types, Country | High |
| TC-03 | Valid Location - Tokyo | `test_get_current_weather_valid_locations` | location="Tokyo", expected_country="Japan" | Returns accurate weather data for Tokyo, Japan | Structure, Location Match, Data Types, Country | High |
| TC-04 | Valid Location - Paris | `test_get_current_weather_valid_locations` | location="Paris", expected_country="France" | Returns accurate weather data for Paris, France | Structure, Location Match, Data Types, Country | High |
| TC-05 | Historical Weather - Cluj | `test_get_historical_weather_cluj` | location="Cluj", date="2024-12-24" | Returns historical weather data for Cluj on Christmas Eve 2024 | Structure, Historical Data, Date Validation | Medium |
| TC-06 | Forecast Weather - Next Week | `test_get_forecast_weather_next_week` | location="Cluj", forecast_days=7 | Returns 7-day weather forecast for Cluj | Structure, Forecast Data, Days Count | Medium |

### Test Coverage Summary

- **Total Test Cases**: 6
- **Parametrized Tests**: 4 (using @pytest.mark.parametrize)
- **Coverage Areas**:
  - Current weather: 4 test cases
  - Historical weather: 1 test case
  - Forecast weather: 1 test case

> **⚠️ Note:** The historical and forecast endpoints require a paid Weatherstack plan. If using a free tier key, these tests will fail with error 104/105!

## 🔍 Validation Summary

### Types of Validation Used

This framework implements **3 core validation strategies** to ensure API reliability and data quality:

#### 1. **Response Structure Validation**
**What it validates:** Presence of required keys (`request`, `location`, `current`) and nested field structure

**Why it's important:**
- Ensures the API contract is maintained and hasn't changed unexpectedly
- Prevents `KeyError` exceptions when accessing nested data
- Detects breaking API changes early
- Guarantees data completeness before further processing

**How it works:** Validates that all expected top-level and nested keys exist in the response

#### 2. **Data Type Validation**
**What it validates:** Correct data types for all fields (strings, numbers, lists)

**Why it's important:**
- Prevents type errors during data processing and calculations
- Ensures data can be safely used without runtime type checks
- Validates data integrity from the API source
- Enables type-safe operations throughout the application

**How it works:** Checks that location fields are strings, temperatures are numeric, and collections are proper lists

#### 3. **Location Matching Validation**
**What it validates:** Returned location and country match the queried values

**Why it's important:**
- Confirms the API returned data for the correct location
- Prevents confusion with similarly-named places (e.g., Paris, Texas vs Paris, France)
- Ensures geographical accuracy of weather data
- Validates that the API correctly processed the query

**How it works:** Performs exact string comparison between expected and actual location/country names

### DRY Principle Implementation

To avoid code duplication, these validations are implemented as **reusable helper methods**:
- `validate_basic_response_structure()` - Combines structure and data type checks
- `validate_location_presence()` - Verifies location data exists
- `validate_location_match()` - Confirms location and country accuracy
- `validate_temperature_field()` - Ensures temperature data is present and valid

This approach ensures **consistent validation** across all tests while maintaining clean, readable test code.

