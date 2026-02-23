import os
import pandas as pd

def process_anomalies(vitals_df):
    """Detects anomalies based on business rules."""
    print("Detecting anomalies...")
    # Abnormal Heart Rate: hr > 100 or hr < 60
    # Low Oxygen: ox < 95
    # High Blood Pressure: sys > 140 or dia > 90
    
    anomalies = []
    
    for index, row in vitals_df.iterrows():
        patient_id = row['patient_id']
        timestamp = row['timestamp']
        
        if row['hr'] > 100:
             anomalies.append({'patient_id': patient_id, 'timestamp': timestamp, 'anomaly_type': 'High HR', 'value': row['hr']})
        elif row['hr'] < 60:
             anomalies.append({'patient_id': patient_id, 'timestamp': timestamp, 'anomaly_type': 'Low HR', 'value': row['hr']})
             
        if row['ox'] < 95:
             anomalies.append({'patient_id': patient_id, 'timestamp': timestamp, 'anomaly_type': 'Low Oxygen', 'value': row['ox']})
             
        if row['sys'] > 140 or row['dia'] > 90:
             anomalies.append({'patient_id': patient_id, 'timestamp': timestamp, 'anomaly_type': 'High BP', 'value': f"{row['sys']}/{row['dia']}"})
             
    return pd.DataFrame(anomalies)