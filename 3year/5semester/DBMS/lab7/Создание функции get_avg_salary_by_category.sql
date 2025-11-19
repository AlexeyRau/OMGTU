CREATE OR REPLACE FUNCTION get_avg_salary_by_category(category_id integer)
RETURNS numeric
LANGUAGE sql
AS $$
    SELECT AVG(vac_salary) 
    FROM vacancies 
    WHERE vac_cat_id = category_id;
$$;

SELECT get_avg_salary_by_category(7) as avg_salary;