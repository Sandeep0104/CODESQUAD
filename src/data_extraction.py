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

def extract_labs(input_path, output_path):
    print(f"Extracting {input_path} to {output_path}...")
    try:
        doc = Document(input_path)
        # Labs is a JSON list format
        json_content = ""
        for p in doc.paragraphs:
             text = p.text.strip()
             if text:
                 json_content += text
        
        parsed_json = json.loads(json_content)
        with open(output_path, 'w') as f:
            json.dump(parsed_json, f, indent=2)
        print("Successfully extracted labs data.")
        
    except Exception as e:
        print(f"Error extracting labs data: {e}")