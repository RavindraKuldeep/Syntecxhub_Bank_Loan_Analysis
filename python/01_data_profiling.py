import pandas as pd
from pathlib import Path

# ==========================================
# BANK LOAN DATA - DATA PROFILING
# ==========================================

# Project paths
PROJECT_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_PATH / "data" / "raw" / "financial_loan.csv"
REPORT_PATH = PROJECT_PATH / "reports" / "final_report"

# Create report folder if it doesn't exist
REPORT_PATH.mkdir(parents=True, exist_ok=True)

# ==========================================
# 1. LOAD DATA
# ==========================================

df = pd.read_csv(DATA_PATH)

print("=" * 70)
print("BANK LOAN DATA PROFILING")
print("=" * 70)

# ==========================================
# 2. BASIC INFORMATION
# ==========================================

print("\n1. DATASET SHAPE")
print("-" * 70)
print(f"Rows    : {df.shape[0]:,}")
print(f"Columns : {df.shape[1]}")

print("\n2. COLUMN NAMES")
print("-" * 70)

for i, column in enumerate(df.columns, start=1):
    print(f"{i:02d}. {column}")

# ==========================================
# 3. DATA TYPES
# ==========================================

print("\n3. DATA TYPES")
print("-" * 70)
print(df.dtypes)

# ==========================================
# 4. MISSING VALUES
# ==========================================

print("\n4. MISSING VALUES")
print("-" * 70)

missing = pd.DataFrame({
    "Column": df.columns,
    "Missing_Count": df.isnull().sum().values,
    "Missing_Percentage": (
        df.isnull().sum().values / len(df) * 100
    ).round(2)
})

print(
    missing[missing["Missing_Count"] > 0]
    .sort_values("Missing_Count", ascending=False)
)

# ==========================================
# 5. DUPLICATES
# ==========================================

print("\n5. DUPLICATE RECORDS")
print("-" * 70)

duplicates = df.duplicated().sum()

print(f"Duplicate rows: {duplicates:,}")

# ==========================================
# 6. UNIQUE VALUES
# ==========================================

print("\n6. UNIQUE VALUES")
print("-" * 70)

unique_values = pd.DataFrame({
    "Column": df.columns,
    "Unique_Count": [
        df[column].nunique(dropna=True)
        for column in df.columns
    ]
})

print(unique_values.to_string(index=False))

# ==========================================
# 7. NUMERICAL SUMMARY
# ==========================================

print("\n7. NUMERICAL SUMMARY")
print("-" * 70)

print(df.describe().T)

# ==========================================
# 8. CATEGORICAL SUMMARY
# ==========================================

print("\n8. IMPORTANT CATEGORICAL COLUMNS")
print("-" * 70)

categorical_columns = [
    "loan_status",
    "grade",
    "sub_grade",
    "home_ownership",
    "verification_status",
    "purpose",
    "term",
    "address_state"
]

for column in categorical_columns:

    if column in df.columns:

        print(f"\n--- {column} ---")
        print(df[column].value_counts(dropna=False).head(20))

# ==========================================
# 9. DATE CHECK
# ==========================================

print("\n9. DATE COLUMN CHECK")
print("-" * 70)

if "issue_date" in df.columns:

    date_column = pd.to_datetime(
        df["issue_date"],
        errors="coerce"
    )

    print(f"Minimum date: {date_column.min()}")
    print(f"Maximum date: {date_column.max()}")
    print(
        f"Invalid dates: {date_column.isna().sum():,}"
    )

# ==========================================
# 10. LOAN STATUS CHECK
# ==========================================

print("\n10. LOAN STATUS")
print("-" * 70)

if "loan_status" in df.columns:
    print(df["loan_status"].value_counts())

# ==========================================
# 11. KEY FINANCIAL COLUMNS
# ==========================================

print("\n11. KEY FINANCIAL COLUMNS")
print("-" * 70)

financial_columns = [
    "loan_amount",
    "total_payment",
    "annual_income",
    "int_rate",
    "dti"
]

for column in financial_columns:

    if column in df.columns:

        print(f"\n{column}")

        print(f"Minimum : {df[column].min()}")
        print(f"Maximum : {df[column].max()}")
        print(f"Average : {df[column].mean():,.2f}")
        print(f"Median  : {df[column].median():,.2f}")

# ==========================================
# 12. SAVE PROFILING REPORT
# ==========================================

report_file = REPORT_PATH / "data_profiling_report.txt"

with open(report_file, "w", encoding="utf-8") as file:

    file.write("BANK LOAN DATA PROFILING REPORT\n")
    file.write("=" * 70 + "\n\n")

    file.write(
        f"Rows: {df.shape[0]:,}\n"
        f"Columns: {df.shape[1]}\n\n"
    )

    file.write("COLUMN NAMES\n")
    file.write("-" * 70 + "\n")

    for column in df.columns:
        file.write(f"{column}\n")

    file.write("\nDATA TYPES\n")
    file.write("-" * 70 + "\n")
    file.write(df.dtypes.to_string())

    file.write("\n\nMISSING VALUES\n")
    file.write("-" * 70 + "\n")
    file.write(missing.to_string(index=False))

    file.write("\n\nDUPLICATE ROWS\n")
    file.write("-" * 70 + "\n")
    file.write(str(duplicates))

    file.write("\n\nNUMERICAL SUMMARY\n")
    file.write("-" * 70 + "\n")
    file.write(df.describe().T.to_string())

print("\n" + "=" * 70)
print("DATA PROFILING COMPLETED SUCCESSFULLY")
print("=" * 70)

print(f"\nReport saved at:")
print(report_file)
