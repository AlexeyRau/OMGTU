SELECT s.service_id, s.service_name
FROM services s
WHERE EXISTS (
    SELECT 1 
    FROM tariffs t 
    WHERE t.service_id = s.service_id 
    AND t.start_date <= CURRENT_DATE 
    AND t.end_date >= CURRENT_DATE
)
AND NOT EXISTS (
    SELECT 1 
    FROM contracts cntr
    JOIN accruals a ON cntr.contract_id = a.contract_id
    WHERE cntr.service_id = s.service_id 
    AND a.status = 'Просрочено'
);