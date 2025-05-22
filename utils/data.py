import os
import pandas as pd

def load_applications(file_path):
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            if df.empty or df.columns.size == 0:
                return []
            return df.to_dict(orient="records")
        except pd.errors.EmptyDataError:
            return []
    return []

def save_applications(file_path, applications):
    columns = ["ID", "Job Title", "Company", "Date Applied", "Status", "Notes"]
    df = pd.DataFrame(applications, columns=columns)
    df.to_csv(file_path, index=False)