import os
from src import data_extraction
from src import silver_layer
from src import gold_layer
from src import visualizations

def run_pipeline():
    print("====================================")
    print("Starting Hospital Health Monitoring Pipeline")
    print("====================================\n")
    
    # Ensure project structure exists (use top-level folders)
    os.makedirs('bronze', exist_ok=True)
    os.makedirs('silver', exist_ok=True)
    os.makedirs('gold', exist_ok=True)
    os.makedirs('visualizations', exist_ok=True)
    
    # Phase 1: Data Extraction (Bronze Layer) - skip if files already present
    print("--- Phase 1: Data Extraction ---")
    if not os.path.exists('bronze/ehr.csv'):
        data_extraction.extract_ehr('ehr.xlsx', 'bronze/ehr.csv')
    else:
        print('Found bronze/ehr.csv, skipping EHR extraction.')

    if not os.path.exists('bronze/vitals.jsonl'):
        data_extraction.extract_vitals('vitals.docx', 'bronze/vitals.jsonl')
    else:
        print('Found bronze/vitals.jsonl, skipping vitals extraction.')

    if not os.path.exists('bronze/labs.json'):
        data_extraction.extract_labs('labs- Ajay kumar.docx', 'bronze/labs.json')
    else:
        print('Found bronze/labs.json, skipping labs extraction.')

    print("Bronze layer ready.\n")
    
    # Phase 2: Cleaning & Standardization (Silver Layer)
    print("--- Phase 2: Silver Layer ---")
    silver_layer.clean_vitals('bronze/vitals.jsonl', 'silver/clean_vitals.csv')
    silver_layer.clean_labs('bronze/labs.json', 'silver/clean_labs.csv')
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
