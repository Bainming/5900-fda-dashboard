import pandas as pd

def merge_firms():
    data_483 = pd.read_csv("./data/cleaned/483_data.csv", low_memory=False)
    data_compliance = pd.read_csv("./data/cleaned/compliance_data.csv", low_memory=False)
    data_inspection = pd.read_csv("./data/cleaned/inspection_data.csv", low_memory=False)
    data_recall = pd.read_csv("./data/cleaned/recall_data.csv", low_memory=False)

    firm_483 = data_483[["FEI Number", "Legal Name"]].rename(
        columns={"FEI Number": "FEINumber", "Legal Name": "LegalName"}
    ).copy()
    firm_483["FEINumber"] = firm_483["FEINumber"].astype(str)

    firm_compliance = data_compliance[["FEINumber", "LegalName"]].copy()
    firm_compliance["FEINumber"] = firm_compliance["FEINumber"].astype(str)

    firm_inspection = data_inspection[["FEINumber", "LegalName"]].copy()
    firm_inspection["FEINumber"] = firm_inspection["FEINumber"].astype(str)

    firm_recall = data_recall[["FIRMFEINUM", "FIRMLEGALNAM"]].rename(
        columns={"FIRMFEINUM": "FEINumber", "FIRMLEGALNAM": "LegalName"}
    ).copy()
    firm_recall["FEINumber"] = firm_recall["FEINumber"].astype(str)

    merged_firm_data = pd.concat([firm_483, firm_compliance, firm_inspection, firm_recall], ignore_index=True)
    merged_firm_data = merged_firm_data.drop_duplicates()

    merged_firm_data.to_csv("./data/cleaned/merged_firm_data.csv", index=False)

if __name__ == "__main__":
    merge_firms()
