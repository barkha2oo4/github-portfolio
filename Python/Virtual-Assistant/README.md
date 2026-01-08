# Virtual Assistant

A Python-based virtual assistant with speech recognition, text-to-speech, and various integrations including Gemini AI, email, and weather services.

## Features

- Speech recognition and text-to-speech capabilities
- Integration with Google's Gemini AI for natural language processing
- Email functionality using Resend API
- Weather information retrieval
- Modern GUI interface
- Voice commands for various system operations

## Prerequisites

- Python 3.8 or higher
- Windows OS (for some system-specific features)
- Microphone for speech recognition
- Speakers for text-to-speech

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Virtual-Assistant
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Install spaCy language model:
```bash
python -m spacy download en_core_web_sm
```

5. Create a `.env` file in the project root with your API keys:
```
GEMINI_API_KEY=your_gemini_api_key
RESEND_API_KEY=your_resend_api_key
WEATHER_API_KEY=your_weather_api_key

**Warning:** Make sure to replace the placeholder values in the `.env` file with your actual API keys. The application will not work correctly if the API keys are not set.
```

## Usage

1. Run the GUI application:
```bash
python GUI.py
```

2. Use the interface to:
   - Type queries in the text box
   - Click "Ask" to use voice input
   - Click "Submit" to send text queries
   - Use "Clear" to clear the response area
   - Use "Delete" to clear the input box

## Voice Commands

The assistant supports various voice commands including:
- "What's the weather in [city]?"
- "What time is it?"
- "Open [application/website]"
- "Send email to [address]"
- And more...

## Error Handling

The application includes comprehensive error handling and logging:
- All errors are logged to `assistant.log`
- User-friendly error messages are displayed in the GUI
- Failed operations are gracefully handled with appropriate feedback

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

# Virtual Assistant Web (Flask Backend)

## Project Structure

```
virtual_assistant_web/
├── backend/
│   ├── app.py                # Flask app entry point
│   ├── action_logic.py       # Main assistant logic
│   ├── utils/                # Utility modules
│   │   ├── weather.py
│   │   ├── text_to_speech.py
│   │   ├── speech_to_text.py
│   ├── templates/
│   │   └── index.html        # Web UI
│   └── static/
│       ├── js/
│       │   └── main.js
│       └── css/
│           └── style.css
├── requirements.txt          # Python dependencies
├── README.md                 # This file
```

## Setup Instructions

1. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

2. **Run the backend:**
   ```powershell
   cd backend
   python app.py
   ```

3. **Open your browser:**
   Go to [http://127.0.0.1:5000](http://127.0.0.1:5000)

4. **Ask questions!**
   - Type your query in the web UI and get responses from the assistant (with Gemini fallback).

## Notes
- All assistant logic is in `backend/action_logic.py` and utilities in `backend/utils/`.
- Gemini integration is required for fallback AI responses (see `gemini_integration.py`).
- For further customization, edit the HTML/CSS/JS in `backend/templates/` and `backend/static/`.

## Advanced Features for Major Project

- **Natural Language Processing (NLP):** Uses spaCy to extract user intent (weather, reminders, definitions, general chat) and entities (city, time, task, word) from queries.
- **Contextual AI (Gemini):** Maintains conversation history and last entity/topic for context-aware follow-ups.
- **Reminders:** Add, list, and delete reminders with natural language (e.g., "Remind me to call John at 5pm").
- **Weather:** Ask for weather in any city using natural language.
- **Text-to-Speech & Speech-to-Text:** Web UI supports speaking responses and voice input.
- **Modular, Testable Backend:** Flask API, modular logic, and system tests included.

### How NLP Works
- The assistant uses spaCy to classify user intent and extract relevant entities.
- This enables robust handling of complex, conversational, and follow-up queries.

### To Install spaCy Model
After installing requirements, run:
```powershell
python -m spacy download en_core_web_sm
```