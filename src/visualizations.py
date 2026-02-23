import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_visualizations():
    print("Creating visualizations...")
    os.makedirs('visualizations', exist_ok=True)
    try:
        # Load necessary data
        try:
             vitals_df = pd.read_csv('silver/clean_vitals.csv')
             vitals_df['timestamp'] = pd.to_datetime(vitals_df['timestamp'])
        except Exception as e:
             print(f"Error loading vitals: {e}")
             return

        try:
             summary_df = pd.read_csv('gold/anomaly_summary.csv')
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
            plt.savefig('visualizations/hr_trend.png')
            plt.close()
            print("Successfully saved hr_trend.png")
        
        # Plot 2: Oxygen distribution (Histogram) across all patients
        if not vitals_df.empty:
             plt.figure(figsize=(8, 6))
             sns.histplot(vitals_df['ox'], bins=20, kde=True, color='skyblue')
             plt.title('Distribution of Oxygen Levels Across All Patients')
             plt.xlabel('Oxygen Level (%)')
             plt.ylabel('Frequency')
             plt.tight_layout()
             plt.savefig('visualizations/oxygen_distribution.png')
             plt.close()
             print("Successfully saved oxygen_distribution.png")
         # Plot 3: Anomaly Counts (Bar Chart)
        if not summary_df.empty:
             plt.figure(figsize=(10, 6))
             # Aggregate total counts by anomaly type
             total_anomalies = summary_df.groupby('anomaly_type')['anomaly_count'].sum().reset_index()
             
             sns.barplot(x='anomaly_type', y='anomaly_count', data=total_anomalies, palette='viridis')
             plt.title('Total Anomaly Counts by Type')
             plt.xlabel('Anomaly Type')
             plt.ylabel('Number of Occurrences')
             plt.tight_layout()
             plt.savefig('project/visualizations/anomaly_counts.png')
             plt.close()
             print("Successfully saved anomaly_counts.png")
        else:
             print("No anomalies to plot.")

    except Exception as e:
        print(f"Error creating visualizations: {e}")

if __name__ == "__main__":
    create_visualizations()
