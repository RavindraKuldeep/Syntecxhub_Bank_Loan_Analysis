import pandas as pd
from pathlib import Path

# ============================================================
# BANK LOAN ANALYSIS - DATA CLEANING
# ============================================================

# Project path
PROJECT_PATH = Path(__file__).resolve().parent.parent

# Input and output paths
RAW_PATH = PROJECT_PATH / "data" / "raw" / "financial_loan.csv"
CLEANED_PATH = PROJECT_PATH / "data" / "cleaned" / "financial_loan_cleaned.csv"

# Create output folder
CLEANED_PATH.parent.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("BANK LOAN DATA CLEANING")
print("=" * 70)

# ============================================================
# 1. LOAD RAW DATA
# ============================================================

df = pd.read_csv(RAW_PATH)

print("\n1. RAW DATA")
print("-" * 70)
print(f"Rows    : {len(df):,}")
print(f"Columns : {len(df.columns)}")

# ============================================================
# 2. REMOVE EXACT DUPLICATES
# ============================================================

duplicate_count = df.duplicated().sum()

print("\n2. DUPLICATE CHECK")
print("-" * 70)
print(f"Duplicate rows found: {duplicate_count:,}")

if duplicate_count > 0:
    df = df.drop_duplicates()
    print(f"Duplicates removed: {duplicate_count:,}")
else:
    print("No duplicate rows found.")

# ============================================================
# 3. STANDARDIZE COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("\n3. COLUMN NAMES STANDARDIZED")
print("-" * 70)
print(list(df.columns))

# ============================================================
# 4. CLEAN TEXT COLUMNS
# ============================================================

text_columns = df.select_dtypes(include=["object", "string"]).columns

for column in text_columns:
    df[column] = df[column].astype("string").str.strip()

print("\n4. TEXT COLUMNS CLEANED")
print("-" * 70)
print(f"Text columns processed: {len(text_columns)}")

# ============================================================
# 5. HANDLE MISSING EMPLOYMENT TITLE
# ============================================================

if "emp_title" in df.columns:

    missing_before = df["emp_title"].isna().sum()

    df["emp_title"] = df["emp_title"].fillna("Not Specified")

    missing_after = df["emp_title"].isna().sum()

    print("\n5. EMPLOYMENT TITLE")
    print("-" * 70)
    print(f"Missing before : {missing_before:,}")
    print(f"Missing after  : {missing_after:,}")

# ============================================================
# 6. CONVERT DATE COLUMNS
# ============================================================

date_columns = [
    "issue_date",
    "last_credit_pull_date",
    "last_payment_date",
    "next_payment_date"
]

print("\n6. DATE CONVERSION")
print("-" * 70)

for column in date_columns:

    if column in df.columns:

        invalid_before = pd.to_datetime(
            df[column],
            errors="coerce"
        ).isna().sum()

        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

        print(
            f"{column}: {invalid_before:,} invalid/missing "
            f"values converted to NaT"
        )

# ============================================================
# 7. CHECK NUMERIC COLUMNS
# ============================================================

numeric_columns = [
    "id",
    "member_id",
    "annual_income",
    "dti",
    "installment",
    "int_rate",
    "loan_amount",
    "total_acc",
    "total_payment"
]

print("\n7. NUMERIC COLUMN VALIDATION")
print("-" * 70)

for column in numeric_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        print(f"{column}: numeric")

# ============================================================
# 8. CREATE GOOD/BAD LOAN CATEGORY
# ============================================================

print("\n8. GOOD/BAD LOAN CLASSIFICATION")
print("-" * 70)

def classify_loan(status):

    if status in ["Fully Paid", "Current"]:
        return "Good Loan"

    elif status == "Charged Off":
        return "Bad Loan"

    else:
        return "Unknown"


df["loan_category"] = df["loan_status"].apply(classify_loan)

print(df["loan_category"].value_counts(dropna=False))

# ============================================================
# 9. CREATE LOAN STATUS FLAG
# ============================================================

df["good_loan_flag"] = (
    df["loan_category"] == "Good Loan"
).astype(int)

df["bad_loan_flag"] = (
    df["loan_category"] == "Bad Loan"
).astype(int)

print("\nLoan flags created:")
print("good_loan_flag")
print("bad_loan_flag")

# ============================================================
# 10. CREATE DATE ANALYSIS COLUMNS
# ============================================================

if "issue_date" in df.columns:

    df["issue_year"] = df["issue_date"].dt.year
    df["issue_month"] = df["issue_date"].dt.month
    df["issue_month_name"] = df["issue_date"].dt.strftime("%B")
    df["issue_year_month"] = df["issue_date"].dt.to_period("M").astype("string")

print("\n10. DATE ANALYSIS COLUMNS CREATED")
print("-" * 70)

# ============================================================
# 11. CREATE FINANCIAL METRICS
# ============================================================

if "loan_amount" in df.columns and "total_payment" in df.columns:

    df["payment_difference"] = (
        df["total_payment"] - df["loan_amount"]
    )

    df["payment_ratio"] = (
        df["total_payment"] / df["loan_amount"]
    ).round(4)

print("\n11. FINANCIAL METRICS CREATED")
print("-" * 70)

print("payment_difference")
print("payment_ratio")

# ============================================================
# 12. REMOVE CONSTANT COLUMNS
# ============================================================

constant_columns = [
    column
    for column in df.columns
    if df[column].nunique(dropna=False) <= 1
]

print("\n12. CONSTANT COLUMNS")
print("-" * 70)

if constant_columns:
    print("Constant columns found:")
    for column in constant_columns:
        print(f"- {column}")

    df = df.drop(columns=constant_columns)

    print("Constant columns removed.")

else:
    print("No constant columns found.")

# ============================================================
# 13. VALIDATE LOAN AMOUNTS
# ============================================================

print("\n13. LOAN AMOUNT VALIDATION")
print("-" * 70)

if "loan_amount" in df.columns:

    negative_loans = (df["loan_amount"] < 0).sum()
    zero_loans = (df["loan_amount"] == 0).sum()

    print(f"Negative loan amounts: {negative_loans:,}")
    print(f"Zero loan amounts    : {zero_loans:,}")

# ============================================================
# 14. VALIDATE TOTAL PAYMENT
# ============================================================

print("\n14. TOTAL PAYMENT VALIDATION")
print("-" * 70)

if "total_payment" in df.columns:

    negative_payment = (df["total_payment"] < 0).sum()

    print(
        f"Negative payment values: "
        f"{negative_payment:,}"
    )

# ============================================================
# 15. FINAL MISSING VALUE CHECK
# ============================================================

print("\n15. FINAL MISSING VALUE CHECK")
print("-" * 70)

missing_final = df.isna().sum()

missing_final = missing_final[
    missing_final > 0
].sort_values(ascending=False)

if len(missing_final) > 0:
    print(missing_final)
else:
    print("No missing values found.")

# ============================================================
# 16. FINAL DATASET SUMMARY
# ============================================================

print("\n16. FINAL DATASET")
print("-" * 70)

print(f"Rows    : {len(df):,}")
print(f"Columns : {len(df.columns)}")

# ============================================================
# 17. SAVE CLEANED DATA
# ============================================================

df.to_csv(
    CLEANED_PATH,
    index=False
)

print("\n17. CLEANED DATA SAVED")
print("-" * 70)
print(CLEANED_PATH)

print("\n" + "=" * 70)
print("DATA CLEANING COMPLETED SUCCESSFULLY")
print("=" * 70)
