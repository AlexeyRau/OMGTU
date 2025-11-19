CREATE MATERIALIZED VIEW salary_by_category AS
SELECT 
    c.cat_name,
    COUNT(v.vac_id) AS vacancy_count,
    AVG(v.vac_salary) AS avg_salary,
    MIN(v.vac_salary) AS min_salary,
    MAX(v.vac_salary) AS max_salary
FROM vacancies v
JOIN categories c ON v.vac_cat_id = c.cat_id
GROUP BY c.cat_id, c.cat_name;

SELECT * FROM salary_by_category;