# Hospital Health Monitoring Pipeline

This repository contains a simple data pipeline and dashboard for hospital patient monitoring. The pipeline ingests raw documents into a Bronze layer, cleans and standardizes data into a Silver layer, detects anomalies and aggregates results into a Gold layer, and generates visualizations and a GUI dashboard.

## Directory Structure
```
project/
│── bronze/                  # Raw extracted data (Task 1)
│── silver/                  # Cleaned & Standardized data (Task 2)
│── gold/                    # Merged data & Anomaly logs (Task 3 & 4)
│── visualizations/          # Generated plots (Task 5)
│── src/                     # Source Code for the 5 Modules
│   │── data_extraction.py   # Module 1: Extracts raw data to Bronze
│   │── silver_layer.py      # Module 2: Cleans Bronze data to Silver
│   │── gold_layer.py        # Module 3: Merges data and detects Anomalies
│   │── visualizations.py    # Module 4: Generates Visualizations
│   │── gui_dashboard.py     # Module: Interactive GUI Dashboard
│── main.py                  # Module 5: Orchestrates the pipeline
│── README.md                # Documentation
```

## How the Pipeline Works

1. **Data Cleaning (Silver Layer)**
   - Vitals JSON lines are loaded and the `patientId` is standardized to `patient_id`.
   - UNIX timestamps are converted to proper `datetime` objects.
   - Lab results JSON list is loaded, standardizing `test` to `lab_test` and `value` to `lab_value`.
   - All critical metric columns (`hr`, `ox`, `sys`, `dia`, `lab_value`) are explicitly converted to numeric types.

2. **Merging / Joining (Gold Layer)**
   - The cleaned vitals dataset is merged with the EHR dataset (`ehr.csv`) using a **Left Join** on `patient_id`. This ensures we keep all reading events and align them with patient demographics (like age and gender).

3. **Anomaly Detection Rules**
   - **Abnormal Heart Rate**: Flagged if `hr > 100` (High HR) or `hr < 60` (Low HR).
   - **Low Oxygen**: Flagged if `ox < 95`.
   - **High Blood Pressure**: Flagged if Systolic (`sys`) > 140 or Diastolic (`dia`) > 90.

4. **Visualizations**
   - `hr_trend.png`: A line chart showing the Heart Rate and Oxygen levels over time for the first patient found in the dataset.
   - `oxygen_distribution.png`: A histogram depicting the distribution density of all patients' oxygen levels.
   - `anomaly_counts.png`: A bar chart tracking the total count/frequency of each detected anomaly type across the facility.

5. **GUI Dashboard**
   - The project includes an interactive graphical dashboard (`src/gui_dashboard.py`) built with `customtkinter`. It allows users to view the generated summary statistics and seamlessly switch between the visual plots.

## Setup & Execution

### Prerequisites
Make sure you have `pandas`, `openpyxl`, `python-docx`, `matplotlib`, `seaborn`, `customtkinter`, and `Pillow` installed:
```bash
pip install pandas openpyxl python-docx matplotlib seaborn customtkinter Pillow
```

### Running the Pipeline
Place the initial 3 files (`ehr.xlsx`, `vitals.docx`, `labs- Ajay kumar.docx`) directly inside the `project/` directory alongside `main.py`.

Run the entire end-to-end pipeline:
```bash
python main.py
```
This will automatically generate the `bronze/`, `silver/`, `gold/`, and `visualizations/` directories with their corresponding outputs.

If you wish to view the interactive GUI dashboard, run that script directly from the `project/` directory:
```bash
python src/gui_dashboard.py
```


## Project Overview
- Bronze: raw ingested files (ehr, vitals, labs)
- Silver: cleaned and standardized CSVs
- Gold: merged results, anomaly logs and summaries
- `src/`: pipeline code, visualization code, and GUI dashboard

## Quickstart (Windows)
1. Create / activate your virtual environment (optional if using the repo `.venv`):

   python -m venv .venv
   .venv\\Scripts\\activate

2. Install dependencies:

   pip install -r requirements.txt

3. Run the pipeline to create the Silver/Gold layers and visualizations:

   .venv\\Scripts\\python.exe main.py

4. Launch the GUI dashboard:

   .venv\\Scripts\\python.exe src/gui_dashboard.py

Notes:
- The pipeline expects input files in the `bronze/` folder: `ehr.csv`, `vitals.jsonl`, `labs.json`.
- Visualizations are saved to the `visualizations/` folder.

## Visualizations (saved files)
- `visualizations/hr_trend_all.png` — combined HR trend (first 10 patients)
- `visualizations/hr_trend_<patient_id>.png` — per-patient HR + Oxygen trend (generated on demand)
- `visualizations/oxygen_distribution.png` — oxygen level histogram with low-threshold marker
- `visualizations/anomaly_counts.png` — bar chart of anomaly counts by type

## File map
- `main.py` — orchestrates pipeline phases
- `src/data_extraction.py` — functions that extract EHR, vitals, labs
- `src/silver_layer.py` — cleaning and standardization logic
- `src/gold_layer.py` — merging and anomaly detection
- `src/visualizations.py` — generates visualizations and per-patient render
- `src/gui_dashboard.py` — the CustomTkinter GUI that displays visuals and summary


## Contributions

Prateek – Handled data extraction, cleaning, standardization, and normalization (Bronze & Silver layers).<br>
Harshit – Supported preprocessing, schema standardization, and numeric validation of datasets.
Mansi – Implemented the Gold layer, patient master table, anomaly detection, and summary generation.
Prakriti – Created visualizations and analytical dashboards for health trends and anomalies.
Sandeep – Managed end-to-end project integration, Git version control, and GUI dashboard development.


## License
This repository does not include a license file. Add one if you plan to share this repository publicly.



