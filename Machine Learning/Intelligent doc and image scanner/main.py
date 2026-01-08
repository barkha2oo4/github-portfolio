import os
import sys
from datetime import datetime
import cv2
import pytesseract
import easyocr
import pandas as pd
from modules.image_preprocess import preprocess_image
from modules.text_extraction import extract_text
from modules.text_cleaning import clean_text, extract_fields
from modules.nlp_postprocess import validate_fields
from modules.data_export import export_to_csv, export_to_sqlite
from modules.realtime_ocr import start_realtime_ocr
from modules.logger_config import setup_logger
from modules.evaluation import evaluate_ocr

# Optional AI handwriting OCR (TrOCR)
try:
    from modules.ai_ocr import is_handwritten, trocr_handwriting_ocr
    _AI_OCR_AVAILABLE = True
except Exception:
    _AI_OCR_AVAILABLE = False


# Initialize logger
logger = setup_logger()

# Detect tesseract availability and configure pytesseract accordingly
import shutil
tess_env = os.environ.get('TESSERACT_CMD') or os.environ.get('TESSERACT_PATH')
has_tesseract = False
if tess_env:
    try:
        pytesseract.pytesseract.tesseract_cmd = tess_env
        pytesseract.get_tesseract_version()
        has_tesseract = True
        logger.info(f"Using TESSERACT_CMD from environment: {tess_env}")
    except Exception as e:
        logger.warning(f"Environment TESSERACT_CMD provided but failed to run: {e}")
else:
    tpath = shutil.which("tesseract")
    if tpath:
        try:
            pytesseract.pytesseract.tesseract_cmd = tpath
            pytesseract.get_tesseract_version()
            has_tesseract = True
            logger.info(f"Found tesseract executable at: {tpath}")
        except Exception as e:
            logger.warning(f"Tesseract found at {tpath} but calling it failed: {e}")
    else:
        logger.warning("Tesseract not found on PATH; pytesseract will be unavailable. Falling back to EasyOCR-only where needed.")


# Global constants
input_dir = "data/input_images"
output_dir = "results/csv"
error_log_dir = "results/logs"

def process_batch_images():
    """Process all images in the input directory and save results."""
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(error_log_dir, exist_ok=True)
    data_records = []
    
    try:
        # Initialize EasyOCR
        reader = easyocr.Reader(['en'])
        logger.info("Initialized EasyOCR reader")
        
        # Walk input_dir recursively so we process images in all subfolders
        for root, _, files in os.walk(input_dir):
            for filename in files:
                if not filename.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")):
                    continue

                filepath = os.path.join(root, filename)
                # Category is the first-level subfolder under input_dir (e.g. receipts_invoices)
                rel = os.path.relpath(root, input_dir)
                category = rel.split(os.sep)[0] if rel not in (".", ".\\") else ""

                try:
                    logger.info(f"🔍 Processing: {filename} (category: {category})")

                    # Read raw image and preprocess
                    raw_img = cv2.imread(filepath)
                    if raw_img is None:
                        raise ValueError(f"Could not read image: {filepath}")
                    img = preprocess_image(raw_img)

                    # Decide OCR engine: TrOCR for handwriting if available, otherwise EasyOCR+Tesseract
                    text = ""
                    used_trocr = False
                    try:
                        if _AI_OCR_AVAILABLE and is_handwritten(raw_img):
                            logger.info("✍️ Detected Handwritten Text → Using TrOCR")
                            text = trocr_handwriting_ocr(raw_img)
                            if text:
                                used_trocr = True
                            else:
                                logger.warning("TrOCR returned no text; falling back to EasyOCR+Tesseract")
                        if not text:
                            logger.info("🖨️ Using EasyOCR + Tesseract")
                            text = extract_text(img, reader)
                    except Exception as e:
                        logger.error(f"Error during AI OCR decision/TrOCR run: {e}")
                        # Fallback to default
                        text = extract_text(img, reader)

                    # Step 1: Clean & Extract
                    cleaned = clean_text(text)
                    fields = extract_fields(cleaned)
                    logger.info(f"📄 Extracted Fields for {filename}: {fields}")

                    # Step 2: Validate with NLP
                    validated_fields, confidence_scores = validate_fields(fields)
                    logger.info(f"✅ Validated Fields: {validated_fields}")
                    logger.info(f"📊 Confidence Scores: {confidence_scores}")

                    # Step 3: Determine document type automatically (or from OCR choice)
                    if used_trocr:
                        doc_type = "Handwritten"
                    elif "receipt" in filename.lower():
                        doc_type = "Receipt"
                    elif "id" in filename.lower():
                        doc_type = "ID Card"
                    else:
                        doc_type = "Document"
                    logger.info(f"📑 Document Type: {doc_type}")

                    # Step 4: Save structured data to records with consistent column naming
                    data_records.append({
                        "filename": filename,
                        "doc_type": doc_type,
                        "category": category,
                        "path": filepath,
                        "extracted_text": cleaned,
                        **{k.lower(): v for k, v in validated_fields.items()},
                        **{f"{k.lower()}_conf": v for k, v in confidence_scores.items()}
                    })
                    logger.info(f"✅ Extraction successful for {filename} (category: {category})")

                except Exception as e:
                    logger.error(f"❌ Error processing {filename} (category: {category}): {e}")
                    with open(os.path.join(error_log_dir, "error_summary.log"), "a", encoding="utf-8") as f:
                        f.write(f"{datetime.now()} | {filepath} | {str(e)}\n")

        # Export results if we have any data
        if data_records:
            try:
                # Export to CSV
                csv_path = os.path.join(output_dir, "ocr_results.csv")
                export_to_csv(data_records, csv_path)
                logger.info(f"✅ Extraction completed! Results saved to {csv_path}")

                # Push to SQLite DB
                export_to_sqlite(data_records)
                logger.info("✅ Data successfully exported to SQLite DB")
            except Exception as e:
                logger.error(f"Error during data export: {str(e)}")
                raise
        else:
            logger.warning("No data was processed successfully.")

    except Exception as e:
        logger.critical(f"Critical error in batch processing: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        logger.info("IDIS OCR System Starting...")
        logger.info("Choose Mode:")
        logger.info("1️⃣ - Batch Image OCR (from data/input_images)")
        logger.info("2️⃣ - Real-Time OCR via Webcam")

        # Support a non-interactive batch run via CLI flag: `python main.py --batch`
        if len(sys.argv) > 1 and sys.argv[1] in ("--batch", "-b"):
            logger.info("Running in batch mode (CLI flag detected)")
            process_batch_images()
            sys.exit(0)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            logger.info("Starting batch OCR processing...")
            process_batch_images()
        elif choice == "2":
            logger.info("Starting real-time OCR via webcam...")
            start_realtime_ocr(save_csv=True)
        else:
            logger.error("Invalid choice selected!")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Unexpected error: {str(e)}")
        sys.exit(1)