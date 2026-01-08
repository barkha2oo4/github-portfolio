import re
import spacy

nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    """Basic cleaning of OCR output"""
    if not text:
        return ""
    # Preserve case for better NER
    text = text.replace('\n', ' ')
    text = re.sub(r'[^\w\s:/.-]', ' ', text)  # preserve alphanumeric and some special chars
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_fields(text):
    """Extract common structured fields using regex + NLP"""
    fields = {}
    
    if not text:
        return fields

    # 🔹 Name (using spaCy NER)
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            fields["name"] = ent.text.strip()
            break
    
    # Extract any numeric ID numbers
    id_match = re.search(r'(?:id|number|no)[\s.:#-]*([A-Z0-9]{4,})', text, re.I)
    if id_match:
        fields["id_number"] = id_match.group(1).strip()

    # 🔹 Totals (more flexible pattern)
    total_match = re.search(r'(?:total|amount|sum|price)\s*[:\-]?\s*[\$£€]?\s*(\d+[.,]?\d*)', text, re.I)
    if total_match:
        fields["total_amount"] = total_match.group(1).strip()

    # 🔹 Date (multiple formats)
    date_patterns = [
        r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',  # DD/MM/YYYY
        r'(\d{4}[/-]\d{1,2}[/-]\d{1,2})',     # YYYY/MM/DD
        r'(\d{1,2}(?:st|nd|rd|th)?\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4})'  # 1st January 2025
    ]
    
    for pattern in date_patterns:
        date_match = re.search(pattern, text, re.I)
        if date_match:
            fields["date"] = date_match.group(1).strip()
            break

    # Look for organization names
    for ent in doc.ents:
        if ent.label_ in ["ORG", "FAC"]:
            fields["organization"] = ent.text.strip()
            break

    return fields
