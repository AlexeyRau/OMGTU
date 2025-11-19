SELECT 
    cat_name,
    vacancy_count,
    avg_salary
FROM salary_by_category
ORDER BY vacancy_count DESC, avg_salary DESC;