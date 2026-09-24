import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# BANK LOAN ANALYSIS - EXPLORATORY DATA ANALYSIS
# ============================================================

PROJECT_PATH = Path(__file__).resolve().parent.parent

INPUT_PATH = (
    PROJECT_PATH
    / "data"
    / "cleaned"
    / "financial_loan_cleaned.csv"
)

CHART_PATH = (
    PROJECT_PATH
    / "reports"
    / "charts"
)

REPORT_PATH = (
    PROJECT_PATH
    / "reports"
    / "final_report"
)

CHART_PATH.mkdir(parents=True, exist_ok=True)
REPORT_PATH.mkdir(parents=True, exist_ok=True)

print("=" * 75)
print("BANK LOAN ANALYSIS - EXPLORATORY DATA ANALYSIS")
print("=" * 75)

# ============================================================
# 1. LOAD CLEANED DATA
# ============================================================

df = pd.read_csv(INPUT_PATH)

print("\n1. DATA LOADED")
print("-" * 75)
print(f"Rows    : {len(df):,}")
print(f"Columns : {len(df.columns)}")

# Convert dates again after CSV loading
date_columns = [
    "issue_date",
    "last_credit_pull_date",
    "last_payment_date",
    "next_payment_date"
]

for column in date_columns:
    if column in df.columns:
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

# ============================================================
# 2. OVERALL KPI ANALYSIS
# ============================================================

total_applications = df["id"].nunique()

total_funded_amount = df["loan_amount"].sum()

total_amount_received = df["total_payment"].sum()

average_loan_amount = df["loan_amount"].mean()

average_interest_rate = df["int_rate"].mean()

average_dti = df["dti"].mean()

total_installment = df["installment"].sum()

print("\n2. OVERALL KPIs")
print("-" * 75)

print(f"Total Loan Applications : {total_applications:,}")
print(f"Total Funded Amount     : ${total_funded_amount:,.2f}")
print(f"Total Amount Received   : ${total_amount_received:,.2f}")
print(f"Average Loan Amount     : ${average_loan_amount:,.2f}")
print(f"Average Interest Rate   : {average_interest_rate:.2%}")
print(f"Average DTI             : {average_dti:.2%}")
print(f"Total Installment       : ${total_installment:,.2f}")

# ============================================================
# 3. GOOD LOAN / BAD LOAN ANALYSIS
# ============================================================

good_loans = df[df["loan_category"] == "Good Loan"]

bad_loans = df[df["loan_category"] == "Bad Loan"]

good_applications = len(good_loans)

bad_applications = len(bad_loans)

good_loan_percentage = (
    good_applications / total_applications
)

bad_loan_percentage = (
    bad_applications / total_applications
)

good_funded_amount = good_loans["loan_amount"].sum()

bad_funded_amount = bad_loans["loan_amount"].sum()

good_amount_received = good_loans["total_payment"].sum()

bad_amount_received = bad_loans["total_payment"].sum()

print("\n3. GOOD LOAN / BAD LOAN ANALYSIS")
print("-" * 75)

print(f"Good Loan Applications       : {good_applications:,}")
print(f"Good Loan %                  : {good_loan_percentage:.2%}")
print(f"Good Loan Funded Amount      : ${good_funded_amount:,.2f}")
print(f"Good Loan Amount Received    : ${good_amount_received:,.2f}")

print()

print(f"Bad Loan Applications        : {bad_applications:,}")
print(f"Bad Loan %                   : {bad_loan_percentage:.2%}")
print(f"Bad Loan Funded Amount       : ${bad_funded_amount:,.2f}")
print(f"Bad Loan Amount Received     : ${bad_amount_received:,.2f}")

# ============================================================
# 4. LOAN STATUS ANALYSIS
# ============================================================

status_analysis = (
    df.groupby("loan_status")
    .agg(
        Applications=("id", "count"),
        Funded_Amount=("loan_amount", "sum"),
        Amount_Received=("total_payment", "sum"),
        Average_Loan=("loan_amount", "mean"),
        Average_Interest_Rate=("int_rate", "mean")
    )
    .reset_index()
)

print("\n4. LOAN STATUS ANALYSIS")
print("-" * 75)
print(status_analysis.to_string(index=False))

# ============================================================
# 5. MONTHLY TREND ANALYSIS
# ============================================================

monthly_analysis = (
    df.dropna(subset=["issue_date"])
    .groupby("issue_year_month")
    .agg(
        Applications=("id", "count"),
        Funded_Amount=("loan_amount", "sum"),
        Amount_Received=("total_payment", "sum")
    )
    .reset_index()
)

