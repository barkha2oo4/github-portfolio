import time
import pytesseract
import easyocr
from modules.image_preprocess import preprocess_image
from modules.text_extraction import extract_text
from modules.evaluation import evaluate_ocr

reader = easyocr.Reader(['en'])

def run_benchmark(image_path, ground_truth_text):
    results = []

    # -------- EasyOCR --------
    start = time.time()
    easy_text = extract_text(preprocess_image(image_path), reader)
    easy_time = round(time.time() - start, 2)
    easy_wer, easy_cer = evaluate_ocr(ground_truth_text, easy_text)
    results.append({
        "Engine": "EasyOCR",
        "WER": easy_wer,
        "CER": easy_cer,
        "Time_s": easy_time
    })

    # -------- Tesseract --------
    start = time.time()
    tess_text = pytesseract.image_to_string(preprocess_image(image_path))
    tess_time = round(time.time() - start, 2)
    tess_wer, tess_cer = evaluate_ocr(ground_truth_text, tess_text)
    results.append({
        "Engine": "Tesseract",
        "WER": tess_wer,
        "CER": tess_cer,
        "Time_s": tess_time
    })

    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run OCR benchmark on a single image")
    parser.add_argument("image", help="Path to the image file to OCR")
    parser.add_argument("ground_truth", help="Ground truth text or path to a .txt file containing the reference text")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    image = args.image
    gt = args.ground_truth
    # If ground_truth points to a file, read it
    try:
        import os
        if os.path.isfile(gt):
            with open(gt, "r", encoding="utf-8") as f:
                gt_text = f.read()
        else:
            gt_text = gt
    except Exception:
        gt_text = gt

    out = run_benchmark(image, gt_text)
    try:
        if args.json:
            import json
            print(json.dumps(out, ensure_ascii=False, indent=2))
        else:
            # Pretty print table without extra dependencies
            headers = ["Engine", "WER", "CER", "Time_s"]
            rows = [[r['Engine'], f"{r['WER']:.3f}", f"{r['CER']:.3f}", f"{r['Time_s']:.2f}"] for r in out]
            # compute column widths
            col_widths = [max(len(str(x)) for x in col) for col in zip(*(rows + [headers]))]
            fmt = "  ".join(f"{{:<{w}}}" for w in col_widths)
            print(fmt.format(*headers))
            print("-" * (sum(col_widths) + 2 * (len(col_widths)-1)))
            for row in rows:
                print(fmt.format(*row))
    except Exception:
        # Fallback simple print
        for r in out:
            print(f"{r['Engine']}: WER={r['WER']}, CER={r['CER']}, Time={r['Time_s']}s")
