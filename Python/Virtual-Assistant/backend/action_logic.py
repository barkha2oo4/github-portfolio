from dotenv import load_dotenv
load_dotenv()

import logging
import datetime
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import webbrowser
import platform
import subprocess
from utils.weather import weather
from utils.text_to_speech import text_to_speech
from utils.config import setup_logging
from apscheduler.schedulers.background import BackgroundScheduler
import re
from utils.nlp_utils import extract_intent_entities

logger = setup_logging()

# Conversation context and reminders storage
conversation_history = []
reminders = []

scheduler = BackgroundScheduler()
scheduler.start()

def extract_city(user_data):
    # ...existing code...
    cities = ["New York", "London", "Paris", "Tokyo"]
    for city in cities:
        if city.lower() in user_data.lower():
            return city
    return None

def get_definition(word):
    # ...existing code from action.py...
    import requests
    word = word.strip().lower()
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            meanings = []
            for entry in data:
                if 'meanings' in entry:
                    for meaning in entry['meanings']:
                        if 'definitions' in meaning and len(meaning['definitions']) > 0:
                            meanings.append(meaning['definitions'][0]['definition'])
            if meanings:
                return " | ".join(meanings)
        return f"Sorry, I couldn't find the definition for '{word}'."
    except requests.exceptions.Timeout:
        logging.error(f"Timeout while fetching definition for {word}")
        return "Sorry, the dictionary service is taking too long to respond. Please try again."
    except Exception as e:
        logging.error(f"Error fetching definition for {word}: {e}")
        return f"Sorry, I couldn't find the definition for '{word}'."

# Helper to add a reminder
def add_reminder(text, remind_time):
    reminders.append({"text": text, "time": remind_time})
    logger.info(f"Reminder set: {text} at {remind_time}")
    # Schedule the reminder
    scheduler.add_job(
        lambda: logger.info(f"Reminder: {text}"),
        'date',
        run_date=remind_time
    )

# Helper to list reminders
def list_reminders():
    if not reminders:
        return "No reminders set."
    return "\n".join([f"{i+1}. {r['text']} at {r['time']}" for i, r in enumerate(reminders)])

# Helper to delete a reminder
def delete_reminder(index):
    try:
        removed = reminders.pop(index)
        return f"Deleted reminder: {removed['text']}"
    except Exception:
        return "Invalid reminder index."

