import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from backend.utils.weather import weather
from backend.utils.config import API_KEYS
from gemini_integration import ask_gemini

print("Testing environment variable loading...")
print("GEMINI_API_KEY:", API_KEYS.get('GEMINI_API_KEY'))
print("WEATHER_API_KEY:", API_KEYS.get('WEATHER_API_KEY'))

print("\nTesting weather function...")
city = "London"
result = weather(city)
print(f"Weather for {city}: {result}")

print("\nTesting Gemini integration...")
try:
    gemini_result = ask_gemini("What is the capital of France?")
    print("Gemini response:", gemini_result)
except Exception as e:
    print("Gemini integration error:", e)

print("\nTesting Gemini with context (follow-up question)...")
try:
    gemini_result2 = ask_gemini("What about its population?")
    print("Gemini follow-up response:", gemini_result2)
except Exception as e:
    print("Gemini context error:", e)
