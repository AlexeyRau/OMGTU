CREATE OR REPLACE VIEW active_vacancies AS
SELECT 
    v.vac_id,
    v.vac_position,
    v.vac_salary,
    e.emp_company_name,
    c.cat_name
FROM vacancies v
JOIN employers e ON v.vac_emp_id = e.emp_id
JOIN categories c ON v.vac_cat_id = c.cat_id
WHERE v.vac_status_id = 1;

SELECT * FROM active_vacancies;