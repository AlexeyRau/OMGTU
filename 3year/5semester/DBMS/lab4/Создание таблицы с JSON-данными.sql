CREATE TABLE candidate_profiles (
    profile_id integer NOT NULL,
    profile_resume_id integer NOT NULL UNIQUE,
    additional_info jsonb,
    CONSTRAINT candidate_profiles_PK PRIMARY KEY (profile_id),
    CONSTRAINT candidate_profiles_FK FOREIGN KEY (profile_resume_id)
        REFERENCES resumes (res_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);