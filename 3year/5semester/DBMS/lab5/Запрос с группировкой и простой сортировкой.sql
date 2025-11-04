SELECT vs.status_name, COUNT(v.vac_id) as vacancy_count
FROM Vacancies v
JOIN VacancyStatuses vs ON v.vac_status_id = vs.status_id
GROUP BY vs.status_name
ORDER BY vacancy_count DESC;