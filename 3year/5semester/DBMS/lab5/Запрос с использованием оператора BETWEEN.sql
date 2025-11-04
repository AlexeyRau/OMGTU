SELECT vac_position, vac_salary
FROM Vacancies
WHERE vac_salary BETWEEN 80000 AND 100000
ORDER BY vac_salary DESC;