print("\n5. MONTHLY LOAN TREND")
print("-" * 75)
print(monthly_analysis.to_string(index=False))

# ============================================================
# 6. STATE / REGION ANALYSIS
# ============================================================

state_analysis = (
    df.groupby("address_state")
    .agg(
        Applications=("id", "count"),
        Funded_Amount=("loan_amount", "sum"),
        Amount_Received=("total_payment", "sum"),
        Average_Loan=("loan_amount", "mean")
    )
    .reset_index()
    .sort_values("Applications", ascending=False)
)

print("\n6. STATE-WISE ANALYSIS - TOP 10")
print("-" * 75)
print(
    state_analysis
    .head(10)
    .to_string(index=False)
)

# ============================================================
# 7. PURPOSE ANALYSIS
# ============================================================

purpose_analysis = (
    df.groupby("purpose")
    .agg(
        Applications=("id", "count"),
        Funded_Amount=("loan_amount", "sum"),
        Amount_Received=("total_payment", "sum"),
        Average_Loan=("loan_amount", "mean")
    )
    .reset_index()
    .sort_values("Applications", ascending=False)
)

print("\n7. LOAN PURPOSE ANALYSIS")
print("-" * 75)
print(purpose_analysis.to_string(index=False))

# ============================================================
# 8. GRADE ANALYSIS
# ============================================================

grade_analysis = (
    df.groupby("grade")
    .agg(
        Applications=("id", "count"),
        Funded_Amount=("loan_amount", "sum"),
        Amount_Received=("total_payment", "sum"),
        Average_Interest_Rate=("int_rate", "mean"),
        Average_DTI=("dti", "mean")
    )
    .reset_index()
    .sort_values("grade")
)

print("\n8. LOAN GRADE ANALYSIS")
print("-" * 75)
print(grade_analysis.to_string(index=False))

# ============================================================
# 9. EMPLOYMENT LENGTH ANALYSIS
# ============================================================

employment_analysis = (
    df.groupby("emp_length")
    .agg(
        Applications=("id", "count"),
        Funded_Amount=("loan_amount", "sum"),
        Amount_Received=("total_payment", "sum"),
        Average_Loan=("loan_amount", "mean")
    )
    .reset_index()
)

print("\n9. EMPLOYMENT LENGTH ANALYSIS")
print("-" * 75)
print(employment_analysis.to_string(index=False))

# ============================================================
# 10. HOME OWNERSHIP ANALYSIS
# ============================================================

home_analysis = (
    df.groupby("home_ownership")
    .agg(
        Applications=("id", "count"),
        Funded_Amount=("loan_amount", "sum"),
        Amount_Received=("total_payment", "sum"),
        Average_Loan=("loan_amount", "mean")
    )
    .reset_index()
    .sort_values("Applications", ascending=False)
)

print("\n10. HOME OWNERSHIP ANALYSIS")
print("-" * 75)
print(home_analysis.to_string(index=False))

# ============================================================
# 11. VERIFICATION STATUS ANALYSIS
# ============================================================

verification_analysis = (
    df.groupby("verification_status")
    .agg(
        Applications=("id", "count"),
        Funded_Amount=("loan_amount", "sum"),
        Amount_Received=("total_payment", "sum")
    )
    .reset_index()
)

print("\n11. VERIFICATION STATUS ANALYSIS")
print("-" * 75)
print(verification_analysis.to_string(index=False))

# ============================================================
# 12. TERM ANALYSIS
# ============================================================

term_analysis = (
    df.groupby("term")
    .agg(
        Applications=("id", "count"),
        Funded_Amount=("loan_amount", "sum"),
        Amount_Received=("total_payment", "sum"),
        Average_Interest_Rate=("int_rate", "mean")
    )
    .reset_index()
)

print("\n12. LOAN TERM ANALYSIS")
print("-" * 75)
print(term_analysis.to_string(index=False))

# ============================================================
# 13. BAD LOAN FACTOR ANALYSIS
# ============================================================

bad_loan_factor_analysis = (
    df.groupby("grade")
    .agg(
        Total_Applications=("id", "count"),
        Bad_Loan_Applications=("bad_loan_flag", "sum"),
        Average_Interest_Rate=("int_rate", "mean"),
        Average_DTI=("dti", "mean"),
        Average_Annual_Income=("annual_income", "mean")
    )
    .reset_index()
)

bad_loan_factor_analysis["Bad_Loan_Rate"] = (
    bad_loan_factor_analysis["Bad_Loan_Applications"]
    / bad_loan_factor_analysis["Total_Applications"]
)

print("\n13. BAD LOAN FACTOR ANALYSIS")
print("-" * 75)

