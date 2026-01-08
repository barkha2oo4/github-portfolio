import requests
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Get API key from environment variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    logging.warning("GEMINI_API_KEY environment variable is not set")

def ask_gemini(prompt):
    """
    Send a prompt to the Gemini API and return the response.
    
    Args:
        prompt (str): The text prompt to send to Gemini
        
    Returns:
        str: The response from Gemini or an error message
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        result = response.json()
        if "candidates" in result and len(result["candidates"]) > 0:
            return result["candidates"][0]["content"]["parts"][0]["text"].strip()
        else:
            logging.error(f"Unexpected response format: {result}")
            return "Sorry, I couldn't process that request properly."
            
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {str(e)}")
        return f"Sorry, I'm having trouble connecting to my brain right now. Please try again later."
    except (KeyError, IndexError) as e:
        logging.error(f"Error parsing response: {str(e)}")
        return "Sorry, I received an unexpected response. Please try again."
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return "Sorry, something unexpected happened. Please try again."

if __name__ == "__main__":
    print("Gemini response:")
    print(ask_gemini("Explain how AI works")) 