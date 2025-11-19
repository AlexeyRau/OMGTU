CREATE OR REPLACE FUNCTION get_company_vacancies_count(company_id integer)
RETURNS integer
LANGUAGE plpgsql
AS $$
DECLARE
    vacancy_count integer;
BEGIN
    SELECT COUNT(*) 
    INTO vacancy_count
    FROM vacancies 
    WHERE vac_emp_id = company_id;
    
    RETURN vacancy_count;
END;
$$;

SELECT get_company_vacancies_count(1) as vacancy_count;