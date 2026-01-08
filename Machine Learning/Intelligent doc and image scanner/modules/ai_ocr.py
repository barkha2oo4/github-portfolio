import cv2
import numpy as np
from PIL import Image
import logging
from typing import Union, Any

logger = logging.getLogger("IDIS")

# Lazy-loaded TrOCR model and processor (typed as Any to avoid static-checker complaints)
_TROCR: Any = None
_PROCESSOR: Any = None


def _ensure_trocr_loaded():
    global _TROCR, _PROCESSOR
    if _TROCR is not None and _PROCESSOR is not None:
        return True
    try:
        from transformers import TrOCRProcessor, VisionEncoderDecoderModel
        _PROCESSOR = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
        _TROCR = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")
        logger.info("Loaded TrOCR handwriting model")
        return True
    except Exception as e:
        logger.warning(f"TrOCR model not available: {e}")
        _TROCR = None
        _PROCESSOR = None
        return False


def is_handwritten(image: Union[str, np.ndarray]) -> bool:
    """Return True if image likely contains handwritten text.

    Accepts either a file path or a BGR numpy array.
    Uses simple heuristics (edge density, grayscale variance).
    """
    if isinstance(image, str):
        img = cv2.imread(image)
        if img is None:
            return False
    else:
        img = image

    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if img.ndim == 3 else img
        # ensure numeric dtype for np.var
        arr = np.asarray(gray, dtype=np.float32)
        edges = cv2.Canny(arr.astype(np.uint8), 50, 150)
        edge_density = float(np.sum(edges > 0)) / edges.size
        variance = float(np.var(arr))

        # Heuristic thresholds (conservative defaults)
        # Handwritten text tends to have higher edge density and lower global variance
        if edge_density > 0.10 and variance < 7000:
            return True
        return False
    except Exception as e:
        logger.debug(f"Handwritten detection failed: {e}")
        return False


def trocr_handwriting_ocr(image: Union[str, np.ndarray]) -> str:
    """Perform OCR using Microsoft TrOCR handwriting model.

    Accepts a file path or a BGR numpy array. Returns decoded text or empty string on failure.
    """
    if not _ensure_trocr_loaded():
        return ""

    try:
        if isinstance(image, str):
            pil_img = Image.open(image).convert("RGB")
        else:
            # Convert BGR numpy array to PIL Image
            if image.ndim == 2:
                pil_img = Image.fromarray(image)
            else:
                pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # _PROCESSOR and _TROCR are typed as Any
        assert _PROCESSOR is not None and _TROCR is not None
        # Prepare inputs (use batch of one)
        inputs = _PROCESSOR(images=pil_img, return_tensors="pt")  # type: ignore[arg-type]
        pixel_values = inputs.pixel_values  # type: ignore[attr-defined]
        generated_ids = _TROCR.generate(pixel_values)  # type: ignore[call-arg]
        text = _PROCESSOR.batch_decode(generated_ids, skip_special_tokens=True)[0]  # type: ignore[attr-defined]
        return text.strip()
    except Exception as e:
        logger.error(f"TrOCR handwriting OCR failed: {e}")
        return ""
