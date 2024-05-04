CREATE FUNCTION rls.fn_rls__user_name(@user_name VARCHAR(30))
    RETURNS TABLE
WITH SCHEMABINDING
AS
RETURN SELECT 1 AS fn_rls__user_name_output
WHERE 
    COALESCE(IS_MEMBER('rls_restricted'), 1) = 0 OR (
        CAST(SESSION_CONTEXT(N'user_name') AS VARCHAR(255)) IN (@user_name, 'superuser')
    )