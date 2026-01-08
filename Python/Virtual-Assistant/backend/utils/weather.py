import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.config import get_config

# Move your weather logic here from weather.py
import requests
import logging
import time
from typing import Optional, Dict, Any
import re

# Get configuration
config = get_config()
WEATHER_API_KEY = config['API_KEYS']['WEATHER_API_KEY']
if not WEATHER_API_KEY:
    logging.warning("WEATHER_API_KEY environment variable is not set")
WEATHER_CONFIG = config['WEATHER_CONFIG']

# Rate limiting
last_request_time = 0
MIN_REQUEST_INTERVAL = WEATHER_CONFIG['MIN_REQUEST_INTERVAL']
REQUEST_TIMEOUT = WEATHER_CONFIG['REQUEST_TIMEOUT']

def validate_city_name(city_name: str) -> bool:
    """
    Validate the city name format.
    
    Args:
        city_name (str): The city name to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not city_name or not isinstance(city_name, str):
        return False
    # Allow letters, numbers, spaces, hyphens, apostrophes, and periods
    return bool(re.match(r"^[A-Za-z0-9\s\-'\.]+$", city_name))

def weather(city_name: str) -> str:
    """
    Get weather information for a city.
    
    Args:
        city_name (str): The name of the city
        
    Returns:
        str: Weather information or error message
    """
    global last_request_time
    
    # Input validation
    if not validate_city_name(city_name):
        return "Error: Invalid city name format. Please use only letters, numbers, spaces, hyphens, apostrophes, and periods."
    
    # Rate limiting
    current_time = time.time()
    if current_time - last_request_time < MIN_REQUEST_INTERVAL:
        time.sleep(MIN_REQUEST_INTERVAL - (current_time - last_request_time))
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}&units={WEATHER_CONFIG['UNITS']}"
    
    try:
        # Set timeout for the request
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        
        # Extract weather details
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        
        # Update last request time
        last_request_time = time.time()
        
        return (
            f"Weather in {city_name}:\n"
            f"Temperature: {temp}°C\n"
            f"Description: {desc}\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s"
        )
        
    except requests.exceptions.Timeout:
        logging.error(f"Timeout while fetching weather data for {city_name}")
        return "Error: Request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        if "401" in str(e):
            logging.error(f"Invalid API key for weather service")
            return "Error: Weather service configuration error. Please check API key."
        elif "404" in str(e):
            logging.error(f"City not found: {city_name}")
            return f"Error: City '{city_name}' not found. Please check the spelling."
        else:
            logging.error(f"Request error for {city_name}: {str(e)}")
            return f"Error: Unable to fetch weather data. Please try again later."
    except KeyError as e:
        logging.error(f"Data parsing error for {city_name}: {str(e)}")
        return "Error: Unable to parse weather data. Please try again later."
    except Exception as e:
        logging.error(f"Unexpected error for {city_name}: {str(e)}")
        return "Error: An unexpected error occurred. Please try again later."

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='weather.log'
    )
    
    print("Testing weather function...")
    city = input("Enter the city name: ")
    result = weather(city)
    print(result)

