CREATE OR REPLACE FUNCTION important_function()
RETURNS TEXT AS $$
BEGIN
    RETURN 'Важная бизнес-логика 1';
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION important_function();