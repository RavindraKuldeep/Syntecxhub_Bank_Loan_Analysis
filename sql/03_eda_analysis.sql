/* ================================================================
   Syntecxhub Bank Loan Analysis
   File: 03_eda_analysis.sql

   Purpose:
   FAST / LIGHTWEIGHT EDA PROFILE

   This version intentionally avoids expensive:
   - GROUP BY on large text columns
   - COUNT(DISTINCT) across every text column
   - AVG/MIN/MAX scans across every numeric column
   - dynamic SQL across all 32 columns
   - duplicate-row hash calculations

   Business-specific EDA will be added after the verified schema
   is confirmed.
================================================================ */

USE Syntecxhub_Bank_Loan_Analysis;
GO


/* ================================================================
   0. VERIFY ACTUAL SCHEMA
   Very fast: reads SQL Server metadata only.
================================================================ */

SELECT
    ORDINAL_POSITION,
    COLUMN_NAME,
    DATA_TYPE,
    CHARACTER_MAXIMUM_LENGTH,
    NUMERIC_PRECISION,
    NUMERIC_SCALE,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME = 'loan_applications'
ORDER BY ORDINAL_POSITION;
GO


/* ================================================================
   1. BASIC DATASET PROFILE
================================================================ */

SELECT
    COUNT_BIG(*) AS TotalRows
FROM dbo.loan_applications;
GO

SELECT
    COUNT(*) AS TotalColumns
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME = 'loan_applications';
GO


/* ================================================================
   2. SAMPLE DATA
   Only 10 rows are read.
================================================================ */

SELECT TOP (10) *
FROM dbo.loan_applications;
GO


/* ================================================================
   3. NULL PROFILE
   Lightweight metadata check only.
   IS_NULLABLE tells whether the column allows NULL.
================================================================ */

SELECT
    ORDINAL_POSITION,
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME = 'loan_applications'
ORDER BY ORDINAL_POSITION;
GO


/* ================================================================
   4. DATA TYPE SUMMARY
   Metadata only — very fast.
================================================================ */

SELECT
    DATA_TYPE,
    COUNT(*) AS ColumnCount
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME = 'loan_applications'
GROUP BY DATA_TYPE
ORDER BY ColumnCount DESC;
GO


/* ================================================================
   5. DATE COLUMN DISCOVERY
   Metadata only — no table scan.
================================================================ */

SELECT
    ORDINAL_POSITION,
    COLUMN_NAME,
    DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME = 'loan_applications'
  AND DATA_TYPE IN
      (
          'date',
          'datetime',
          'datetime2',
          'smalldatetime',
          'datetimeoffset'
      )
ORDER BY ORDINAL_POSITION;
GO


/* ================================================================
   6. NUMERIC COLUMN DISCOVERY
   Metadata only — no table scan.
================================================================ */

SELECT
    ORDINAL_POSITION,
    COLUMN_NAME,
    DATA_TYPE,
    NUMERIC_PRECISION,
    NUMERIC_SCALE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME = 'loan_applications'
  AND DATA_TYPE IN
      (
          'tinyint',
          'smallint',
          'int',
          'bigint',
          'decimal',
          'numeric',
          'float',
          'real',
          'money',
          'smallmoney'
      )
ORDER BY ORDINAL_POSITION;
GO


/* ================================================================
   7. TEXT / CATEGORICAL COLUMN DISCOVERY
   Metadata only — no table scan.
================================================================ */

SELECT
    ORDINAL_POSITION,
    COLUMN_NAME,
    DATA_TYPE,
    CHARACTER_MAXIMUM_LENGTH
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME = 'loan_applications'
  AND DATA_TYPE IN
      (
          'char',
          'varchar',
          'nchar',
          'nvarchar',
          'text',
          'ntext'
      )
ORDER BY ORDINAL_POSITION;
GO


/* ================================================================
   8. TABLE INFORMATION
================================================================ */

SELECT
    TABLE_SCHEMA,
    TABLE_NAME,
    TABLE_TYPE
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME = 'loan_applications';
GO


/* ================================================================
   9. EDA STATUS
================================================================ */

SELECT
    'FAST schema and dataset profiling completed.' AS EDA_Status,
    'Business-specific loan EDA will be added after schema verification.'
        AS NextStep;
GO


/* ================================================================
   10. PLANNED BANK LOAN EDA
================================================================ */

/*
   After verifying the actual 32-column schema, add only relevant
   queries for columns that actually exist:

   - Loan application volume
   - Loan amount analysis
   - Loan status distribution
   - Applicant income analysis
   - Employment analysis
   - Credit-risk indicators
   - Interest-rate analysis
   - Loan purpose analysis
   - Loan-term analysis
   - Default / delinquency analysis
   - Applicant segmentation
   - Time trends
   - Banking KPIs

   No guessed column names will be used.
*/


/* ================================================================
   END OF FILE
================================================================ */
