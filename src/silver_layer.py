import os
import pandas as pd
import json

def clean_ehr(input_path, output_path):
    pass

def clean_vitals(input_path, output_path):
    print("Cleaning vitals file")
    try:
        # Read JSON lines
        data = []
        with open(input_path, 'r') as f:
            for line in f:
                data.append(json.loads(line.strip()))
                
        df = pd.DataFrame(data)
        
        # Standardize columns
        df.rename(columns={'patientId': 'patient_id'}, inplace=True)
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        
        # Ensure numeric fields
        numeric_cols = ['hr', 'ox', 'sys', 'dia']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
        df.to_csv(output_path, index=False)
        print(f"Saved cleaned vitals to {output_path}")
        
    except Exception as e:
        print(f"Error cleaning vitals: {e}")

def clean_labs(input_path, output_path):
    print("Cleaning labs...")
    try:
        with open(input_path, 'r') as f:
            data = json.load(f)
            
        df = pd.DataFrame(data)
        
        # Standardize columns (patient_id, timestamp, lab_test, lab_value)
        df.rename(columns={'patientId': 'patient_id', 'test': 'lab_test', 'value': 'lab_value'}, inplace=True)
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Ensure numeric fields
        df['lab_value'] = pd.to_numeric(df['lab_value'], errors='coerce')
        
        df.to_csv(output_path, index=False)
        print(f"Saved cleaned labs to {output_path}")

    except Exception as e:
        print(f"Error cleaning labs: {e}")
        

if __name__ == "__main__":
    os.makedirs('project/silver', exist_ok=True)
    clean_vitals('project/bronze/vitals.jsonl', 'project/silver/clean_vitals.csv')
    clean_labs('project/bronze/labs.json', 'project/silver/clean_labs.csv')
