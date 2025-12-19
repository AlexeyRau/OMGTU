SELECT 
    c.full_name, 
    cntr.contract_number, 
    SUM(a.amount) as total_accrued
FROM clients c
JOIN contracts cntr ON c.client_id = cntr.client_id
JOIN accruals a ON cntr.contract_id = a.contract_id
WHERE c.client_id = 1
GROUP BY c.full_name, cntr.contract_number;