# Extend handle_known_actions for reminders
def handle_known_actions(user_data):
    responses = []
    user_data = user_data.lower()
    global last_entity
    try:
        # Greetings
        if any(greet in user_data for greet in ["hello", "hi", "hey", "namaste"]):
            responses.append("Hello, how can I help you?")
            text_to_speech("Hello, how can I help you?")
        if "how are you" in user_data:
            responses.append("I am fine, how are you doing?")
            text_to_speech("I am fine, how are you doing?")
        if "what is your name" in user_data:
            responses.append("My Name is Kai")
            text_to_speech("My Name is Kai")
        if "what is your age" in user_data:
            responses.append("I am 25 years old")
            text_to_speech("I am 25 years old")
        if "bye" in user_data or "goodbye" in user_data or "see you" in user_data or "exit" in user_data:
            responses.append("Goodbye! Have a great day!")
            text_to_speech("Goodbye! Have a great day!")
        # Time/date/day
        if "time now" in user_data:
            time = datetime.datetime.now().strftime("%H:%M")
            responses.append("The time is " + time)
            text_to_speech("The time is " + time)
        if "date today" in user_data:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            responses.append("The date is " + date)
            text_to_speech("The date is " + date)
        if "day today" in user_data:
            day = datetime.datetime.now().strftime("%A")
            responses.append("Today is " + day)
            text_to_speech("Today is " + day)
        # File explorer, drives, browser, system
        if "open gmail" in user_data:
            try:
                webbrowser.open("https://mail.google.com/mail/u/jhabarkha808@gmail.com")
                responses.append("Opening Gmail for you. <a href='https://mail.google.com/mail/u/jhabarkha808@gmail.com' target='_blank'>Open Gmail</a>")
                text_to_speech("Opening Gmail for you.")
            except Exception as e:
                responses.append("Sorry, I couldn't open Gmail.")
                text_to_speech("Sorry, I couldn't open Gmail.")
        if "open e drive" in user_data or "open e:" in user_data:
            try:
                webbrowser.open("file:///E:/")
                responses.append("Opening E drive for you. <a href='file:///E:/' target='_blank'>Open E Drive</a>")
                text_to_speech("Opening E drive for you.")
            except Exception as e:
                responses.append("Sorry, I couldn't open E drive.")
                text_to_speech("Sorry, I couldn't open E drive.")
        if "open c drive" in user_data or "open c:" in user_data:
            try:
                webbrowser.open("file:///C:/")
                responses.append("Opening C drive for you. <a href='file:///C:/' target='_blank'>Open C Drive</a>")
                text_to_speech("Opening C drive for you.")
            except Exception as e:
                responses.append("Sorry, I couldn't open C drive.")
                text_to_speech("Sorry, I couldn't open C drive.")
        if "open file explorer" in user_data:
            try:
                if open_file_explorer():
                    responses.append("Opening File Explorer for you.")
                    text_to_speech("Opening File Explorer for you.")
                else:
                    responses.append("Sorry, I couldn't open the file explorer.")
                    text_to_speech("Sorry, I couldn't open the file explorer.")
            except Exception as e:
                responses.append("Sorry, I couldn't open the file explorer.")
                text_to_speech("Sorry, I couldn't open the file explorer.")
        if "open recycle bin" in user_data:
            try:
                if open_recycle_bin():
                    responses.append("Opening Recycle Bin for you.")
                    text_to_speech("Opening Recycle Bin for you.")
                else:
                    responses.append("Sorry, I couldn't open the recycle bin.")
                    text_to_speech("Sorry, I couldn't open the recycle bin.")
            except Exception as e:
                responses.append("Sorry, I couldn't open the recycle bin.")
                text_to_speech("Sorry, I couldn't open the recycle bin.")
        if "open vscode" in user_data or "open visual studio code" in user_data:
            try:
                if open_vscode():
                    responses.append("Opening Visual Studio Code for you.")
                    text_to_speech("Opening Visual Studio Code for you.")
                else:
                    responses.append("Sorry, I couldn't open Visual Studio Code.")
                    text_to_speech("Sorry, I couldn't open Visual Studio Code.")
            except Exception as e:
                responses.append("Sorry, I couldn't open Visual Studio Code.")
                text_to_speech("Sorry, I couldn't open Visual Studio Code.")
        if "open settings" in user_data:
            try:
                os.startfile("ms-settings:")
                responses.append("Opening Windows Settings for you.")
                text_to_speech("Opening Windows Settings for you.")
            except Exception as e:
                responses.append("Sorry, I couldn't open Windows Settings.")
                text_to_speech("Sorry, I couldn't open Windows Settings.")
        if "play music" in user_data:
            try:
                webbrowser.open("https://www.spotify.com/")
                responses.append("Opening Spotify for you. <a href='https://www.spotify.com/' target='_blank'>Open Spotify</a>")
                text_to_speech("Opening Spotify for you.")
            except Exception as e:
                responses.append("Sorry, I couldn't open Spotify.")
                text_to_speech("Sorry, I couldn't open Spotify.")
        if "open youtube" in user_data:
            try:
                webbrowser.open("https://www.youtube.com/")
                responses.append("Opening YouTube for you. <a href='https://www.youtube.com/' target='_blank'>Open YouTube</a>")
                text_to_speech("Opening YouTube for you.")
            except Exception as e:
                responses.append("Sorry, I couldn't open YouTube.")
                text_to_speech("Sorry, I couldn't open YouTube.")
        if "open google" in user_data:
            try:
                webbrowser.open("https://www.google.com/")
                responses.append("Opening Google for you. <a href='https://www.google.com/' target='_blank'>Open Google</a>")
                text_to_speech("Opening Google for you.")
            except Exception as e:
                responses.append("Sorry, I couldn't open Google.")
                text_to_speech("Sorry, I couldn't open Google.")
        if "open github" in user_data:
            try:
                webbrowser.open("https://www.github.com/")
                responses.append("Opening GitHub for you. <a href='https://www.github.com/' target='_blank'>Open GitHub</a>")
                text_to_speech("Opening GitHub for you.")
            except Exception as e:
                responses.append("Sorry, I couldn't open GitHub.")
                text_to_speech("Sorry, I couldn't open GitHub.")
        # Email
        if "send email" in user_data:
            import re
            to = re.search(r"to ([\w\.-]+@[\w\.-]+)", user_data)
            subject = re.search(r"about ([^:]+)", user_data)
            message = re.search(r"subject: (.+)", user_data)
            to_email = to.group(1) if to else "jhabarkha808@gmail.com"
            subject_text = subject.group(1).strip() if subject else ""
            message_text = message.group(1).strip() if message else ""
            email_response = send_email(to_email, subject_text, message_text)
            responses.append(email_response)
            text_to_speech(email_response)
        # Reminders
        if "remind me to" in user_data:
            task = user_data.split("remind me to")[-1].strip()
            reminders.append(task)
            responses.append(f"Reminder added: {task}")
            text_to_speech(f"Reminder added: {task}")
        if "show reminders" in user_data:
            if reminders:
                all_reminders = "; ".join(reminders)
                responses.append(f"Your reminders: {all_reminders}")
                text_to_speech(f"Your reminders are: {all_reminders}")
            else:
                responses.append("You have no reminders.")
                text_to_speech("You have no reminders.")
        # Definitions
        if user_data.startswith("define ") or (user_data.startswith("what does ") and "mean" in user_data):
            word = user_data.split("define ")[-1].strip() if "define " in user_data else user_data.split("what does ")[-1].split(" mean")[0].strip()
            definition = get_definition(word)
            responses.append(f"Definition of {word}: {definition}")
            text_to_speech(f"Definition of {word}: {definition}")
        # Weather (already handled above)
        # Fallback
        if not responses:
            responses.append("I am sorry, I am not able to understand you right now.")
            text_to_speech("I am sorry, I am not able to understand you right now.")
    except Exception as e:
        logger.error(f"Error in known actions: {e}")
    return responses

