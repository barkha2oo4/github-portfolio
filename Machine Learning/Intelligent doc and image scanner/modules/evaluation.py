"""OCR evaluation module for measuring text extraction accuracy.

This module provides:
- Word Error Rate (WER) calculation
- Character Error Rate (CER) calculation
- Text normalization and comparison utilities
"""

import logging
logger = logging.getLogger("IDIS")
from typing import Tuple


def edit_distance(a: list, b: list) -> int:
    """Compute Levenshtein edit distance between sequences a and b."""
    na = len(a)
    nb = len(b)
    if na == 0:
        return nb
    if nb == 0:
        return na

    prev = list(range(nb + 1))
    for i in range(1, na + 1):
        cur = [i] + [0] * nb
        for j in range(1, nb + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            cur[j] = min(prev[j] + 1,      # deletion
                         cur[j - 1] + 1,   # insertion
                         prev[j - 1] + cost)  # substitution
        prev = cur
    return prev[nb]


def cer(ref: str, hyp: str) -> float:
    """Character Error Rate: edits / len(ref_chars). Returns float in [0,1]."""
    ref_chars = list(ref) if ref is not None else []
    hyp_chars = list(hyp) if hyp is not None else []
    if len(ref_chars) == 0:
        return 0.0 if len(hyp_chars) == 0 else 1.0
    edits = edit_distance(ref_chars, hyp_chars)
    return edits / len(ref_chars)


def wer(ref: str, hyp: str) -> float:
    """Word Error Rate: edits / len(ref_words). Treats words split on whitespace."""
    ref_words = ref.split() if ref is not None else []
    hyp_words = hyp.split() if hyp is not None else []
    if len(ref_words) == 0:
        return 0.0 if len(hyp_words) == 0 else 1.0
    edits = edit_distance(ref_words, hyp_words)
    return edits / len(ref_words)


def evaluate_ocr(true_text: str, predicted_text: str) -> Tuple[float, float]:
    """Return (wer_score, cer_score) for the given reference and hypothesis texts.

    Scores are returned as floats (not rounded). Caller may round/format as desired.
    """
    w = wer(true_text or "", predicted_text or "")
    c = cer(true_text or "", predicted_text or "")
    return w, c
