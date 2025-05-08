import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from dotenv import load_dotenv
import sys
import threading
import shutil
import os
import webbrowser
from collect.collect_all import collect_all as run_ingestion
from clean.clean_all import clean_all as run_clean

# Custom stdout redirector
class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)

    def flush(self):
        pass

# Run ingestion task
def ingest():
    output_box.delete("1.0", tk.END)
    status_label.config(text="Running...")
    sys.stdout = StdoutRedirector(output_box)

    def task():
        try:
            run_ingestion()
            status_label.config(text="Ingestion Completed")
        except Exception as e:
            print(f"Error: {e}")
            status_label.config(text="Error")
        finally:
            sys.stdout = sys.__stdout__

    threading.Thread(target=task).start()

def clean():
    output_box.delete("1.0", tk.END)
    status_label.config(text="Running...")
    sys.stdout = StdoutRedirector(output_box)

    def task():
        try:
            run_clean()
            status_label.config(text="Clean Completed")
        except Exception as e:
            print(f"Error: {e}")
            status_label.config(text="Error")
        finally:
            sys.stdout = sys.__stdout__

    threading.Thread(target=task).start()

# Select file and copy it to the target folder
def upload_and_run_all():
    file_path = filedialog.askopenfilename(title="Select 483 file to import")
    
    if not file_path:
        return  # If no file selected, simply return

    def task():
        sys.stdout = StdoutRedirector(output_box)  # Redirect stdout to output_box

        try:
            # Step 1: Copy 483 file
            target_folder = "./data/raw_483/"
            os.makedirs(target_folder, exist_ok=True)
            shutil.copy(file_path, target_folder)
            copied_file = os.path.join(target_folder, os.path.basename(file_path))
            print(f"Copied to: {copied_file}")

            # Step 2: Ingestion
            status_label.config(text="Running Ingestion...")
            run_ingestion()
            print("\n--- Ingestion Completed ---\n")

            # Step 3: Clean
            status_label.config(text="Running Cleaning...")
            run_clean()
            print("\n--- Cleaning Completed ---\n")

            status_label.config(text="All Tasks Completed")

        except Exception as e:
            print(f"Error: {e}")
            status_label.config(text="Error")
        
        finally:
            sys.stdout = sys.__stdout__  # Always restore stdout

    threading.Thread(target=task).start()


# Function to open URL
def open_url(event):
    webbrowser.open("https://www.fda.gov/about-fda/office-inspections-and-investigations/oii-foia-electronic-reading-room")


load_dotenv()

user = os.getenv('USER')
enforce_report_key = os.getenv('ENFORCE_REPORT_KEY')
fda_dashboard_key = os.getenv('FDA_DASHBOARD_KEY')

# Create GUI
root = tk.Tk()
root.title("Data Ingestion GUI")

status_label = tk.Label(root, text="Waiting for operation")
status_label.pack(pady=10)

button_upload = tk.Button(root, text="Run", command=upload_and_run_all)
button_upload.pack(pady=5)

output_box = ScrolledText(root, height=20, width=80)
output_box.pack(pady=10)

# Add Instructions as a guide
guide_label = tk.Label(root, text="**Instructions for Use:**\n\n"
                                  "1. Upload the 483 Form: Click on the 'Run' and upload 483 dataset.\n\n"
                                  "2. Automatic Ingestion: Upon uploading, the system will automatically trigger the ingestion for other dataset.\n\n"
                                  "3. Data Cleaning: After ingestion, the system will proceed with cleaning the dataset.\n\n"
                                  "4. The status will be updated to confirm the successful execution of all tasks.",
                       justify="left", padx=10)
guide_label.pack(pady=10)

# Add a clickable URL link
url_label = tk.Label(root, text="Click here for more info", fg="blue", cursor="hand2")
url_label.pack(pady=10)
url_label.bind("<Button-1>", open_url)  # Bind left-click to open_url function

root.mainloop()
