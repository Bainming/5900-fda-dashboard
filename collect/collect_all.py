from . import collect_classifications
from . import collect_citations
from . import collect_recall
from . import collect_compliances
import os
import shutil

def delete_all_files(directory):
    # Check if the directory exists
    if os.path.exists(directory) and os.path.isdir(directory):
        # Loop through all files in the directory
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            # Check if it's a file (not a subdirectory)
            if os.path.isfile(file_path):
                os.remove(file_path)  # Delete the file
                print(f"Deleted: {file_path}")
    else:
        print("The specified directory does not exist.")

def move_files_from_temp(temp_dir, target_dir):
    # Check if target directory exists, if not, create it
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # Loop through the files in the temporary directory
    for filename in os.listdir(temp_dir):
        temp_file_path = os.path.join(temp_dir, filename)
        target_file_path = os.path.join(target_dir, filename)
        
        # Move the file from the temporary directory to the target directory
        if os.path.isfile(temp_file_path):
            shutil.move(temp_file_path, target_file_path)
            print(f"Moved: {temp_file_path} to {target_file_path}")
        else:
            print(f"Skipping directory: {temp_file_path}")

def collect_all():

    inspec_class_url = "https://api-datadashboard.fda.gov/v1/inspections_classifications" 
    inspec_citation_url = "https://api-datadashboard.fda.gov/v1/inspections_citations"
    compliance_url = "https://api-datadashboard.fda.gov/v1/compliance_actions"

    raw_dir = "./data/raw_csv/"
    temp_dir = "./data/temp_csv/"

    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)

    delete_all_files(temp_dir)

    collect_compliances.request_compliances(compliance_url, temp_dir)

    collect_classifications.request_classifications(inspec_class_url, temp_dir)

    collect_citations.request_citations(inspec_citation_url, temp_dir)

    collect_recall.request_recall(temp_dir)

    move_files_from_temp(temp_dir, raw_dir)

    print("Ingestion completed. \nPlease drop 483 data into the following folder manually: \n./data/raw_483")