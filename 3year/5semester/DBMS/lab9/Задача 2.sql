DROP FUNCTION IF EXISTS calculate_avg_salary_by_category();

CREATE OR REPLACE FUNCTION calculate_avg_salary_by_category()
RETURNS TABLE(category_name TEXT, avg_salary NUMERIC)
LANGUAGE plpgsql
AS $$
DECLARE
    cur CURSOR FOR 
        SELECT 
            c.cat_name,
            AVG(v.vac_salary) as avg_sal
        FROM Categories c
        LEFT JOIN Vacancies v ON c.cat_id = v.vac_cat_id
        GROUP BY c.cat_id, c.cat_name
        ORDER BY c.cat_name;
    
    cat_name_val TEXT;
    avg_sal_val NUMERIC;
BEGIN
    OPEN cur;
    LOOP
        FETCH cur INTO cat_name_val, avg_sal_val;
        EXIT WHEN NOT FOUND;
        
        category_name := cat_name_val;
        avg_salary := COALESCE(avg_sal_val, 0);
        RETURN NEXT;
    END LOOP;
    CLOSE cur;
END;
$$;

SELECT * FROM calculate_avg_salary_by_category();