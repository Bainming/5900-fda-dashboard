import pandas as pd

def merge_classification_and_citation(
    classification_file='./data/raw_csv/inspections_classifications.csv',
    citation_file='./data/raw_csv/inspections_citations.csv',
    output_file="./data/cleaned/inspection_data.csv"
):

    df_class = pd.read_csv(classification_file)

    # Drop unnecessary columns if they exist (excluding 'Classification')
    cols_to_drop = ['Address 2', 'ProductType']
    df_class = df_class.drop(columns=[col for col in cols_to_drop if col in df_class.columns])

    # Keep only unique rows in df_class
    df_class = df_class.drop_duplicates()

    # Read and clean citation data
    df_cit = pd.read_csv(citation_file)
    df_cit = df_cit.drop(columns=[col for col in ['Address line 2', 'ProgramArea'] if col in df_cit.columns])

    # Merge on FEINumber and InspectionID
    df_merged = pd.merge(
        df_class,
        df_cit,
        on=["FEINumber", "InspectionID"], 
        how="left",
        suffixes=("_class", "_cit")
    )

    # Collapse duplicate columns
    same_columns = [
        "City", "State", "ZipCode", "LegalName", "AddressLine1", "AddressLine2",
        "StateCode", "CountryCode", "CountryName", "InspectionEndDate",
        "FiscalYear", "FirmProfile"
    ]
    
    for col in same_columns:
        col_class = col + "_class"
        col_cit = col + "_cit"
        if col_class in df_merged.columns and col_cit in df_merged.columns:
            df_merged[col] = df_merged[col_class].combine_first(df_merged[col_cit])
            df_merged.drop(columns=[col_class, col_cit], inplace=True)

    # Save result
    df_merged.to_csv(output_file, index=False)
    print(f"Merge completed, file saved to: {output_file}")

if __name__ == "__main__":
    merge_classification_and_citation()
