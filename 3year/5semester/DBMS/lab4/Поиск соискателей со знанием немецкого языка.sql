SELECT r.res_full_name, p.additional_info -> 'languages' AS languages
FROM candidate_profiles p
JOIN resumes r ON p.profile_resume_id = r.res_id
WHERE p.additional_info -> 'languages' @> '["немецкий"]'::jsonb;