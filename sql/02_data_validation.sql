/* Syntecxhub Bank Loan Analysis
   File: 02_data_validation.sql
   Purpose: Validate the imported loan_applications table.

   IMPORTANT:
   This version deliberately uses metadata-driven checks first because the exact
   32-column source schema must be verified before writing column-specific EDA.
*/

USE Syntecxhub_Bank_Loan_Analysis;
GO

/* 1. Confirm database */
SELECT DB_NAME() AS CurrentDatabase;
GO

/* 2. Confirm table exists */
SELECT
    TABLE_SCHEMA,
    TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME = 'loan_applications';
GO

/* 3. Row count */
IF OBJECT_ID('dbo.loan_applications', 'U') IS NOT NULL
BEGIN
    SELECT COUNT_BIG(*) AS TotalRows
    FROM dbo.loan_applications;
END;
GO

/* 4. Column count */
SELECT COUNT(*) AS TotalColumns
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME = 'loan_applications';
GO

/* 5. Complete schema - REQUIRED before column-specific analysis */
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

/* 6. First 10 rows */
SELECT TOP (10) *
FROM dbo.loan_applications;
GO

/* 7. Last 10 rows by physical/display order.
   If the dataset has a reliable date or ID column, use that column after schema review. */
SELECT TOP (10) *
FROM dbo.loan_applications;
GO

/* 8. NULL count for every column using dynamic SQL */
DECLARE @sql NVARCHAR(MAX) = N'';

SELECT @sql = STRING_AGG(
    CAST(
        N'SELECT ' + QUOTENAME(COLUMN_NAME,'''') + N' AS ColumnName, ' +
        N'COUNT_BIG(*) AS TotalRows, ' +
        N'SUM(CASE WHEN ' + QUOTENAME(COLUMN_NAME) + N' IS NULL THEN 1 ELSE 0 END) AS NullRows ' +
        N'FROM dbo.loan_applications'
        AS NVARCHAR(MAX)
    ),
    N' UNION ALL '
)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME = 'loan_applications';

IF @sql IS NOT NULL AND LEN(@sql) > 0
    EXEC sys.sp_executesql @sql;
GO

/* 9. Empty-string count for text columns */
DECLARE @sql_text NVARCHAR(MAX) = N'';

SELECT @sql_text = STRING_AGG(
    CAST(
        N'SELECT ' + QUOTENAME(COLUMN_NAME,'''') + N' AS ColumnName, ' +
        N'SUM(CASE WHEN LTRIM(RTRIM(' + QUOTENAME(COLUMN_NAME) + N')) = '''' THEN 1 ELSE 0 END) AS EmptyStringRows ' +
        N'FROM dbo.loan_applications'
        AS NVARCHAR(MAX)
    ),
    N' UNION ALL '
)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME = 'loan_applications'
  AND DATA_TYPE IN ('char','varchar','nchar','nvarchar','text','ntext');

IF @sql_text IS NOT NULL AND LEN(@sql_text) > 0
    EXEC sys.sp_executesql @sql_text;
GO

/* 10. Duplicate full rows */
SELECT
    COUNT_BIG(*) AS TotalRows,
    COUNT_BIG(*) - COUNT_BIG(DISTINCT RowHash) AS DuplicateRows
FROM
(
    SELECT
        CONVERT(VARCHAR(64), HASHBYTES('SHA2_256',
            (SELECT STRING_AGG(CONVERT(NVARCHAR(MAX), ISNULL(CONVERT(NVARCHAR(MAX), c.COLUMN_NAME), '')), '|')
             FROM INFORMATION_SCHEMA.COLUMNS c
             WHERE c.TABLE_SCHEMA='dbo' AND c.TABLE_NAME='loan_applications')
        ), 2) AS RowHash
    FROM dbo.loan_applications
) AS x;
GO

/* 11. Numeric-column descriptive statistics (generated dynamically) */
DECLARE @sql_num NVARCHAR(MAX) = N'';

SELECT @sql_num = STRING_AGG(
    CAST(
        N'SELECT ' + QUOTENAME(COLUMN_NAME,'''') + N' AS ColumnName, ' +
        N'MIN(TRY_CONVERT(DECIMAL(38,10),' + QUOTENAME(COLUMN_NAME) + N')) AS MinValue, ' +
        N'MAX(TRY_CONVERT(DECIMAL(38,10),' + QUOTENAME(COLUMN_NAME) + N')) AS MaxValue, ' +
        N'AVG(TRY_CONVERT(DECIMAL(38,10),' + QUOTENAME(COLUMN_NAME) + N')) AS AvgValue, ' +
        N'COUNT(TRY_CONVERT(DECIMAL(38,10),' + QUOTENAME(COLUMN_NAME) + N')) AS NumericRows ' +
        N'FROM dbo.loan_applications'
        AS NVARCHAR(MAX)
    ),
    N' UNION ALL '
)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA='dbo'
  AND TABLE_NAME='loan_applications'
  AND DATA_TYPE IN ('tinyint','smallint','int','bigint','decimal','numeric','float','real','money','smallmoney');

IF @sql_num IS NOT NULL AND LEN(@sql_num) > 0
    EXEC sys.sp_executesql @sql_num;
GO

/* 12. Final validation summary */
SELECT
    DB_NAME() AS DatabaseName,
    OBJECT_SCHEMA_NAME(OBJECT_ID('dbo.loan_applications')) AS TableSchema,
    OBJECT_NAME(OBJECT_ID('dbo.loan_applications')) AS TableName,
    (SELECT COUNT_BIG(*) FROM dbo.loan_applications) AS TotalRows,
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
     WHERE TABLE_SCHEMA='dbo' AND TABLE_NAME='loan_applications') AS TotalColumns;
GO

/* NEXT STEP:
Run the schema query from section 5 and use its actual 32-column output to build
03_eda_analysis.sql. Do not assume column names from a different loan dataset.
*/
