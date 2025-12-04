CREATE OR REPLACE FUNCTION log_function_operations()
RETURNS EVENT_TRIGGER AS $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN SELECT * FROM pg_event_trigger_ddl_commands() 
    LOOP
        IF r.command_tag IN ('CREATE FUNCTION', 'DROP FUNCTION', 'CREATE PROCEDURE', 'DROP PROCEDURE') THEN
            RAISE NOTICE 'Операция с функцией/процедурой: % - Объект: %', r.command_tag, r.object_identity;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

CREATE EVENT TRIGGER log_function_trigger
ON ddl_command_end
EXECUTE FUNCTION log_function_operations();