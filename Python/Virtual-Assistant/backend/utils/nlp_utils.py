import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)

# Add a pattern for reminders (e.g., 'remind me to ... at ...')
reminder_pattern = [
    {"LOWER": "remind"},
    {"LOWER": "me"},
    {"LOWER": "to"},
    {"OP": "*"},
    {"LOWER": "at", "OP": "?"},
    {"IS_DIGIT": True, "OP": "?"}
]
matcher.add("REMINDER", [reminder_pattern])

def extract_intent_entities(text):
    doc = nlp(text)
    intent = "general"
    entities = {}
    # Definition intent
    if "define" in text.lower() or "definition" in text.lower():
        intent = "definition"
        # Try to extract the word after "define"
        tokens = text.lower().split()
        if "define" in tokens:
            idx = tokens.index("define")
            if idx + 1 < len(tokens):
                entities["word"] = tokens[idx + 1]
        # Fallback: use first NOUN entity
        for ent in doc.ents:
            if ent.label_ == "NOUN":
                entities["word"] = ent.text
    # Weather intent
    if any(tok.lemma_ == "weather" for tok in doc):
        intent = "weather"
        for ent in doc.ents:
            if ent.label_ == "GPE":
                entities["city"] = ent.text
    # Reminder intent
    matches = matcher(doc)
    if matches:
        intent = "reminder"
        # Extract time and task
        for ent in doc.ents:
            if ent.label_ in ["TIME", "DATE"]:
                entities["time"] = ent.text
        # Extract task (text after 'to')
        for i, tok in enumerate(doc):
            if tok.text.lower() == "to":
                entities["task"] = doc[i+1:].text
                break
    # Fallback: extract GPE for city, TIME for time
    if intent == "general":
        for ent in doc.ents:
            if ent.label_ == "GPE":
                entities["city"] = ent.text
            if ent.label_ == "TIME":
                entities["time"] = ent.text
    return intent, entities
