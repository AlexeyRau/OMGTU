SELECT r.res_full_name, v.vac_position, rs.status_name
FROM Responses resp
INNER JOIN Resumes r ON resp.resp_resume_id = r.res_id
INNER JOIN Vacancies v ON resp.resp_vacancy_id = v.vac_id
INNER JOIN ResponseStatuses rs ON resp.resp_status_id = rs.status_id;