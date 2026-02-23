import os
from src import data_extraction
from src import silver_layer
from src import gold_layer
from src import visualizations

def run_pipeline():
    print("====================================")
    print("Starting Hospital Health Monitoring Pipeline")
    print("====================================\n")
    
    # Ensure project structure exists
    os.makedirs('project/bronze', exist_ok=True)
    os.makedirs('project/silver', exist_ok=True)
    os.makedirs('project/gold', exist_ok=True)
    os.makedirs('project/visualizations', exist_ok=True)
    
    # Phase 1: Data Extraction (Bronze Layer)
    print("--- Phase 1: Data Extraction ---")
    data_extraction.extract_ehr('ehr.xlsx', 'project/bronze/ehr.csv')
    data_extraction.extract_vitals('vitals.docx', 'project/bronze/vitals.jsonl')
    data_extraction.extract_labs('labs- Ajay kumar.docx', 'project/bronze/labs.json')
    print("Bronze layer created successfully.\n")
    
    # Phase 2: Cleaning & Standardization (Silver Layer)
    print("--- Phase 2: Silver Layer ---")
    silver_layer.clean_vitals('project/bronze/vitals.jsonl', 'project/silver/clean_vitals.csv')
    silver_layer.clean_labs('project/bronze/labs.json', 'project/silver/clean_labs.csv')
    # EHR needs no cleaning, we just act as if it is in Silver already for the next step 
    print("Silver layer created successfully.\n")
    
    # Phase 3: Merging & Anomaly Detection (Gold Layer)
    print("--- Phase 3: Gold Layer ---")
    gold_layer.create_gold_layer()
    print("Gold layer created successfully.\n")
    
    # Phase 4: Data Visualizations
    print("--- Phase 4: Visualizations ---")
    visualizations.create_visualizations()
    print("Visualizations generated successfully.\n")
    
    print("====================================")
    print("Pipeline Execution Complete!")
    print("====================================")

if __name__ == "__main__":
    run_pipeline()
