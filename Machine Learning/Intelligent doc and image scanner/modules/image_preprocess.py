import cv2
import numpy as np
from pathlib import Path
from typing import Union

def preprocess_image(image: Union[str, Path, np.ndarray], *, clahe_clip: float = 3.0, target_min_dim: int = 800) -> np.ndarray:
    """
    Advanced adaptive preprocessing for OCR-ready image.
    
    Args:
        image: Either a file path (str/Path) or numpy array (BGR/RGB format)
        
    Returns:
        Preprocessed image as numpy array
    """
    if isinstance(image, (str, Path)):
        # Load image from file
        img = cv2.imread(str(image))
        if img is None:
            raise ValueError(f"Could not load image from {image}")
    elif isinstance(image, np.ndarray):
        # Use array directly
        img = image.copy()
    else:
        raise TypeError("Expected image path or numpy array")

    # 1️⃣ Convert to grayscale (handle both BGR and RGB inputs)
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()

    # 2️⃣ Contrast limited adaptive histogram equalization (better for uneven lighting)
    clahe = cv2.createCLAHE(clipLimit=float(clahe_clip), tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    # 3️⃣ Remove noise while preserving edges
    gray = cv2.bilateralFilter(gray, 9, 75, 75)

    # 4️⃣ Adaptive thresholding (handles lighting variations)
    adaptive = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        15, 8
    )

    # 5️⃣ Morphological opening (remove small dots & shadows)
    kernel = np.ones((2, 2), np.uint8)
    morph = cv2.morphologyEx(adaptive, cv2.MORPH_OPEN, kernel, iterations=1)

    # 6️⃣ Dilation to strengthen thin characters
    dilated = cv2.dilate(morph, kernel, iterations=1)

    # 7️⃣ Optional deskew (only if we have foreground pixels)
    coords = np.column_stack(np.where(dilated > 0))
    deskewed = dilated
    if coords.size and coords.shape[0] > 10:
        try:
            angle = cv2.minAreaRect(coords)[-1]
            if angle < -45:
                angle = -(90 + angle)
            else:
                angle = -angle
            (h, w) = dilated.shape[:2]
            M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
            deskewed = cv2.warpAffine(dilated, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        except Exception:
            # If deskew fails, fall back to the dilated image
            deskewed = dilated

    # 8️⃣ Upscale / sharpen to help OCR on small text
    h, w = deskewed.shape[:2]
    scale = 1.0
    if min(h, w) < int(target_min_dim):
        scale = int(target_min_dim) / min(h, w)
        deskewed = cv2.resize(deskewed, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC)

    # Unsharp mask (sharpen)
    gaussian = cv2.GaussianBlur(deskewed, (0, 0), sigmaX=1.0)
    sharpened = cv2.addWeighted(deskewed, 1.5, gaussian, -0.5, 0)

    return sharpened
