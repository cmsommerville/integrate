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
     WHERE name = '$(UID_ADMIN)')
BEGIN
    CREATE LOGIN $(UID_ADMIN) WITH PASSWORD = '$(PWD_ADMIN)'
END

IF NOT EXISTS 
    (SELECT name  
     FROM master.sys.server_principals
     WHERE name = '$(UID_ANALYST)')
BEGIN
CREATE LOGIN $(UID_ANALYST) WITH PASSWORD = '$(PWD_ANALYST)'
END

IF NOT EXISTS 
    (SELECT name  
     FROM master.sys.server_principals
     WHERE name = '$(UID_APPLICATION)')
BEGIN
CREATE LOGIN $(UID_APPLICATION) WITH PASSWORD = '$(PWD_APPLICATION)'
END





USE integrate
GO 



IF DATABASE_PRINCIPAL_ID('rls_restricted') IS NULL
BEGIN 
    CREATE ROLE rls_restricted
END 



IF NOT EXISTS (SELECT name
                FROM sys.database_principals
                WHERE type = N'S' AND name = N'$(UID_ADMIN)')
BEGIN
    CREATE USER $(UID_ADMIN) FOR LOGIN $(UID_ADMIN)
    ALTER ROLE db_owner ADD MEMBER $(UID_ADMIN)
END

IF NOT EXISTS (SELECT name
                FROM sys.database_principals
                WHERE type = N'S' AND name = N'$(UID_ANALYST)')
BEGIN
    CREATE USER $(UID_ANALYST) FOR LOGIN $(UID_ANALYST)
    ALTER ROLE db_owner ADD MEMBER $(UID_ANALYST)
END

IF NOT EXISTS (SELECT name
                FROM sys.database_principals
                WHERE type = N'S' AND name = N'$(UID_APPLICATION)')
BEGIN
    CREATE USER $(UID_APPLICATION) FOR LOGIN $(UID_APPLICATION)
    ALTER ROLE rls_restricted ADD MEMBER $(UID_APPLICATION)
    ALTER ROLE db_owner ADD MEMBER $(UID_APPLICATION)
END


PRINT 'Base users, logins, and roles created'