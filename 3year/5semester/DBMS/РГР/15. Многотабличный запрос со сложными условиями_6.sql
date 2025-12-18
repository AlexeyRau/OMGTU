SELECT 
    cl.client_id,
    cl.full_name,
    cl.client_type,
    COUNT(c.contract_id) AS "Кол-во договоров"
FROM clients cl
LEFT JOIN contracts c ON cl.client_id = c.client_id
WHERE cl.client_id NOT IN (
    SELECT DISTINCT client_id 
    FROM contracts 
    WHERE status = 'Расторгнут'
)
GROUP BY cl.client_id, cl.full_name, cl.client_type
HAVING COUNT(c.contract_id) > 0;