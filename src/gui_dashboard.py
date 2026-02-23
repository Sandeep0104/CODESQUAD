import os
import pandas as pd
import customtkinter as ctk
from PIL import Image

# Set the appearance and color theme
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class HealthDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Setup main window
        self.title("Hospital Health Monitoring Dashboard")
        self.geometry("1000x800")
        
        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Health Dashboard", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_summary = ctk.CTkButton(self.sidebar_frame, text="Summary Data", command=self.show_summary)
        self.btn_summary.grid(row=1, column=0, padx=20, pady=10)
        
        self.btn_hr = ctk.CTkButton(self.sidebar_frame, text="Heart Rate Trend", command=self.show_hr_trend)
        self.btn_hr.grid(row=2, column=0, padx=20, pady=10)

        self.btn_oxygen = ctk.CTkButton(self.sidebar_frame, text="Oxygen Distribution", command=self.show_oxygen_dist)
        self.btn_oxygen.grid(row=3, column=0, padx=20, pady=10)
        
        self.btn_anomalies = ctk.CTkButton(self.sidebar_frame, text="Anomaly Counts", command=self.show_anomaly_counts)
        self.btn_anomalies.grid(row=4, column=0, padx=20, pady=10, sticky="n")

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 20))

        # Main content area
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.main_frame, text="Welcome to the Health Monitoring System", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20)

        # Image label for displaying plots
        self.image_label = ctk.CTkLabel(self.main_frame, text="")
        self.image_label.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        # Load initial view
        self.show_summary()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def load_image(self, path):
        if os.path.exists(path):
            img = Image.open(path)
            # Resize image to fit nicely
            img.thumbnail((750, 600))
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            self.image_label.configure(image=ctk_img, text="")
            # Keep a reference to prevent garbage collection
            self.image_label.image = ctk_img
        else:
            self.image_label.configure(image=None, text=f"Image not found:\n{path}")

    def show_summary(self):
        self.title_label.configure(text="Summary Statistics")
        self.image_label.configure(image=None)
        
        try:
            summary_df = pd.read_csv('gold/anomaly_summary.csv')
            total_anomalies = summary_df['anomaly_count'].sum() if not summary_df.empty else 0
            
            vitals_df = pd.read_csv('silver/clean_vitals.csv')
            total_patients = vitals_df['patient_id'].nunique() if not vitals_df.empty else 0
            
            summary_text = f"Total Unique Patients Tracked: {total_patients}\n\n"
            summary_text += f"Total Anomalies Detected: {total_anomalies}\n\n"
            
            if not summary_df.empty:
                aggregated = summary_df.groupby('anomaly_type')['anomaly_count'].sum().reset_index()
                for index, row in aggregated.iterrows():
                    summary_text += f"• {row['anomaly_type']}: {row['anomaly_count']} occurrences\n"
            else:
                summary_text += "No anomalies currently recorded in the system."
                
            self.image_label.configure(text=summary_text, font=ctk.CTkFont(size=18))
        except Exception as e:
            self.image_label.configure(text=f"Error loading summary data:\n{e}", font=ctk.CTkFont(size=16))

    def show_hr_trend(self):
        self.title_label.configure(text="Heart Rate & Oxygen Trend")
        self.load_image('visualizations/hr_trend.png')

    def show_oxygen_dist(self):
        self.title_label.configure(text="Oxygen Levels Distribution")
        self.load_image('visualizations/oxygen_distribution.png')

    def show_anomaly_counts(self):
        self.title_label.configure(text="Total Anomaly Counts")
        self.load_image('visualizations/anomaly_counts.png')

if __name__ == "__main__":
    app = HealthDashboard()
    app.mainloop()
