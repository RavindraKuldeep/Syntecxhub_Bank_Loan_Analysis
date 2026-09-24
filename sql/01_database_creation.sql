/* Syntecxhub Bank Loan Analysis
   File: 01_database_creation.sql
   Purpose: Create/reset the project database.
*/

USE master;
GO

IF DB_ID('Syntecxhub_Bank_Loan_Analysis') IS NOT NULL
BEGIN
    ALTER DATABASE Syntecxhub_Bank_Loan_Analysis
    SET SINGLE_USER
    WITH ROLLBACK IMMEDIATE;

    DROP DATABASE Syntecxhub_Bank_Loan_Analysis;
END;
GO

CREATE DATABASE Syntecxhub_Bank_Loan_Analysis;
GO

USE Syntecxhub_Bank_Loan_Analysis;
GO

SELECT DB_NAME() AS CurrentDatabase;
GO

/*
NOTE:
The loan_applications table is imported from the source dataset using SQL Server Import/Export Wizard.
After import, validate the actual schema before running the EDA script.
*/
