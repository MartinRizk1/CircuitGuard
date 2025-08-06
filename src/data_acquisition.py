# Data Acquisition Module
# Handles importing and preprocessing PCB test data

import pandas as pd
import os

def import_data(file_path):
    """
    Imports PCB test data from a CSV or Excel file.
    Returns a pandas DataFrame.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    _, ext = os.path.splitext(file_path)
    if ext.lower() == '.csv':
        df = pd.read_csv(file_path)
    elif ext.lower() in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file type. Please use CSV or Excel.")
    # Basic preprocessing: drop empty rows/columns
    df = df.dropna(axis=0, how='all').dropna(axis=1, how='all')
    return df
