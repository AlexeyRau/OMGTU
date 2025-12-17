DROP TABLE IF EXISTS responses_archive;

CREATE TABLE responses_archive (
    arch_id SERIAL PRIMARY KEY,
    resp_vacancy_id INTEGER,
    resp_resume_id INTEGER,
    resp_date DATE,
    resp_status_id INTEGER,
    resp_staff_id INTEGER,
    archived_date DATE DEFAULT CURRENT_DATE
);

INSERT INTO Responses (resp_vacancy_id, resp_resume_id, resp_date, resp_status_id, resp_staff_id) VALUES
(1, 1, CURRENT_DATE - INTERVAL '45 days', 1, 1),
(2, 2, CURRENT_DATE - INTERVAL '60 days', 2, 2),
(3, 3, CURRENT_DATE - INTERVAL '90 days', 3, 3);

DROP PROCEDURE IF EXISTS archive_old_responses();

CREATE OR REPLACE PROCEDURE archive_old_responses()
LANGUAGE plpgsql
AS $$
DECLARE
    cur CURSOR FOR 
        SELECT * 
        FROM Responses 
        WHERE resp_date < CURRENT_DATE - INTERVAL '30 days';
    
    resp_record Responses%ROWTYPE;
    archived_count INTEGER := 0;
BEGIN
    OPEN cur;
    LOOP
        FETCH cur INTO resp_record;
        EXIT WHEN NOT FOUND;
        
        INSERT INTO responses_archive 
            (resp_vacancy_id, resp_resume_id, resp_date, resp_status_id, resp_staff_id)
        VALUES 
            (resp_record.resp_vacancy_id, resp_record.resp_resume_id, 
             resp_record.resp_date, resp_record.resp_status_id, resp_record.resp_staff_id);
        
        DELETE FROM Responses WHERE resp_id = resp_record.resp_id;
        
        archived_count := archived_count + 1;
    END LOOP;
    CLOSE cur;
    
    RAISE NOTICE 'Заархивировано % откликов', archived_count;
END;
$$;

CALL archive_old_responses();

SELECT * FROM responses_archive ORDER BY archived_date;