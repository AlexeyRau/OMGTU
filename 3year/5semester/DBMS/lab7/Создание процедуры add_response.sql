CREATE OR REPLACE PROCEDURE add_response(
    vacancy_id integer,
    resume_id integer,
    response_date date,
    status_id integer,
    staff_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO responses (
        resp_vacancy_id, resp_resume_id, resp_date, 
        resp_status_id, resp_staff_id
    ) VALUES (
        vacancy_id, resume_id, response_date, 
        status_id, staff_id
    );
END;
$$;

SELECT * FROM responses ORDER BY resp_id;