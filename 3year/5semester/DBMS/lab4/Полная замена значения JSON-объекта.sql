UPDATE candidate_profiles
SET additional_info = '{"languages": ["английский", "китайский"], "certificates": ["AWS Certified"], "relocation": true, "expected_salary": 160000}'::jsonb
WHERE profile_id = 1;

SELECT r.res_full_name, p.additional_info
FROM candidate_profiles p
JOIN resumes r ON p.profile_resume_id = r.res_id;