CREATE OR REPLACE FUNCTION update_modified_date()
RETURNS TRIGGER AS $$
BEGIN
    NEW.resp_date = CURRENT_DATE;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_response_date_trigger
BEFORE UPDATE ON Responses
FOR EACH ROW EXECUTE FUNCTION update_modified_date();

SELECT * FROM Responses
ORDER BY resp_id ASC;