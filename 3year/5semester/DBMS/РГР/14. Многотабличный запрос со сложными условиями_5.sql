SELECT 
    c.contract_number,
    cl.full_name,
    s.service_name,
    c.start_date,
    c.status
FROM contracts c
JOIN clients cl ON c.client_id = cl.client_id
JOIN services s ON c.service_id = s.service_id
WHERE s.service_name IN ('Водоснабжение', 'Электроснабжение')
ORDER BY s.service_name, c.start_date;