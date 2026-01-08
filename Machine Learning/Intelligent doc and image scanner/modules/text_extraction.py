"""Text extraction module supporting multiple OCR engines."""
import os
import cv2
import numpy as np
from typing import Optional, List, Union, Tuple
import statistics
import shutil
import logging

logger = logging.getLogger("IDIS")

# Configure Tesseract
pytesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ["PATH"] += os.pathsep + os.path.dirname(pytesseract_path)

# Check Tesseract availability
has_tesseract = False
try:
    import pytesseract
    if os.path.isfile(pytesseract_path):
        pytesseract.pytesseract.tesseract_cmd = pytesseract_path
        version = pytesseract.get_tesseract_version()
        has_tesseract = True
        logger.info(f"Using Tesseract v{version} from: {pytesseract_path}")
except Exception as e:
    logger.warning(f"Tesseract not available: {e}")

def _run_easyocr_on_image(reader, img: np.ndarray) -> Tuple[str, float]:
    """Run EasyOCR on img and return concatenated text + average confidence."""
    try:
        results = reader.readtext(img)
    except Exception as e:
        logger.error(f"EasyOCR failed: {e}")
        return "", 0.0

    texts = []
    confs = []
    for res in results:
        if isinstance(res, (list, tuple)) and len(res) >= 3:
            text = str(res[1]).strip()
            conf = float(res[2]) if res[2] is not None else 0.0
        elif isinstance(res, (list, tuple)) and len(res) > 1:
            text = str(res[1]).strip()
            conf = 0.0
        elif isinstance(res, dict):
            text = str(res.get("text", "")).strip()
            conf = float(res.get("confidence", 0.0)) if res.get("confidence") is not None else 0.0
        else:
            text = str(res).strip()
            conf = 0.0

        if text:
            texts.append(text)
            confs.append(conf)

    avg_conf = float(statistics.mean(confs)) if confs else 0.0
    return " ".join(texts), round(avg_conf, 3)


def extract_text(image: np.ndarray, reader, combine_engines: bool = True) -> str:
    """
    Extract text from image using EasyOCR (multi-scale) and optional Tesseract.

    Strategy:
    - Run EasyOCR on a small set of image scales (1.0, 1.5, 2.0)
    - For each scale collect text + avg confidence
    - Optionally run Tesseract on the best-scale image and merge results

    Returns a best-effort concatenated text string.
    """
    scales = [1.0, 1.5, 2.0]
    candidates: List[Tuple[str, float, float]] = []  # (text, avg_conf, scale)

    h0, w0 = image.shape[:2]
    for s in scales:
        try:
            if s == 1.0:
                img_scaled = image
            else:
                img_scaled = cv2.resize(image, (int(w0 * s), int(h0 * s)), interpolation=cv2.INTER_CUBIC)

            easy_text, easy_conf = _run_easyocr_on_image(reader, img_scaled)
            if easy_text:
                candidates.append((easy_text, easy_conf, s))
                logger.info(f"EasyOCR (scale={s}) extracted text length={len(easy_text)} avg_conf={easy_conf}")
            else:
                logger.warning(f"EasyOCR returned no text at scale {s}")
        except Exception as e:
            logger.error(f"EasyOCR scale {s} failed: {e}")

    # Pick best candidate by avg confidence, fall back to longest text
    best_text = ""
    if candidates:
        # sort by (avg_conf, length)
        candidates.sort(key=lambda t: (t[1], len(t[0])), reverse=True)
        best_text, best_conf, best_scale = candidates[0]
    else:
        best_text, best_conf, best_scale = "", 0.0, 1.0

    # Dynamic recheck: if confidence low, try inverted-contrast image
    best_img = None
    inverted_used = False
    try:
        if best_scale == 1.0:
            best_img = image.copy()
        else:
            best_img = cv2.resize(image, (int(w0 * best_scale), int(h0 * best_scale)), interpolation=cv2.INTER_CUBIC)
    except Exception:
        best_img = image

    conf_threshold = 0.45
    if best_conf < conf_threshold:
        try:
            # Prepare inverted image (ensure single-channel)
            if best_img.ndim == 3:
                inv_base = cv2.cvtColor(best_img, cv2.COLOR_BGR2GRAY)
            else:
                inv_base = best_img
            inv_img = cv2.bitwise_not(inv_base)

            inv_text, inv_conf = _run_easyocr_on_image(reader, inv_img)
            logger.info(f"Inverted recheck: text_len={len(inv_text)} avg_conf={inv_conf}")
            if inv_text:
                # Prefer inverted if it gave higher confidence
                if inv_conf > best_conf:
                    best_text = inv_text
                    best_conf = inv_conf
                    inverted_used = True
                    best_img = inv_img
                elif inv_conf > 0.2 and len(inv_text) > len(best_text):
                    # Otherwise, append inverted result if it adds content
                    best_text = f"{best_text} {inv_text}".strip()
        except Exception as e:
            logger.warning(f"Inverted recheck failed: {e}")

    # Optionally run Tesseract on the best-scale (or inverted) image and merge
    if has_tesseract and combine_engines:
        try:
            t_img = best_img if best_img is not None else image

            # Use a conservative PSM for dense text; tune if you need single-line or sparse text
            tess_config = "--psm 6"
            tess_text = pytesseract.image_to_string(t_img, config=tess_config)
            if tess_text and tess_text.strip():
                logger.info("Tesseract extraction successful; merging results")
                # prefer EasyOCR text, but append any Tesseract-only content
                merged = f"{best_text} {tess_text}" if best_text else tess_text
                return merged.strip()
            else:
                logger.warning("Tesseract returned no text")
        except Exception as e:
            logger.error(f"Tesseract OCR failed: {e}")

    return best_text.strip()
