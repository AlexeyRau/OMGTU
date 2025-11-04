UPDATE candidate_profiles
SET additional_info = jsonb_set(additional_info, '{languages, 2}', '"испанский"')
WHERE profile_id = 3;

SELECT r.res_full_name, p.additional_info
FROM candidate_profiles p
JOIN resumes r ON p.profile_resume_id = r.res_id;