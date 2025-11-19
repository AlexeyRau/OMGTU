CREATE OR REPLACE PROCEDURE add_vacancy(
    vac_position_text text,
    description text,
    requirements text,
    salary numeric,
    employer_id integer,
    category_id integer,
    status_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO vacancies (
        vac_position, vac_description, vac_requirements, 
        vac_salary, vac_emp_id, vac_cat_id, vac_status_id
    ) VALUES (
        vac_position_text, description, requirements, 
        salary, employer_id, category_id, status_id
    );
END;
$$;

SELECT * FROM vacancies ORDER BY vac_id;
