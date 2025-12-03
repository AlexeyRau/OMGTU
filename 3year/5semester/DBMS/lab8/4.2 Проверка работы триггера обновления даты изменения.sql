UPDATE Responses SET resp_status_id = 2 WHERE resp_id = 1;

SELECT * FROM Responses
ORDER BY resp_id ASC;