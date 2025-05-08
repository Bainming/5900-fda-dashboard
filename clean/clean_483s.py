import os
import glob
import pandas as pd

def get_latest_xlsx_file(folder_path):
    xlsx_files = glob.glob(os.path.join(folder_path, '*.xlsx'))
    if not xlsx_files:
        return None

    latest_file = max(xlsx_files, key=os.path.getmtime)
    return latest_file

def clean_and_save_file(file_path, destination_folder):
    df = pd.read_excel(file_path)

    cleaned_file_name = "483_data.csv"
    cleaned_file_path = os.path.join(destination_folder, cleaned_file_name)

    # Save the new cleaned data to the same file
    df.to_csv(cleaned_file_path, index=False)
    print(f'File cleaned and saved to: {cleaned_file_path}')

def monitor_and_clean_folder():

    source_folder = './data/raw_483'
    destination_folder = './data/cleaned'

    os.makedirs(destination_folder, exist_ok=True)

    xlsx_files = glob.glob(os.path.join(source_folder, '*.xlsx'))
    
    latest_file = get_latest_xlsx_file(source_folder)

    print(latest_file)

    if latest_file:
        print(f'Latest file to process: {latest_file}')
        clean_and_save_file(latest_file, destination_folder)

    if len(xlsx_files) >= 10:
        xlsx_files.sort(key=os.path.getmtime)
        oldest_file = xlsx_files[0]
        os.remove(oldest_file)
        print(f'Removed oldest file: {oldest_file}')

if __name__ == "__main__":
    monitor_and_clean_folder()