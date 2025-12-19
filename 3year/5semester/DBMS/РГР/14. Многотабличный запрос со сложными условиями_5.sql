SELECT cntr.*, c.full_name, s.service_name
FROM contracts cntr
JOIN clients c ON cntr.client_id = c.client_id
JOIN services s ON cntr.service_id = s.service_id
WHERE s.service_name IN ('Водоснабжение', 'Электроснабжение');