DROP PROCEDURE IF EXISTS show_high_salary_vacancies(INTEGER);

CREATE OR REPLACE PROCEDURE show_high_salary_vacancies(min_salary INTEGER)
LANGUAGE plpgsql
AS $$
DECLARE
    cur CURSOR FOR 
        SELECT 
            v.vac_position,
            to_char(v.vac_salary, '9999999990.00') as formatted_salary,
            e.emp_company_name,
            c.cat_name
        FROM Vacancies v
        JOIN Employers e ON v.vac_emp_id = e.emp_id
        JOIN Categories c ON v.vac_cat_id = c.cat_id
        WHERE v.vac_salary > min_salary
        ORDER BY v.vac_salary DESC;
    
    rec RECORD;
BEGIN
    OPEN cur;
    LOOP
        FETCH cur INTO rec;
        EXIT WHEN NOT FOUND;
        
        RAISE NOTICE 'Вакансия: %, Зарплата: %, Работодатель: %, Категория: %',
            rec.vac_position,
            rec.formatted_salary,
            rec.emp_company_name,
            rec.cat_name;
    END LOOP;
    CLOSE cur;
END;
$$;

CALL show_high_salary_vacancies(100000);