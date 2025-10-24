CREATE TABLE VacancyStatuses (
    status_id SERIAL PRIMARY KEY,
    status_name TEXT NOT NULL
);

CREATE TABLE ResponseStatuses (
    status_id SERIAL PRIMARY KEY,
    status_name TEXT NOT NULL
);

CREATE TABLE Categories (
    cat_id SERIAL PRIMARY KEY,
    cat_name TEXT NOT NULL,
    cat_parent_id INTEGER,
    FOREIGN KEY (cat_parent_id) REFERENCES Categories(cat_id) 
        ON UPDATE CASCADE 
        ON DELETE SET NULL
);

CREATE TABLE Employers (
    emp_id SERIAL PRIMARY KEY,
    emp_company_name TEXT NOT NULL,
    emp_contact_person TEXT,
    emp_contacts TEXT NOT NULL,
    emp_address TEXT
);

CREATE TABLE Resumes (
    res_id SERIAL PRIMARY KEY,
    res_full_name TEXT NOT NULL,
    res_contacts TEXT NOT NULL,
    res_birth_date DATE,
    res_education TEXT,
    res_experience INTEGER,
    res_cat_id INTEGER NOT NULL,
    FOREIGN KEY (res_cat_id) REFERENCES Categories(cat_id) 
        ON UPDATE CASCADE 
        ON DELETE RESTRICT
);

CREATE TABLE Staff (
    staff_id SERIAL PRIMARY KEY,
    staff_name TEXT NOT NULL,
    staff_position TEXT NOT NULL
);

CREATE TABLE Vacancies (
    vac_id SERIAL PRIMARY KEY,
    vac_position TEXT NOT NULL,
    vac_description TEXT,
    vac_requirements TEXT,
    vac_salary NUMERIC(10,2) NOT NULL,
    vac_emp_id INTEGER NOT NULL,
    vac_cat_id INTEGER NOT NULL,
    vac_status_id INTEGER NOT NULL,
    FOREIGN KEY (vac_emp_id) REFERENCES Employers(emp_id) 
        ON UPDATE CASCADE 
        ON DELETE CASCADE,
    FOREIGN KEY (vac_cat_id) REFERENCES Categories(cat_id) 
        ON UPDATE CASCADE 
        ON DELETE RESTRICT,
    FOREIGN KEY (vac_status_id) REFERENCES VacancyStatuses(status_id) 
        ON UPDATE CASCADE 
        ON DELETE RESTRICT
);

CREATE TABLE Responses (
    resp_id SERIAL PRIMARY KEY,
    resp_vacancy_id INTEGER NOT NULL,
    resp_resume_id INTEGER NOT NULL,
    resp_date DATE NOT NULL DEFAULT CURRENT_DATE,
    resp_status_id INTEGER NOT NULL,
    resp_staff_id INTEGER,
    FOREIGN KEY (resp_vacancy_id) REFERENCES Vacancies(vac_id) 
        ON UPDATE CASCADE 
        ON DELETE CASCADE,
    FOREIGN KEY (resp_resume_id) REFERENCES Resumes(res_id) 
        ON UPDATE CASCADE 
        ON DELETE CASCADE,
    FOREIGN KEY (resp_status_id) REFERENCES ResponseStatuses(status_id) 
        ON UPDATE CASCADE 
        ON DELETE RESTRICT,
    FOREIGN KEY (resp_staff_id) REFERENCES Staff(staff_id) 
        ON UPDATE CASCADE 
        ON DELETE SET NULL
);

CREATE TABLE Interviews (
    int_id SERIAL PRIMARY KEY,
    int_response_id INTEGER NOT NULL,
    int_date_time TIMESTAMP NOT NULL,
    int_location TEXT,
    int_result TEXT,
    FOREIGN KEY (int_response_id) REFERENCES Responses(resp_id) 
        ON UPDATE CASCADE 
        ON DELETE CASCADE
);

ALTER TABLE Vacancies ADD CONSTRAINT chk_vac_salary_positive 
CHECK (vac_salary > 0);

ALTER TABLE Resumes ADD CONSTRAINT chk_experience_non_negative 
CHECK (res_experience >= 0);

ALTER TABLE Resumes ADD CONSTRAINT chk_birth_date_reasonable 
CHECK (res_birth_date > '1900-01-01' AND res_birth_date < CURRENT_DATE);

ALTER TABLE Interviews ADD CONSTRAINT chk_interview_date_future 
CHECK (int_date_time > CURRENT_TIMESTAMP);

ALTER TABLE Responses ADD CONSTRAINT chk_response_date_valid 
CHECK (resp_date <= CURRENT_DATE);

ALTER TABLE Categories ADD CONSTRAINT unq_category_name UNIQUE (cat_name);

ALTER TABLE Employers ADD CONSTRAINT unq_company_name UNIQUE (emp_company_name);

ALTER TABLE VacancyStatuses ADD CONSTRAINT unq_vacancy_status UNIQUE (status_name);

ALTER TABLE ResponseStatuses ADD CONSTRAINT unq_response_status UNIQUE (status_name);


