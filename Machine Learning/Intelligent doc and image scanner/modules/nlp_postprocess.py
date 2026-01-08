"""NLP post-processing module for text validation and correction.

This module provides lightweight spelling correction, confidence scoring, and
normalization helpers for common structured fields (name, organization, date,
amounts). It includes targeted normalization for organization strings to
recover common OCR errors (e.g. `B.Lech` -> `B.Tech`, `CSE-Of latch` -> `CSE`).
"""

from functools import lru_cache
import re
from textblob import TextBlob
from rapidfuzz import fuzz, process
from typing import Dict, Tuple, Any


@lru_cache(maxsize=1024)
def correct_spelling(text: str) -> str:
    """Auto-correct spelling mistakes in extracted text (cached).

    Uses TextBlob but caches results to avoid repeated expensive calls.
    """
    if not isinstance(text, str):
        return str(text)
    try:
        corrected = str(TextBlob(text).correct())
        return corrected
    except Exception:
        return text


def compute_confidence(original: str, corrected: str) -> float:
    """Compare original vs corrected text for confidence score (0.0-1.0)."""
    if not isinstance(original, str):
        original = str(original)
    if not isinstance(corrected, str):
        corrected = str(corrected)
    return round(fuzz.ratio(original, corrected) / 100, 3)


# Canonical lists for normalization
_DEGREES = {
    r"b\.?tech\b": "B.Tech",
    r"b\.?e\b": "B.E",
    r"b\.?sc\b": "B.Sc",
    r"m\.?tech\b": "M.Tech",
    r"m\.?sc\b": "M.Sc",
    r"ph\.?d\b": "Ph.D",
}

_DEPARTMENTS = [
    "Computer Science and Engineering",
    "CSE",
    "Electronics and Communication",
    "ECE",
    "Mechanical Engineering",
    "Civil Engineering",
    "Electrical Engineering",
]

_ORG_TYPES = ["College", "Institute", "University", "Department", "Office", "Center"]


def _regex_find_degree(text: str) -> Tuple[str, float]:
    """Find and normalize degree mentions using regex mapping.

    Returns (normalized_degree or empty, score)
    """
    txt = text.lower()
    for pat, canon in _DEGREES.items():
        if re.search(pat, txt):
            return canon, 1.0
    return "", 0.0


def _fuzzy_match_department(text: str) -> Tuple[str, float]:
    """Attempt fuzzy matching of department names from known list."""
    if not text:
        return "", 0.0
    # Use rapidfuzz to get best match
    res = process.extractOne(text, _DEPARTMENTS)
    if not res:
        return "", 0.0
    choice, score, _ = res
    return (choice, score / 100.0) if score else ("", 0.0)


def normalize_organization(text: str) -> Tuple[str, float]:
    """Normalize organization strings to canonical components.

    Returns (normalized_text, confidence_score).
    """
    if not text or not isinstance(text, str):
        return "", 0.0

    orig = text.strip()
    working = orig

    # quick cleanup of obvious OCR artifacts
    working = working.replace('_', ' ').replace('|', 'I').replace('0f', 'of')

    # Try to find degree
    degree, deg_score = _regex_find_degree(working)

    # Try fuzzy department match on the whole string
    dept, dept_score = _fuzzy_match_department(working)

    # If dept is generic (CSE) but original contains acronym-like tokens (C S E), try simple token fix
    if not dept and re.search(r'\b(c\W?s\W?e)\b', working, re.I):
        dept = 'CSE'
        dept_score = 0.9

    # Build normalized pieces
    pieces = []
    if degree:
        pieces.append(degree)
    if dept:
        pieces.append(dept)

    # Try to extract org type (College/Institute/University)
    found_type = None
    for t in _ORG_TYPES:
        if re.search(rf'\b{re.escape(t.lower())}\b', working.lower()):
            found_type = t
            break
    if found_type:
        pieces.append(found_type)

    normalized = " ".join(pieces).strip()

    # If normalization found nothing useful, fallback to light spelling correction
    if not normalized:
        corrected = correct_spelling(orig)
        conf = compute_confidence(orig, corrected)
        return corrected, conf

    # Compute final confidence as combination of component scores
    comp_scores = []
    if deg_score:
        comp_scores.append(deg_score)
    if dept_score:
        comp_scores.append(dept_score)
    if comp_scores:
        final_conf = sum(comp_scores) / len(comp_scores)
    else:
        final_conf = 0.5

    # Re-check similarity vs original
    final_conf = (final_conf + compute_confidence(orig, normalized)) / 2.0
    return normalized, round(final_conf, 3)


def validate_fields(fields: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, float]]:
    """
    Validate extracted fields using targeted NLP logic.

    - Applies spelling correction for `name`.
    - Applies structured normalization for `organization` (degrees, departments).
    - Leaves numeric/date fields untouched and assigns high confidence (1.0).
    - Returns (validated_fields, confidence_scores)
    """
    if not isinstance(fields, dict):
        return {}, {}

    validated: Dict[str, Any] = {}
    confidence: Dict[str, float] = {}

    for key, value in fields.items():
        if value is None:
            continue
        k = key.lower()
        v = str(value).strip()
        if not v:
            continue

        if k == 'name':
            corrected = correct_spelling(v)
            validated[key] = corrected
            confidence[key] = compute_confidence(v, corrected)
        elif k == 'organization' or k == 'org':
            # Normalize organization strings
            normalized, conf = normalize_organization(v)
            validated[key] = normalized if normalized else v
            confidence[key] = conf if conf is not None else 0.0
        else:
            # Pass-through for numeric/date/other fields
            validated[key] = v
            confidence[key] = 1.0

    return validated, confidence
