# 🏦 Bank Loan Analysis

> **End-to-End Data Analytics Project | SQL • Python • Power BI**

An end-to-end **Bank Loan Analysis** project built to analyze loan applications, funded amounts, repayment performance, loan quality, borrower-related patterns, and portfolio risk.

The project follows a complete analytics workflow:

**SQL Server → Business EDA → Python EDA → Power BI Dashboard → Business Insights**

---

## 📌 Project Overview

The objective of this project is to transform raw loan application data into meaningful business insights using **SQL, Python, and Power BI**.

The analysis focuses on:

* Loan application volume
* Total funded loan amount
* Total amount received
* Average loan amount
* Interest rate
* DTI
* Good vs Bad loans
* Loan status distribution
* Loan purpose analysis
* Loan grade analysis
* Monthly loan application trends
* State-wise loan applications

The final output is a **single-page QHD Power BI dashboard** designed for clear and interactive portfolio analysis.

---

# 🎯 Business Objectives

The analysis aims to answer questions such as:

1. How many loan applications were received?
2. What is the total amount funded?
3. How much amount has been received through repayments?
4. What is the average loan amount?
5. What is the average interest rate?
6. What is the average DTI?
7. What proportion of loans are classified as Good Loans?
8. What proportion are classified as Bad Loans?
9. Which loan statuses have the highest application volume?
10. How do loan applications change over time?
11. Which loan purposes have the highest application volume?
12. How does loan quality vary across grades?
13. Which states have the highest number of loan applications?

---

# 🛠️ Tools & Technologies

| Tool           | Purpose                                       |
| -------------- | --------------------------------------------- |
| **SQL Server** | Data analysis, aggregation and business EDA   |
| **Python**     | Exploratory Data Analysis and data validation |
| **Pandas**     | Data manipulation and analysis                |
| **Matplotlib** | EDA visualizations                            |
| **Power BI**   | Interactive dashboard and visualization       |
| **DAX**        | KPI and analytical calculations               |
| **GitHub**     | Project version control and portfolio hosting |

---

# 🗂️ Project Workflow

```text
Raw Loan Data
      │
      ▼
SQL Server
      │
      ├── Data Preparation
      ├── Business EDA
      └── KPI Analysis
      │
      ▼
Python EDA
      │
      ├── Data Validation
      ├── Descriptive Analysis
      └── Visualization
      │
      ▼
Power BI
      │
      ├── Data Modeling
      ├── DAX Measures
      ├── Interactive Visuals
      └── QHD Dashboard
      │
      ▼
Business Insights
```

---

# 📊 Key KPIs

The Power BI dashboard contains the following major KPIs:

### Loan Portfolio KPIs

* **Total Loan Applications**
* **Total Funded Amount**
* **Total Amount Received**
* **Average Loan Amount**
* **Average Interest Rate**
* **Average DTI**

### Loan Quality KPIs

* **Good Loan Applications**
* **Bad Loan Applications**
* **Good Loan %**
* **Bad Loan %**

---

# 📈 Power BI Dashboard

The final dashboard is designed as a **single-page QHD dashboard (2560 × 1440)**.

### Dashboard Components

#### 1. Loan Applications by Status

A donut chart showing the distribution of applications across different loan statuses.

#### 2. Monthly Loan Applications Trend

A line chart showing the monthly trend of loan applications over time.

#### 3. Good vs Bad Loan

A donut chart comparing Good Loan and Bad Loan application volumes.

#### 4. Loan Applications by Purpose

A horizontal bar chart showing application volume across different loan purposes.

#### 5. Loan Grade Analysis

A combination chart showing:

* Loan applications by grade
* Bad Loan percentage by grade

#### 6. Top 10 States by Loan Applications

A horizontal bar chart showing the states with the highest loan application volume.

---

# 🎛️ Dashboard Filters

The dashboard includes interactive slicers for:

* **Issue Year**
* **Loan Status**
* **Loan Grade**
* **Loan Purpose**
* **Loan Term**

These filters allow users to dynamically explore different segments of the loan portfolio.

---

# 🧮 Important DAX Measures

### Total Loan Applications

```DAX
Total Loan Applications =
DISTINCTCOUNT(loan_applications[id])
```

### Total Funded Amount

```DAX
Total Funded Amount =
SUM(loan_applications[loan_amount])
```

### Total Amount Received

```DAX
Total Amount Received =
SUM(loan_applications[total_payment])
```

### Average Loan Amount

```DAX
Average Loan Amount =
AVERAGE(loan_applications[loan_amount])
```

### Average Interest Rate

```DAX
Average Interest Rate =
AVERAGE(loan_applications[int_rate])
```

### Average DTI

```DAX
Average DTI =
AVERAGE(loan_applications[dti])
```

### Good Loan Applications

```DAX
Good Loan Applications =
CALCULATE(
    DISTINCTCOUNT(loan_applications[id]),
    loan_applications[good_loan_flag] = TRUE()
)
```

### Bad Loan Applications

```DAX
Bad Loan Applications =
CALCULATE(
    DISTINCTCOUNT(loan_applications[id]),
    loan_applications[bad_loan_flag] = TRUE()
)
```

### Good Loan %