# Helper to add to conversation history
def add_to_history(role, content):
    conversation_history.append({"role": role, "content": content})
    # Limit history to last 10 exchanges for brevity
    if len(conversation_history) > 10:
        conversation_history.pop(0)

# Fix sys.path and import for gemini_integration
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gemini_integration import ask_gemini as gemini_raw

def ask_gemini(query):
    # Compose context for Gemini
    context_text = "\n".join([
        f"{item['role']}: {item['content']}" for item in conversation_history
    ])
    prompt = f"{context_text}\nuser: {query}\nassistant:"
    return gemini_raw(prompt)

# Advanced context tracking for last entity/topic
last_entity = None

def extract_entity_from_response(response):
    # Simple heuristic: look for capitalized words in Gemini's answer
    import re
    matches = re.findall(r'\b([A-Z][a-z]+)\b', response)
    if matches:
        return matches[0]  # Return the first capitalized word (e.g., 'Paris', 'France')
    return None

def format_response(response):
    """
    Clean and format the response for clarity and readability.
    - Convert markdown-style **bold** to HTML <b> tags
    - Add line breaks for lists or multi-part answers
    - Add emoticons and punctuation for friendliness and clarity
    - Remove excessive whitespace
    - Capitalize first letter
    - Truncate overly long responses at a sentence boundary
    - Add spacing between sections
    - Convert lists to <ul>/<li>
    - Convert URLs to hyperlinks
    """
    import re
    if not response:
        return "No response."
    # Convert **bold** to <b> tags
    response = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', response)
    # Convert numbered lists to <ul><li>
    def numbered_list_to_ul(text):
        lines = text.splitlines()
        in_list = False
        new_lines = []
        for line in lines:
            m = re.match(r'\s*(\d+)\.\s+(.*)', line)
            if m:
                if not in_list:
                    new_lines.append('<ul>')
                    in_list = True
                new_lines.append(f'<li>{m.group(2)}</li>')
            else:
                if in_list:
                    new_lines.append('</ul>')
                    in_list = False
                new_lines.append(line)
        if in_list:
            new_lines.append('</ul>')
        return '\n'.join(new_lines)
    response = numbered_list_to_ul(response)
    # Convert bullet lists to <ul><li>
    response = re.sub(r'(?:^|\n)[\-•]\s*(.+)', r'<ul><li>\1</li></ul>', response)
    # Merge adjacent <ul>
    response = re.sub(r'</ul>\s*<ul>', '', response)
    # Convert URLs to clickable links
    response = re.sub(r'(https?://[\w\-./?%&=#:]+)', r'<a href="\1" target="_blank">\1</a>', response)
    # Add line breaks after periods, question marks, exclamation marks (but not inside <b> tags)
    response = re.sub(r'(?<!<b>)([.!?])\s+', r'\1<br><br>', response)
    # Add emoticons for friendliness and clarity
    response = re.sub(r'\bhello\b', 'Hello 👋', response, flags=re.IGNORECASE)
    response = re.sub(r'\bthank you\b', 'Thank you 🙏', response, flags=re.IGNORECASE)
    response = re.sub(r'\bgoodbye\b', 'Goodbye 👋', response, flags=re.IGNORECASE)
    response = re.sub(r'\bcongratulations\b', 'Congratulations 🎉', response, flags=re.IGNORECASE)
    response = re.sub(r'\bimportant\b', 'important ⚡', response, flags=re.IGNORECASE)
    response = re.sub(r'\btip\b', 'Tip 💡', response, flags=re.IGNORECASE)
    response = re.sub(r'\bwarning\b', 'Warning ⚠️', response, flags=re.IGNORECASE)
    response = re.sub(r'\bnote\b', 'Note 📝', response, flags=re.IGNORECASE)
    response = re.sub(r'\bproject\b', 'project 📊', response, flags=re.IGNORECASE)
    response = re.sub(r'\bdata\b', 'data 📈', response, flags=re.IGNORECASE)
    response = re.sub(r'\bemail\b', 'email ✉️', response, flags=re.IGNORECASE)
    response = re.sub(r'\bweather\b', 'weather ☀️', response, flags=re.IGNORECASE)
    response = re.sub(r'\breminder\b', 'reminder ⏰', response, flags=re.IGNORECASE)
    # Remove excessive <br> tags
    response = re.sub(r'(<br>\s*){2,}', '<br><br>', response)
    # Remove excessive whitespace
    response = re.sub(r'\s+', ' ', response).strip()
    # Capitalize first letter
    response = response[0].upper() + response[1:] if response else response
    # Truncate at a sentence boundary if too long, but only summarize if '[Response truncated]' is explicitly mentioned in the response
    max_len = 900
    if len(response) > max_len and '[Response truncated]' in response:
        trunc = response[:max_len]
        last_period = trunc.rfind('.<br><br>')
        if last_period != -1:
            response = trunc[:last_period+6] + "...<br><br>[Response truncated]"
        else:
            response = trunc + "...<br><br>[Response truncated]"
    return response

