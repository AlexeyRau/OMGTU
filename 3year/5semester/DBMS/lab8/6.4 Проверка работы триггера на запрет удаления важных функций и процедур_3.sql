CREATE OR REPLACE FUNCTION unprotected_function()
RETURNS INTEGER AS $$
BEGIN
    RETURN 999;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION unprotected_function();