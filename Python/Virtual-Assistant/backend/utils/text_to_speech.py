import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.config import get_config

# Optional: move your TTS logic here if needed for backend

import pyttsx3
import logging

def text_to_speech(text):
    """
    Convert text to speech using pyttsx3 with preference for a deep male voice.
    
    Args:
        text (str): The text to be converted to speech
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not text:
        logging.warning("Empty text provided to text_to_speech")
        return False

    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')

        # Attempt to find a deep, male voice
        preferred_voice = None
        preferred_keywords = ['david', 'mark', 'alex', 'male', 'baritone']

        # First pass: look for voices with preferred keywords
        for voice in voices:
            voice_id = voice.id.lower()
            if any(keyword in voice_id for keyword in preferred_keywords):
                preferred_voice = voice
                break

        # If no preferred voice found, try to select a male voice with a lower pitch if available
        # On Windows, SAPI5 voices may have 'gender' attribute
        if not preferred_voice:
            for voice in voices:
                if hasattr(voice, 'gender') and voice.gender.lower() == 'male':
                    preferred_voice = voice
                    break

        if preferred_voice:
            engine.setProperty('voice', preferred_voice.id)
            logging.info(f"Using preferred male voice: {getattr(preferred_voice, 'name', preferred_voice.id)}")
        else:
            engine.setProperty('voice', voices[0].id)
            logging.warning("Preferred male voice not found, using default.")

        engine.setProperty('rate', 100)  # Even slower for deeper effect
        # Try to set pitch lower if supported (SAPI5 does not support pitch directly)
        # For some engines, you can use engine.setProperty('pitch', value), but pyttsx3 SAPI5 does not support this
        # So, only rate and voice selection are used
        engine.setProperty('volume', 1.0)

        # Convert text to speech
        engine.say(text)
        engine.runAndWait()
        return True

    except Exception as e:
        logging.error(f"Error in text_to_speech: {str(e)}")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Test the text-to-speech functionality
    test_text = "Hello, this is a test of the deep voice text to speech system."
    success = text_to_speech(test_text)
    print("Text to speech test:", "successful" if success else "failed")
