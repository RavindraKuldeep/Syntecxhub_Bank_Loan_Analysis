/* ============================================================
   SYNTECXHUB - BANK LOAN ANALYSIS
   File: 04_business_eda.sql
   Purpose: FAST Business-level Loan EDA
   Database: Syntecxhub_Bank_Loan_Analysis
   Table: dbo.loan_applications
   ============================================================ */

USE Syntecxhub_Bank_Loan_Analysis;
GO


/* ============================================================
   01. OVERALL PORTFOLIO KPIs
   ============================================================ */

SELECT
    COUNT_BIG(*) AS TotalApplications,
    COUNT(DISTINCT id) AS UniqueLoans,
    COUNT(DISTINCT member_id) AS UniqueMembers,

    SUM(CAST(loan_amount AS DECIMAL(38,2)))
        AS TotalLoanAmount,

    AVG(CAST(loan_amount AS DECIMAL(38,2)))
        AS AverageLoanAmount,

    SUM(CAST(total_payment AS DECIMAL(38,2)))
        AS TotalPayment,

    AVG(int_rate) AS AverageInterestRate,
    AVG(dti) AS AverageDTI,
    AVG(annual_income) AS AverageAnnualIncome

FROM dbo.loan_applications;
GO


/* ============================================================
   02. GOOD LOAN VS BAD LOAN
   ============================================================ */

SELECT
    SUM(
        CASE
            WHEN good_loan_flag = 1 THEN 1
            ELSE 0
        END
    ) AS GoodLoanApplications,

    SUM(
        CASE
            WHEN bad_loan_flag = 1 THEN 1
            ELSE 0
        END
    ) AS BadLoanApplications,

    SUM(
        CASE
            WHEN good_loan_flag = 1
            THEN CAST(loan_amount AS DECIMAL(38,2))
            ELSE 0
        END
    ) AS GoodLoanAmount,

    SUM(
        CASE
            WHEN bad_loan_flag = 1
            THEN CAST(loan_amount AS DECIMAL(38,2))
            ELSE 0
        END
    ) AS BadLoanAmount,

    CAST(
        100.0 *
        SUM(CASE WHEN good_loan_flag = 1 THEN 1 ELSE 0 END)
        / NULLIF(COUNT_BIG(*),0)
        AS DECIMAL(10,2)
    ) AS GoodLoanPercentage,

    CAST(
        100.0 *
        SUM(CASE WHEN bad_loan_flag = 1 THEN 1 ELSE 0 END)
        / NULLIF(COUNT_BIG(*),0)
        AS DECIMAL(10,2)
    ) AS BadLoanPercentage

FROM dbo.loan_applications;
GO


/* ============================================================
   03. LOAN STATUS ANALYSIS
   ============================================================ */

SELECT
    loan_status AS LoanStatus,
    COUNT_BIG(*) AS Applications,

    SUM(
        CAST(loan_amount AS DECIMAL(38,2))
    ) AS TotalLoanAmount

FROM dbo.loan_applications

GROUP BY loan_status

ORDER BY Applications DESC;
GO


/* ============================================================
   04. LOAN CATEGORY ANALYSIS
   ============================================================ */

SELECT
    loan_category AS LoanCategory,
    COUNT_BIG(*) AS Applications,

    SUM(
        CAST(loan_amount AS DECIMAL(38,2))
    ) AS TotalLoanAmount,

    AVG(
        CAST(loan_amount AS DECIMAL(38,2))
    ) AS AverageLoanAmount

FROM dbo.loan_applications

GROUP BY loan_category

ORDER BY Applications DESC;
GO


/* ============================================================
   05. LOAN PURPOSE ANALYSIS
   ============================================================ */

SELECT
    purpose AS LoanPurpose,
    COUNT_BIG(*) AS Applications,

    SUM(
        CAST(loan_amount AS DECIMAL(38,2))
    ) AS TotalLoanAmount

FROM dbo.loan_applications

GROUP BY purpose

ORDER BY Applications DESC;
GO


/* ============================================================
   06. GRADE ANALYSIS
   ============================================================ */

SELECT
    grade AS Grade,
    COUNT_BIG(*) AS Applications,

    SUM(
        CAST(loan_amount AS DECIMAL(38,2))
    ) AS TotalLoanAmount,

    AVG(int_rate) AS AverageInterestRate,

    CAST(
        100.0 *
        SUM(CASE WHEN bad_loan_flag = 1 THEN 1 ELSE 0 END)
        / NULLIF(COUNT_BIG(*),0)
        AS DECIMAL(10,2)
    ) AS BadLoanPercentage

FROM dbo.loan_applications

GROUP BY grade

ORDER BY grade;
GO


/* ============================================================
   07. LOAN TERM ANALYSIS
   ============================================================ */

SELECT
    term AS LoanTerm,
    COUNT_BIG(*) AS Applications,

    SUM(
        CAST(loan_amount AS DECIMAL(38,2))
    ) AS TotalLoanAmount,

    AVG(int_rate) AS AverageInterestRate

FROM dbo.loan_applications

GROUP BY term

ORDER BY Applications DESC;
GO


/* ============================================================
   08. YEAR-WISE LOAN TREND
   ============================================================ */

SELECT
    issue_year AS IssueYear,

    COUNT_BIG(*) AS Applications,

    SUM(
        CAST(loan_amount AS DECIMAL(38,2))
    ) AS TotalLoanAmount,

    CAST(
        100.0 *
        SUM(CASE WHEN bad_loan_flag = 1 THEN 1 ELSE 0 END)
        / NULLIF(COUNT_BIG(*),0)
        AS DECIMAL(10,2)
    ) AS BadLoanPercentage

FROM dbo.loan_applications

WHERE issue_year IS NOT NULL

GROUP BY issue_year

ORDER BY issue_year;
GO


/* ============================================================
   09. STATE-WISE LOAN ANALYSIS
   ============================================================ */

SELECT
    address_state AS State,

    COUNT_BIG(*) AS Applications,

    SUM(
        CAST(loan_amount AS DECIMAL(38,2))
    ) AS TotalLoanAmount,

    CAST(
        100.0 *
        SUM(CASE WHEN bad_loan_flag = 1 THEN 1 ELSE 0 END)
        / NULLIF(COUNT_BIG(*),0)
        AS DECIMAL(10,2)
    ) AS BadLoanPercentage

FROM dbo.loan_applications

GROUP BY address_state

ORDER BY Applications DESC;
GO


/* ============================================================
   10. PAYMENT PERFORMANCE
   ============================================================ */

SELECT
    AVG(
        CAST(total_payment AS DECIMAL(38,2))
    ) AS AverageTotalPayment,

    AVG(payment_difference)
        AS AveragePaymentDifference,

    AVG(payment_ratio)
        AS AveragePaymentRatio,

    MIN(payment_difference)
        AS MinimumPaymentDifference,

    MAX(payment_difference)
        AS MaximumPaymentDifference

FROM dbo.loan_applications;
GO


/* ============================================================
   END OF FAST BUSINESS EDA
   ============================================================ */