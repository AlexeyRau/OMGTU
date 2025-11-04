SELECT r.res_full_name, v.vac_position
FROM Resumes r
LEFT JOIN Responses resp ON r.res_id = resp.resp_resume_id
LEFT JOIN Vacancies v ON resp.resp_vacancy_id = v.vac_id;