print(
    bad_loan_factor_analysis
    .sort_values("Bad_Loan_Rate", ascending=False)
    .to_string(index=False)
)

# ============================================================
# 14. CREATE CHARTS
# ============================================================

print("\n14. CREATING CHARTS")
print("-" * 75)

# ------------------------------------------------------------
# Chart 1 - Loan Applications by Status
# ------------------------------------------------------------

status_counts = df["loan_status"].value_counts()

plt.figure(figsize=(9, 6))

status_counts.plot(
    kind="bar"
)

plt.title("Loan Applications by Loan Status")
plt.xlabel("Loan Status")
plt.ylabel("Number of Applications")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    CHART_PATH / "01_loan_status.png",
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Chart 2 - Monthly Loan Applications
# ------------------------------------------------------------

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_analysis["issue_year_month"],
    monthly_analysis["Applications"],
    marker="o"
)

plt.title("Monthly Loan Applications Trend")
plt.xlabel("Month")
plt.ylabel("Applications")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    CHART_PATH / "02_monthly_applications.png",
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Chart 3 - State-wise Applications
# ------------------------------------------------------------

top_states = state_analysis.head(10)

plt.figure(figsize=(10, 6))

plt.bar(
    top_states["address_state"],
    top_states["Applications"]
)

plt.title("Top 10 States by Loan Applications")
plt.xlabel("State")
plt.ylabel("Applications")

plt.tight_layout()

plt.savefig(
    CHART_PATH / "03_top_states.png",
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Chart 4 - Loan Purpose
# ------------------------------------------------------------

top_purposes = purpose_analysis.head(10)

plt.figure(figsize=(11, 6))

plt.barh(
    top_purposes["purpose"],
    top_purposes["Applications"]
)

plt.title("Top Loan Purposes by Applications")
plt.xlabel("Applications")
plt.ylabel("Purpose")

plt.tight_layout()

plt.savefig(
    CHART_PATH / "04_loan_purpose.png",
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Chart 5 - Grade vs Bad Loan Rate
# ------------------------------------------------------------

grade_chart = bad_loan_factor_analysis.sort_values(
    "grade"
)

plt.figure(figsize=(9, 6))

plt.plot(
    grade_chart["grade"],
    grade_chart["Bad_Loan_Rate"] * 100,
    marker="o"
)

plt.title("Bad Loan Rate by Loan Grade")
plt.xlabel("Loan Grade")
plt.ylabel("Bad Loan Rate (%)")

plt.tight_layout()

plt.savefig(
    CHART_PATH / "05_bad_loan_rate_by_grade.png",
    dpi=300
)

plt.close()

# ============================================================
# 15. SAVE ANALYSIS TABLES
# ============================================================

monthly_analysis.to_csv(
    REPORT_PATH / "monthly_analysis.csv",
    index=False
)

state_analysis.to_csv(
    REPORT_PATH / "state_analysis.csv",
    index=False
)

purpose_analysis.to_csv(
    REPORT_PATH / "purpose_analysis.csv",
    index=False
)

grade_analysis.to_csv(
    REPORT_PATH / "grade_analysis.csv",
    index=False
)

status_analysis.to_csv(
    REPORT_PATH / "status_analysis.csv",
    index=False
)

bad_loan_factor_analysis.to_csv(
    REPORT_PATH / "bad_loan_factor_analysis.csv",
    index=False
)

# ============================================================
# 16. SAVE KPI REPORT
# ============================================================

kpi_report = pd.DataFrame({
    "KPI": [
        "Total Loan Applications",
        "Total Funded Amount",
        "Total Amount Received",
        "Average Loan Amount",
        "Average Interest Rate",
        "Average DTI",
        "Good Loan Applications",
        "Good Loan Percentage",
        "Good Loan Funded Amount",
        "Good Loan Amount Received",
        "Bad Loan Applications",
        "Bad Loan Percentage",
        "Bad Loan Funded Amount",
        "Bad Loan Amount Received"
    ],
    "Value": [
        total_applications,
        total_funded_amount,
        total_amount_received,
        average_loan_amount,
        average_interest_rate,
        average_dti,
        good_applications,
        good_loan_percentage,
        good_funded_amount,
        good_amount_received,
        bad_applications,
        bad_loan_percentage,
        bad_funded_amount,
        bad_amount_received
    ]
})

kpi_report.to_csv(
    REPORT_PATH / "kpi_summary.csv",
    index=False
)

# ============================================================
# 17. FINAL MESSAGE
# ============================================================

print("\nCharts saved in:")
print(CHART_PATH)

print("\nAnalysis tables saved in:")
print(REPORT_PATH)

print("\n" + "=" * 75)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 75)
