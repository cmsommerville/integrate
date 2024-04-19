USE master
GO 
IF NOT EXISTS (
        SELECT name
        FROM sys.databases
        WHERE name = N'integrate'
    ) 
    CREATE DATABASE integrate
GO 

IF NOT EXISTS 
    (SELECT name  
     FROM master.sys.server_principals
     WHERE name = 'dba')
BEGIN
    CREATE LOGIN dba WITH PASSWORD = '$(PWD_DBA)'
END

IF NOT EXISTS 
    (SELECT name  
     FROM master.sys.server_principals
     WHERE name = 'analyst')
BEGIN
CREATE LOGIN analyst WITH PASSWORD = '$(PWD_ANALYST)'
END

IF NOT EXISTS 
    (SELECT name  
     FROM master.sys.server_principals
     WHERE name = 'app_integrate')
BEGIN
CREATE LOGIN app_integrate WITH PASSWORD = '$(PWD_APP_INTEGRATE)'
END





USE integrate
GO 



IF DATABASE_PRINCIPAL_ID('rls_restricted') IS NULL
BEGIN 
    CREATE ROLE rls_restricted
END 



IF NOT EXISTS (SELECT [name]
                FROM [sys].[database_principals]
                WHERE [type] = N'S' AND [name] = N'dba')
BEGIN
    CREATE USER dba FOR LOGIN dba
    ALTER ROLE db_owner ADD MEMBER dba
END

IF NOT EXISTS (SELECT [name]
                FROM [sys].[database_principals]
                WHERE [type] = N'S' AND [name] = N'analyst')
BEGIN
    CREATE USER analyst FOR LOGIN analyst
    ALTER ROLE db_owner ADD MEMBER analyst
END

IF NOT EXISTS (SELECT [name]
                FROM [sys].[database_principals]
                WHERE [type] = N'S' AND [name] = N'app_integrate')
BEGIN
    CREATE USER app_integrate FOR LOGIN app_integrate
    ALTER ROLE rls_restricted ADD MEMBER app_integrate
    ALTER ROLE db_owner ADD MEMBER app_integrate
END


