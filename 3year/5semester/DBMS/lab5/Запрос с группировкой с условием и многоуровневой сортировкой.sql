SELECT c.cat_name, COUNT(v.vac_id) as vacancy_count
FROM Categories c
LEFT JOIN Vacancies v ON c.cat_id = v.vac_cat_id
GROUP BY c.cat_name
HAVING COUNT(v.vac_id) > 0
ORDER BY vacancy_count DESC, c.cat_name ASC;