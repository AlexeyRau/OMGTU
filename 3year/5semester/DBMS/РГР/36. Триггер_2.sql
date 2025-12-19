DROP TRIGGER IF EXISTS trg_check_reading_date ON meter_readings;
DROP FUNCTION IF EXISTS check_reading_date_sequence();

CREATE OR REPLACE FUNCTION check_reading_date_sequence()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    last_reading_date DATE;
BEGIN
    SELECT MAX(reading_date) INTO last_reading_date
    FROM meter_readings
    WHERE meter_id = NEW.meter_id;

    IF last_reading_date IS NOT NULL AND NEW.reading_date <= last_reading_date THEN
        RAISE EXCEPTION 'Дата нового показания (%) должна быть позже последней существующей даты (%) для счётчика %',
                        NEW.reading_date, last_reading_date, NEW.meter_id;
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_check_reading_date
BEFORE INSERT
ON meter_readings
FOR EACH ROW
EXECUTE FUNCTION check_reading_date_sequence();