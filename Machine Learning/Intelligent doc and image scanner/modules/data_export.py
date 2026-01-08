# modules/data_export.py
import pandas as pd
import sqlite3
from datetime import datetime
import os

def normalize_columns(df):
    """Normalize column names to be consistent across exports."""
    # Replace spaces and special characters with underscores
    df.columns = [col.replace(" ", "_").replace("-", "_") for col in df.columns]
    # Ensure no CamelCase causes issues (e.g., DocType -> doc_type)
    df.columns = [col.lower() for col in df.columns]
    return df

def export_to_csv(data_records, output_path):
    """Save OCR results to CSV with timestamp."""
    df = pd.DataFrame(data_records)
    df = normalize_columns(df)
    df["export_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"✅ CSV saved to: {output_path}")

def export_to_sqlite(data_records, db_path="results/ocr_results.db"):
    """Export OCR results to SQLite database with proper column naming."""
    df = pd.DataFrame(data_records)
    df = normalize_columns(df)
    df["export_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    
    try:
        # Drop existing table to ensure schema consistency
        try:
            conn.execute("DROP TABLE IF EXISTS ocr_results")
        except:
            pass
            
        df.to_sql("ocr_results", conn, if_exists="replace", index=False)
        print(f"💾 Data inserted into SQLite DB: {db_path}")
    finally:
        conn.close()
