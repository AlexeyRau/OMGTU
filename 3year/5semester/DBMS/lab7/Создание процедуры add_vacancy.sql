DROP PROCEDURE IF EXISTS add_vacancy;
CREATE OR REPLACE PROCEDURE add_vacancy(
    p_position TEXT,
    p_description TEXT,
    p_requirements TEXT,
    p_salary INTEGER,
    p_employer_id INTEGER,
    p_category_id INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO Vacancies (
        vac_position, 
        vac_description, 
        vac_requirements, 
        vac_salary, 
        vac_emp_id, 
        vac_cat_id, 
        vac_status_id
    ) VALUES (
        p_position,
        p_description,
        p_requirements,
        p_salary,
        p_employer_id,
        p_category_id,
        1
    );
END;
$$;

SELECT * FROM Vacancies WHERE vac_position = 'Data Scientist';