IDIS Project
===========

Simple OCR extraction pipeline for PDFs and images.

Prerequisites
-------------
- Python 3.8+
- Tesseract OCR installed and on PATH: https://github.com/tesseract-ocr/tesseract
- Poppler installed (for PDF -> images): https://poppler.freedesktop.org/ (Windows builds available)

Python dependencies
-------------------
See `requirements.txt`. Install with:

    pip install -r requirements.txt

Usage
-----
Place PDFs or images into `data/raw_docs/` then run the extractor:

    python src/ocr_extraction.py --input data/raw_docs --output data/extracted_text

By default the script will:
- convert PDFs to images (one image per page)
- run Tesseract OCR on each image
- save per-file text (.txt) and a combined CSV `extracted.csv` with columns: filename, page, text

Notes
-----
- For scanned PDFs and complex layouts, OCR accuracy varies.
- You can set the TESSDATA_PREFIX environment variable if tesseract data isn't on PATH.
- The script includes basic logging and error handling.
