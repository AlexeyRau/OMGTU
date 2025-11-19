DROP PROCEDURE IF EXISTS add_response;
CREATE OR REPLACE PROCEDURE add_response(
    p_vacancy_id INTEGER,
    p_resume_id INTEGER,
    p_staff_id INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_vacancy_exists BOOLEAN;
    v_resume_exists BOOLEAN;
BEGIN
    SELECT EXISTS(SELECT 1 FROM Vacancies WHERE vac_id = p_vacancy_id) INTO v_vacancy_exists;
    IF NOT v_vacancy_exists THEN
        RAISE EXCEPTION 'Вакансия с ID % не найдена', p_vacancy_id;
    END IF;
    
    SELECT EXISTS(SELECT 1 FROM Resumes WHERE res_id = p_resume_id) INTO v_resume_exists;
    IF NOT v_resume_exists THEN
        RAISE EXCEPTION 'Резюме с ID % не найдено', p_resume_id;
    END IF;
    
    INSERT INTO Responses (
        resp_vacancy_id,
        resp_resume_id,
        resp_date,
        resp_status_id,
        resp_staff_id
    ) VALUES (
        p_vacancy_id,
        p_resume_id,
        CURRENT_DATE,
        1,
        p_staff_id
    );
END;
$$;

SELECT * FROM Responses WHERE resp_id = 6;