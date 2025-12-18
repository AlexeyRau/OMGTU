DROP TRIGGER IF EXISTS trg_check_meter_reading ON meter_readings;
DROP FUNCTION IF EXISTS check_meter_reading_validity();

CREATE OR REPLACE FUNCTION check_meter_reading_validity()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.current_value < NEW.previous_value THEN
        RAISE EXCEPTION 
            'Текущее показание (%) не может быть меньше предыдущего (%) для счётчика %',
            NEW.current_value, NEW.previous_value, NEW.meter_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_meter_reading
BEFORE INSERT OR UPDATE ON meter_readings
FOR EACH ROW
EXECUTE FUNCTION check_meter_reading_validity();

INSERT INTO meter_readings (meter_id, reading_date, current_value, previous_value)
VALUES (1, '2024-05-01', 140.000, 143.900);