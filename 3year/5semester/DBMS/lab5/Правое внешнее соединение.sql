SELECT r.res_full_name, v.vac_position
FROM Responses resp
RIGHT JOIN Resumes r ON resp.resp_resume_id = r.res_id
RIGHT JOIN Vacancies v ON resp.resp_vacancy_id = v.vac_id;