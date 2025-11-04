SELECT res_full_name, res_experience
FROM Resumes
WHERE res_experience > (SELECT AVG(res_experience) FROM Resumes);