```DAX
Good Loan % =
DIVIDE(
    [Good Loan Applications],
    [Total Loan Applications],
    0
)
```

### Bad Loan %

```DAX
Bad Loan % =
DIVIDE(
    [Bad Loan Applications],
    [Total Loan Applications],
    0
)
```

---

# 🐍 Python EDA

Python was used to perform exploratory data analysis and validate important business metrics.

### Main Python Libraries

```python
import pandas as pd
import matplotlib.pyplot as plt
```

### Analysis Areas

The Python analysis includes:

* Total applications
* Total funded amount
* Total amount received
* Average loan amount
* Average interest rate
* Average DTI
* Good Loan analysis
* Bad Loan analysis
* Loan status analysis
* Loan purpose analysis
* Loan grade analysis
* Time-based analysis
* State-level analysis

---

# 🗄️ SQL Analysis

SQL Server was used for structured business analysis.

The SQL analysis covers:

* Overall portfolio KPIs
* Good Loan / Bad Loan analysis
* Loan status analysis
* Loan category analysis
* Loan purpose analysis
* Loan grade analysis
* Loan term analysis
* Year-wise analysis
* State-wise analysis
* Payment performance metrics

Example:

```sql
SELECT
    loan_status AS LoanStatus,
    COUNT_BIG(*) AS Applications,
    SUM(CAST(loan_amount AS DECIMAL(38,2))) AS TotalLoanAmount
FROM dbo.loan_applications
GROUP BY loan_status
ORDER BY Applications DESC;
```

---

# 💡 Business Insights

The analysis enables identification of:

* Overall loan application volume
* Total capital deployed through loans
* Repayment amount received
* Distribution of loan quality
* High-volume loan purposes
* Loan status concentration
* Differences in loan performance across grades
* Monthly changes in application volume
* Geographic concentration of applications

These insights can support **portfolio monitoring, risk analysis, and business decision-making**.

---

# 📁 Project Structure

```text
Syntecxhub_Bank_Loan_Analysis/
│
├── data/
│   └── README.md
│
├── sql/
│   ├── 01_database_setup.sql
│   ├── 02_data_cleaning.sql
│   └── 04_business_eda.sql
│
├── python/
│   └── 03_eda.py
│
├── powerbi/
│   └── Bank_Loan_Analysis.pbix
│
├── reports/
│   ├── charts/
│   └── final_report/
│
├── screenshots/
│   └── bank_loan_dashboard.png
│
└── README.md
```

---

# 🚀 How to Run the Project

## 1. SQL Server

Create the database:

```sql
CREATE DATABASE Syntecxhub_Bank_Loan_Analysis;
```

Then execute the SQL scripts in the appropriate order.

The main analysis table is:

```text
dbo.loan_applications
```

---

## 2. Python EDA

Install the required libraries:

```bash
pip install pandas matplotlib
```

Run:

```bash
python python/03_eda.py
```

The generated analysis outputs are stored under the reports directory.

---

## 3. Power BI

Open:

```text
powerbi/Bank_Loan_Analysis.pbix
```

Connect the report to the SQL Server database and refresh the data if required.

---

# 📊 Dashboard Design

The dashboard uses a clean financial analytics design with:

* QHD resolution
* Single-page layout
* KPI cards
* Donut charts
* Line chart
* Horizontal bar charts
* Combination chart
* Interactive slicers
* Consistent Good/Bad loan color coding
* Minimal and professional visual styling

---

# 🔍 Analytical Focus

This project demonstrates practical experience with:

### SQL

* Aggregations
* `GROUP BY`
* `CASE`
* Conditional calculations
* Business KPIs
* Portfolio segmentation

### Python

* Data loading
* Data cleaning
* Date conversion
* Filtering
* Aggregation
* Exploratory analysis
* Visualization

### Power BI

* Data modeling
* DAX measures
* KPI cards
* Interactive slicers
* Drill/filter interactions
* Time-series analysis
* Category analysis
* Portfolio risk visualization

---

# 🎓 Skills Demonstrated

* SQL
* Python
* Pandas
* Matplotlib
* Power BI
* DAX
* Exploratory Data Analysis
* Business Intelligence
* Data Visualization
* KPI Development
* Business Analytics
* Data Storytelling

---

# 📌 Project Type

**Data Analytics / Business Intelligence**

Built as part of a **Syntecxhub Data Analysis Internship Project**.

---

# 👨‍💻 Author

**Ravindra Deo Kuldeep (ARKAY)**

Aspiring Data Analyst | SQL | Power BI | Excel | Python | Tableau

### Profiles

* LinkedIn: https://www.linkedin.com/in/arkay003/
* GitHub: https://github.com/RavindraKuldeep/
* Tableau Public: https://public.tableau.com/app/profile/ravindra.kuldeep

---

# ⭐ Conclusion

This project demonstrates an end-to-end approach to transforming loan application data into actionable analytical insights using **SQL Server, Python, and Power BI**.

The final Power BI dashboard provides an interactive view of **loan volume, funding, repayment, loan quality, purpose, grade, trend, and geographic distribution** in a single-page analytical interface.

---

## 📌 Disclaimer

This project is created for **educational, portfolio, and internship purposes**. The analysis should not be interpreted as financial advice or as a real-world lending decision model.
