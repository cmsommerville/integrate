CREATE FUNCTION rls.fn_rls__user_role(@user_role VARCHAR(30))
    RETURNS TABLE
WITH SCHEMABINDING
AS
RETURN SELECT 1 AS fn_rls__user_role_output
WHERE 
    COALESCE(IS_MEMBER('rls_restricted'), 1) = 0 OR (
        @user_role IN (
            SELECT value AS user_role 
            FROM STRING_SPLIT(CAST(SESSION_CONTEXT(N'user_roles') AS VARCHAR(8000)), ';')
        )
        OR 'superuser' IN (
            SELECT value AS user_role 
            FROM STRING_SPLIT(CAST(SESSION_CONTEXT(N'user_roles') AS VARCHAR(8000)), ';')
        )
    )