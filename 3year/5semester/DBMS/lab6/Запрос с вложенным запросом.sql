SELECT 
    av.vac_position,
    av.vac_salary,
    av.emp_company_name
FROM active_vacancies av
WHERE av.vac_salary > (
    SELECT AVG(vac_salary) 
    FROM active_vacancies
);