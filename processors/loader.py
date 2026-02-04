import pandas as pd
import os

def load_file(file_path):
    _, ext = os.path.splitext(file_path.lower())
    if ext == '.csv': return pd.read_csv(file_path)
    if ext in ['.xlsx', '.xls']: return pd.read_excel(file_path)
    if ext == '.json': return pd.read_json(file_path)
    if ext == '.xml': return pd.read_xml(file_path)
    raise ValueError("Format non supporté")
