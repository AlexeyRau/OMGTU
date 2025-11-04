SELECT 
    res_full_name,
    res_experience,
    CASE 
        WHEN res_experience < 3 THEN 'Начинающий'
        WHEN res_experience BETWEEN 3 AND 5 THEN 'Опытный'
        ELSE 'Эксперт'
    END AS "Уровень опыта"
FROM Resumes
ORDER BY res_experience DESC;