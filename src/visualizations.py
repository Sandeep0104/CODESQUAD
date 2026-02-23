import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_visualizations():
    print("Creating visualizations...")
    os.makedirs('project/visualizations', exist_ok=True)
    try:
        # Load necessary data
        try:
             vitals_df = pd.read_csv('project/silver/clean_vitals.csv')
             vitals_df['timestamp'] = pd.to_datetime(vitals_df['timestamp'])
        except Exception as e:
             print(f"Error loading vitals: {e}")
             return

        try:
             summary_df = pd.read_csv('project/gold/anomaly_summary.csv')
        except Exception as e:
             print(f"Error loading anomaly summary: {e}")
             summary_df = pd.DataFrame()
             
             
        # Plot 1: HR and Oxygen trends over time (for a specific patient, e.g., patient 2001)
        # Or, we can plot the average over time
        plt.figure(figsize=(12, 6))
        
        # Pick the first patient for the trend line
        if not vitals_df.empty:
            patient_id = vitals_df['patient_id'].iloc[0]
            patient_data = vitals_df[vitals_df['patient_id'] == patient_id].sort_values('timestamp')
            
            plt.plot(patient_data['timestamp'], patient_data['hr'], label='Heart Rate (bpm)', color='red', marker='o')
            plt.plot(patient_data['timestamp'], patient_data['ox'], label='Oxygen (%)', color='blue', marker='x')
            plt.title(f'Vitals Trend for Patient {patient_id}')
            plt.xlabel('Timestamp')
            plt.ylabel('Value')
            plt.legend()
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig('project/visualizations/hr_trend.png')
            plt.close()
            print("Successfully saved hr_trend.png")
        
        

    except Exception as e:
        print(f"Error creating visualizations: {e}")

if __name__ == "__main__":
    create_visualizations()
