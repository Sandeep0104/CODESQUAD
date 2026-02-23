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

def create_gold_layer():
    print("Creating Gold Layer...")
    try:
        # Load Silver Data
        vitals_df = pd.read_csv('project/silver/clean_vitals.csv')
        labs_df = pd.read_csv('project/silver/clean_labs.csv')
        ehr_df = pd.read_csv('project/bronze/ehr.csv') # EHR is passed through Bronze
        
        # Merge Vitals with EHR
        # We can do an outer join or left join depending on requirements. 
        # A left join on vitals ensures we keep all reading events.
        merged_vitals = pd.merge(vitals_df, ehr_df, on='patient_id', how='left')
        
        # Apply anomaly detection on vitals
        anomalies_df = process_anomalies(vitals_df)
        
        # Aggregate Anomaly counts per patient
        if not anomalies_df.empty:
            summary_df = anomalies_df.groupby(['patient_id', 'anomaly_type']).size().reset_index(name='anomaly_count')
        else:
            summary_df = pd.DataFrame(columns=['patient_id', 'anomaly_type', 'anomaly_count'])
        
        os.makedirs('project/gold', exist_ok=True)
        
        # Save merged and anomaly results
        merged_vitals.to_csv('project/gold/merged_vitals.csv', index=False)
        anomalies_df.to_csv('project/gold/anomalies_log.csv', index=False)
        summary_df.to_csv('project/gold/anomaly_summary.csv', index=False)
        
        print("Successfully created Gold Layer.")
    except Exception as e:
        print(f"Error creating Gold Layer: {e}")

if __name__ == "__main__":
    create_gold_layer()
   