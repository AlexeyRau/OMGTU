UPDATE candidate_profiles
SET additional_info = additional_info || '{"expected_salary": 120000}'
WHERE profile_id = 2;

SELECT r.res_full_name, p.additional_info
FROM candidate_profiles p
JOIN resumes r ON p.profile_resume_id = r.res_id;