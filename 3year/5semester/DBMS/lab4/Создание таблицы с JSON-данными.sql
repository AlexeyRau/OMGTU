CREATE TABLE candidate_profiles (
    profile_id integer NOT NULL,
    profile_resume_id integer NOT NULL,
    additional_info jsonb,
    CONSTRAINT candidate_profiles_PK PRIMARY KEY (profile_id)
);

ALTER TABLE candidate_profiles
ADD CONSTRAINT candidate_profiles_FK FOREIGN KEY (profile_resume_id)
REFERENCES resumes (res_id)
ON DELETE CASCADE
ON UPDATE CASCADE;

SELECT r.res_full_name, p.additional_info
FROM candidate_profiles p
JOIN resumes r ON p.profile_resume_id = r.res_id;