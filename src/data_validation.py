import pandas as pd


file_path = "data/Appeals_Master_100_Sample.xlsx"

# Load sheets

appeals = pd.read_excel(
    file_path,
    sheet_name="Appeals"
)

payers = pd.read_excel(
    file_path,
    sheet_name="Payers"
)

denial_master = pd.read_excel(
    file_path,
    sheet_name="Denial_Master"
)


errors = []


# -----------------------------
# 1. Mandatory Field Check
# -----------------------------

required_columns = [
    "Claim_ID",
    "Insurance",
    "CPT_Code",
    "ICD10",
    "Denial_Code",
    "Appeal_Type"
]


for column in required_columns:

    missing = appeals[
        appeals[column].isna()
    ]

    for index,row in missing.iterrows():

        errors.append(
            f"Claim {row['Claim_ID']}: Missing {column}"
        )


# -----------------------------
# 2. Duplicate Claim Check
# -----------------------------

duplicate_claims = appeals[
    appeals.duplicated(
        "Claim_ID",
        keep=False
    )
]


for _,row in duplicate_claims.iterrows():

    errors.append(
        f"Duplicate Claim ID: {row['Claim_ID']}"
    )


# -----------------------------
# 3. Insurance Validation
# -----------------------------

valid_insurance = (
    payers["Insurance"]
    .dropna()
    .tolist()
)


for _,row in appeals.iterrows():

    if row["Insurance"] not in valid_insurance:

        errors.append(
            f"Claim {row['Claim_ID']}: Invalid Insurance {row['Insurance']}"
        )


# -----------------------------
# 4. Denial Code Validation
# -----------------------------

valid_denials = (
    denial_master["Denial_Code"]
    .dropna()
    .tolist()
)


for _,row in appeals.iterrows():

    if row["Denial_Code"] not in valid_denials:

        errors.append(
            f"Claim {row['Claim_ID']}: Invalid Denial Code {row['Denial_Code']}"
        )


# -----------------------------
# Final Report
# -----------------------------

print("\n========== Validation Report ==========")


if len(errors)==0:

    print("All Claims Passed Validation ✅")

else:

    print(f"Total Errors Found: {len(errors)}\n")

    for error in errors:
        print(error)