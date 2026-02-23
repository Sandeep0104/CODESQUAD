import os
import pandas as pd
from docx import Document
import json

def extract_ehr(input_path, output_path):
    print(f"Extracting {input_path} to {output_path}...")
    try:
        df = pd.read_excel(input_path)
        df.to_csv(output_path, index=False)
        print("Successfully extracted ehr data.")
    except Exception as e:
        print(f"Error extracting ehr data: {e}")