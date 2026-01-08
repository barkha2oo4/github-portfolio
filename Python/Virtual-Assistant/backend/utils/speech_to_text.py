import speech_recognition as sr
import logging

def speech_to_text():
    """
    Convert speech to text using Google's speech recognition.
    
    Returns:
        str: The recognized text, or "Unknown" if recognition failed,
             or "Error" if there was a service error
    """
    r = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            print("Listening...")
            # Adjust for ambient noise
            r.adjust_for_ambient_noise(source, duration=0.5)
            # Listen for audio input
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            
        try:
            # Use Google's speech recognition
            voice_data = r.recognize_google(audio)
            print(f"You said: {voice_data}")
            return voice_data
            
        except sr.UnknownValueError:
            logging.warning("Speech recognition could not understand audio")
            print("Sorry, I couldn't understand that.")
            return "Unknown"
            
        except sr.RequestError as e:
            logging.error(f"Could not request results from speech recognition service: {str(e)}")
            print("Sorry, my speech service is down.")
            return "Error"
            
    except Exception as e:
        logging.error(f"Error in speech_to_text: {str(e)}")
        print(f"An error occurred: {str(e)}")
        return "Error"

if __name__ == "__main__":
    # Test the speech-to-text functionality
    result = speech_to_text()
    print("Speech recognition result:", result)