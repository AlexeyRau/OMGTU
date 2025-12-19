SELECT c.client_id, c.full_name
FROM clients c
WHERE c.client_id IN (
    SELECT cntr.client_id 
    FROM contracts cntr 
    JOIN services s ON cntr.service_id = s.service_id 
    WHERE s.service_name = 'Водоснабжение'
)
AND c.client_id NOT IN (
    SELECT cntr.client_id 
    FROM contracts cntr 
    JOIN services s ON cntr.service_id = s.service_id 
    WHERE s.service_name = 'Газоснабжение'
);