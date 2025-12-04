CREATE OR REPLACE FUNCTION get_avg_salary_by_category(p_category_id INTEGER)
RETURNS NUMERIC
LANGUAGE plpgsql
AS $$
DECLARE
    v_avg_salary NUMERIC;
BEGIN
    SELECT AVG(vac_salary) INTO v_avg_salary
    FROM Vacancies 
    WHERE vac_cat_id = p_category_id 
      AND vac_status_id = 1;
    
    RETURN COALESCE(v_avg_salary, 0);
END;
$$;

--SELECT * FROM Vacancies WHERE vac_cat_id = 5 AND vac_status_id = 1;
SELECT get_avg_salary_by_category(5) AS avg_salary_programming;