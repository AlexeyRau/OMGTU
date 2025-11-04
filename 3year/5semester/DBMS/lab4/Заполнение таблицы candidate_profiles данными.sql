INSERT INTO candidate_profiles VALUES
(1, 1, '{"languages": ["английский", "немецкий"], "certificates": ["AWS Certified", "Scrum Master"], "relocation": true, "expected_salary": 150000}'::jsonb),
(2, 2, '{"languages": ["английский"], "certificates": ["Sales Professional"], "relocation": false, "expected_salary": 100000}'::jsonb),
(3, 3, '{"languages": ["английский", "французский"], "certificates": ["CCNA", "Linux Professional"], "relocation": true, "expected_salary": 110000}'::jsonb);

SELECT r.res_full_name, p.additional_info
FROM candidate_profiles p
JOIN resumes r ON p.profile_resume_id = r.res_id;