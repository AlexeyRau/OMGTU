CREATE OR REPLACE FUNCTION protect_important_functions()
RETURNS EVENT_TRIGGER AS $$
DECLARE
    obj RECORD;
    protected_items TEXT[] := ARRAY[
        'public.important_function()',
        'public.important_procedure()'
    ];
    is_protected BOOLEAN := FALSE;
BEGIN
    IF tg_tag IN ('DROP FUNCTION', 'DROP PROCEDURE') THEN
        FOR obj IN SELECT * FROM pg_event_trigger_dropped_objects()
        LOOP
            RAISE NOTICE 'Проверяем объект: %', obj.object_identity;
            
            IF obj.object_identity = ANY(protected_items) THEN
                is_protected := TRUE;
                RAISE EXCEPTION 
                    'Удаление защищенной функции/процедуры "%" запрещено!', 
                    obj.object_identity;
            END IF;
        END LOOP;
        
        IF NOT is_protected THEN
            RAISE NOTICE 'Удаление разрешено: ни один из объектов не защищен';
        END IF;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE EVENT TRIGGER protect_functions_trigger
ON sql_drop
EXECUTE FUNCTION protect_important_functions();