# FDA Data Ingestion and Cleaning

## FDA Data Sources

- [FDA Inspection Classifications](https://datadashboard.fda.gov/ora/api/index.htm) (API)  
- [FDA Inspection Citations](https://datadashboard.fda.gov/ora/api/index.htm) (API)  
- [Compliances (Warning Letters)](https://datadashboard.fda.gov/ora/api/index.htm) (API)  
- [Product Recall](https://www.accessdata.fda.gov/scripts/ires/apidocs/) (API)  
- [483 Forms](https://www.fda.gov/about-fda/office-inspections-and-investigations/oii-foia-electronic-reading-room) (Manual Download)

The API needed for this project can be registered [here](https://www.accessdata.fda.gov/scripts/oul/index.cfm?action=portal.login). For this project, only **Enforcement Reports API** and **FDA Data Dashboard API** are needed. Your may check other options if you are planning to expand on this project.

## Data Ingestion
Data ingestion files are stored under folder **collect**. Multiple python files named **collect_x.py** are stored under **collect** folder, each is responsible for handling a different dataset. The file **collect_all.py** is used to run all ingestion at once. This will create a new folder called **data/**. All data pulled via API will be saved to folder **data/raw_csv**.

For 483 dataset, you will have to download manually from link given above by first filter the **FOIA Record Type** to **483** and export as an excel file.

## Data Cleaning
Data cleaning files are stored under folder **clean**. Multiple python files named **clean_x.py** are stored under **clean** folder, each is responsible for cleaning a different dataset. The file **clean_all.py** is used to run all ingestion at once. All cleaned datasets will be saved to folder **data/cleaned**.

## Steps to Run

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables in .env**
   ```env
   USER=your_user_name
   ENFORCE_REPORT_KEY=your_key
   FDA_DASHBOARD_KEY=your_key
   ```
   
3. **Update Local Database**
   There are two ways to run the data ingetion and cleaning process.

   a) **483 Manual Upload**
      ```bash
      python GUI.py
      ```
   This will open a simple user interface. Click **Run** and choose your manually downloaded 483 dataset.The tool will then ingest the other datasets and perform cleaning on all of them.

   b) b) **Automatic Update (Without Manual Upload)**
      ```bash
      python auto_script.py
      ```
   **Note**: This will update your local database using the most recent datasets *except* for the 483 data. It uses the last manually uploaded 483 dataset without fetching a new one. As a result, your local database **will not contain the latest 483 data** unless you manually update it.
