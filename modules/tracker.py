import pandas as pd
import os

CSV_FILE = "job_applications.csv"

def load_applications():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            if df.empty or df.columns.size == 0:
                return []
            return df.to_dict(orient="records")
        except pd.errors.EmptyDataError:
            return []
    return []

