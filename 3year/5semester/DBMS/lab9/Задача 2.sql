DROP FUNCTION IF EXISTS calculate_avg_salary_by_category();

CREATE OR REPLACE FUNCTION calculate_avg_salary_by_category()
RETURNS TABLE(category_name TEXT, avg_salary TEXT)
LANGUAGE plpgsql
AS $$
DECLARE
    cur CURSOR FOR 
        SELECT 
            c.cat_name,
            to_char(ROUND(COALESCE(AVG(v.vac_salary), 0), 2), 'FM9999999990.00') as avg_sal
        FROM Categories c
        LEFT JOIN Vacancies v ON c.cat_id = v.vac_cat_id
        GROUP BY c.cat_id, c.cat_name
        ORDER BY c.cat_name;
    
    cat_name_val TEXT;
    avg_sal_val TEXT;
BEGIN
    OPEN cur;
    LOOP
        FETCH cur INTO cat_name_val, avg_sal_val;
        EXIT WHEN NOT FOUND;
        
        category_name := cat_name_val;
        avg_salary := avg_sal_val;
        RETURN NEXT;
    END LOOP;
    CLOSE cur;
END;
$$;

SELECT * FROM calculate_avg_salary_by_category();