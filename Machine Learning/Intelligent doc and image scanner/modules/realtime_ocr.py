import cv2
import easyocr
import pandas as pd
from datetime import datetime
import numpy as np
import logging
logger = logging.getLogger()


def start_realtime_ocr(save_csv=False):
    # Initialize the OCR reader
    reader = easyocr.Reader(['en'])
    cap = cv2.VideoCapture(0)  # 0 means your default webcam
    
    print("📸 Starting real-time OCR... Press 'q' to quit.")
    results = []

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Failed to grab frame")
            break

        # Convert to grayscale for better performance
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Perform OCR
        detections = reader.readtext(gray)

        for (bbox, text, confidence) in detections:
            # Draw bounding box
            (top_left, top_right, bottom_right, bottom_left) = bbox
            pts = [tuple(map(int, point)) for point in [top_left, top_right, bottom_right, bottom_left]]
            cv2.polylines(frame, [np.array(pts)], isClosed=True, color=(0, 255, 0), thickness=2)

            # Display detected text and confidence
            cv2.putText(frame, f"{text} ({confidence:.2f})", (pts[0][0], pts[0][1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # Log detected text
            logger.info(f"Detected text: {text} ({confidence:.2f})")

            # Save detected text
            results.append({
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Text": text,
                "Confidence": confidence
            })

        # Show live window
        cv2.imshow("🧠 IDIS - Real-Time OCR", frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release camera
    cap.release()
    cv2.destroyAllWindows()

    # Save results to CSV if requested
    if save_csv and results:
        try:
            df = pd.DataFrame(results)
            csv_path = "results/csv/realtime_ocr_results.csv"
            df.to_csv(csv_path, index=False)
            logger.info(f"✅ Saved results to {csv_path}")
        except Exception as e:
            logger.error(f"Failed to save results to CSV: {str(e)}")