# Update handle_query to track last entity

def handle_query(query):
    logging.info(f"User query: {query}")
    add_to_history("user", query)
    global last_entity
    intent, entities = extract_intent_entities(query)
    responses = []
    # Always check for direct open/system commands before intent logic
    user_data = query.lower()
    # File explorer, drives, browser, system (ALWAYS RUN these commands if present)
    opened = False
    try:
        if "open youtube" in user_data:
            webbrowser.open("https://www.youtube.com/")
            opened = True
        if "open google" in user_data:
            webbrowser.open("https://www.google.com/")
            opened = True
        if "open gmail" in user_data:
            webbrowser.open("https://mail.google.com/mail/u/jhabarkha808@gmail.com")
            opened = True
        if "open github" in user_data:
            webbrowser.open("https://www.github.com/")
            opened = True
        if "play music" in user_data:
            webbrowser.open("https://www.spotify.com/")
            opened = True
        if "open e drive" in user_data or "open e:" in user_data:
            webbrowser.open("file:///E:/")
            opened = True
        if "open c drive" in user_data or "open c:" in user_data:
            webbrowser.open("file:///C:/")
            opened = True
        if "open file explorer" in user_data:
            open_file_explorer()
            opened = True
        if "open recycle bin" in user_data:
            open_recycle_bin()
            opened = True
        if "open vscode" in user_data or "open visual studio code" in user_data:
            open_vscode()
            opened = True
        if "open settings" in user_data:
            try:
                os.startfile("ms-settings:")
                opened = True
            except Exception:
                pass
    except Exception as e:
        logging.error(f"Error running open/system command: {e}")
    # If a direct open command was run, still return the formatted response as before
    try:
        # Weather
        if intent == "weather":
            city = entities.get("city") or extract_city(query)
            if not city:
                responses.append("Please specify a city name to get the weather information.")
            else:
                ans = weather(city)
                responses.append(ans)
                last_entity = city
        elif intent == "reminder":
            task = entities.get("task")
            time_str = entities.get("time")
            if task and time_str:
                now = datetime.datetime.now()
                try:
                    remind_time = datetime.datetime.strptime(time_str, "%I%p")
                    remind_time = remind_time.replace(year=now.year, month=now.month, day=now.day)
                    if remind_time < now:
                        remind_time += datetime.timedelta(days=1)
                except Exception:
                    remind_time = now + datetime.timedelta(minutes=1)
                add_reminder(task, remind_time)
                responses.append(f"Reminder set for {task} at {remind_time.strftime('%I:%M %p')}")
            else:
                responses.append("Please specify what and when to remind you, e.g., 'Remind me to call John at 5pm'.")
        elif intent == "definition":
            word = entities.get("word")
            if word:
                definition = get_definition(word)
                responses.append(f"Definition of {word}: {definition}")
            else:
                responses.append("Please specify a word to define.")
        if responses:
            response_text = "\n".join(responses)
            response_text = format_response(response_text)
            add_to_history("assistant", response_text)
            entity = extract_entity_from_response(response_text)
            if entity:
                last_entity = entity
            logging.info(f"Response from NLP/known actions: {responses}")
            return response_text
        follow_ups = ["what about", "its population", "that city", "that country", "it"]
        if any(phrase in query.lower() for phrase in follow_ups) and last_entity:
            query = f"{query} ({last_entity})"
        try:
            gemini_response = ask_gemini(query)
            gemini_response = format_response(gemini_response)
            add_to_history("assistant", gemini_response)
            entity = extract_entity_from_response(gemini_response)
            if entity:
                last_entity = entity
            logging.info(f"Response from Gemini: {gemini_response}")
            return gemini_response
        except Exception as e:
            logging.error(f"Error in Gemini integration: {e}")
            return "Sorry, I couldn't process your request right now."
    except Exception as e:
        logging.error(f"Error in query handling: {e}")
        return "Sorry, I couldn't process your request right now."
