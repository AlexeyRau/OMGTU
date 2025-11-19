CREATE OR REPLACE PROCEDURE update_vacancy_status(
    vacancy_id integer,
    new_status_id integer
)
LANGUAGE sql
AS $$
    UPDATE vacancies 
    SET vac_status_id = new_status_id 
    WHERE vac_id = vacancy_id;
$$;

SELECT * FROM vacancies ORDER BY vac_id;