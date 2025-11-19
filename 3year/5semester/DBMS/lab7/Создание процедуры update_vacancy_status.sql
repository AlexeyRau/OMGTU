DROP PROCEDURE IF EXISTS update_vacancy_status;
CREATE OR REPLACE PROCEDURE update_vacancy_status(
    p_vacancy_id INTEGER,
    p_new_status_id INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE Vacancies 
    SET vac_status_id = p_new_status_id
    WHERE vac_id = p_vacancy_id;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Вакансия с ID % не найдена', p_vacancy_id;
    END IF;
END;
$$;

SELECT * FROM Vacancies WHERE vac_id = 1;
