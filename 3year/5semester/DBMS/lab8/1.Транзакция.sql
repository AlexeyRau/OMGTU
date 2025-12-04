BEGIN;

UPDATE Responses 
SET resp_status_id = 2
WHERE resp_id = 1;

SAVEPOINT before_changes;

UPDATE Responses 
SET resp_status_id = 3
WHERE resp_id = 2;

ROLLBACK TO SAVEPOINT before_changes;

COMMIT;

SELECT resp_id, resp_vacancy_id, resp_resume_id, resp_status_id 
FROM Responses ORDER BY resp_id;