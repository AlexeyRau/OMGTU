CREATE OR REPLACE PROCEDURE important_procedure()
LANGUAGE plpgsql AS $$
BEGIN
    RAISE NOTICE 'Важная процедура выполнена';
END;
$$;

DROP PROCEDURE important_procedure();
