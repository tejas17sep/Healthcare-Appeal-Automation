import pandas as pd

# python src/pdf_appeal_generator.py

file_path = "data/Appeals_Master_100_Sample.xlsx"

# Read all sheets
excel_data = pd.ExcelFile(file_path)

print("Sheets available:")
print(excel_data.sheet_names)

# Read each sheet
appeals_df = pd.read_excel(file_path, sheet_name="Appeals")
providers_df = pd.read_excel(file_path, sheet_name="Providers")
payers_df = pd.read_excel(file_path, sheet_name="Payers")
denial_df = pd.read_excel(file_path, sheet_name="Denial_Master")
diagnosis_cpt_df = pd.read_excel(file_path, sheet_name="Diagnosis_CPT")
config_df = pd.read_excel(file_path, sheet_name="Configuration")


# Display information

print("\nAppeals Sheet")
print("----------------")
print("Rows:", len(appeals_df))
print("Columns:")
print(list(appeals_df.columns))


print("\nProviders Sheet Rows:", len(providers_df))
print("Payers Sheet Rows:", len(payers_df))
print("Denial Master Rows:", len(denial_df))
print("Diagnosis CPT Rows:", len(diagnosis_cpt_df))
print("Configuration Rows:", len(config_df))


print("\nFirst Claim:")
print(appeals_df.head(1))