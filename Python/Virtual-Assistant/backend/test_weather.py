import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from backend.utils.weather import weather
from backend.utils.config import API_KEYS

print("Testing environment variable loading...")
print("GEMINI_API_KEY:", API_KEYS.get('GEMINI_API_KEY'))
print("RESEND_API_KEY:", API_KEYS.get('RESEND_API_KEY'))
print("WEATHER_API_KEY:", API_KEYS.get('WEATHER_API_KEY'))

print("\nTesting weather function...")
city = "London"
result = weather(city)
print(f"Weather for {city}: {result}")
