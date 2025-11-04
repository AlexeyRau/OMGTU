SELECT 
    COUNT(*) AS "Всего вакансий",
    AVG(vac_salary) AS "Средняя зарплата",
    MAX(vac_salary) AS "Максимальная зарплата",
    MIN(vac_salary) AS "Минимальная зарплата"
FROM Vacancies;