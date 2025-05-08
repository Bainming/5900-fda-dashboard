import pandas as pd

def format_date(date_str):
    """Convert date string to MMDDYYYY format"""
    try:
        date_obj = pd.to_datetime(date_str)
        return date_obj.strftime('%m%d%Y')
    except:
        return None

def generate_warning_letter_link(row):
    """Generate warning letter link based on the specified format"""
    if row['ActionType'] != 'Warning Letter':
        return None
    
    firm_name = str(row['LegalName']).lower()
    firm_name = ''.join(c for c in firm_name if c.isalnum() or c.isspace() or c == '&')
    firm_name = firm_name.replace(' ', '-').replace('&', '')
    
    case_id = str(row['CaseInjunctionID'])
    action_date = format_date(row['ActionTakenDate'])
    
    if not action_date:
        return None
    
    link = f"https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/warning-letters/{firm_name}-{case_id}-{action_date}"
    return link

def preprocess_compliance_data():
    input_file = 'data/raw_csv/compliance_actions.csv'
    output_file = 'data/cleaned/compliance_data.csv'
    
    print("Reading compliance actions data...")
    df = pd.read_csv(input_file)
    
    print("Handling missing values...")
    df = df.fillna('unavailable')
    
    print("Dropping unnecessary columns...")
    columns_to_drop = ['ProductType', 'Center']
    df = df.drop(columns=columns_to_drop, errors='ignore')
    
    print("Generating warning letter links...")
    df['WarningLetterLink'] = df.apply(generate_warning_letter_link, axis=1)
    
    print("\nExample links generated:")
    for idx, row in df[df['WarningLetterLink'].notna()].head(3).iterrows():
        print(f"\nRow {idx}:")
        print(f"LegalName: {row['LegalName']}")
        print(f"CaseInjunctionID: {row['CaseInjunctionID']}")
        print(f"ActionTakenDate: {row['ActionTakenDate']}")
        print(f"Generated Link: {row['WarningLetterLink']}")
    
    print("\nSaving processed data...")
    df.to_csv(output_file, index=False)
    print(f"Processed data saved to: {output_file}")
    
    print("\nProcessing Summary:")
    print(f"Total rows processed: {len(df)}")
    print(f"Warning letter links generated: {len(df[df['WarningLetterLink'].notna()])}")

if __name__ == "__main__":
    preprocess_compliance_data()
