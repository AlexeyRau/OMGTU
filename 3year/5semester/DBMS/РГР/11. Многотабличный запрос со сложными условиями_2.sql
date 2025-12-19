SELECT a.*, cntr.contract_number
FROM accruals a
JOIN contracts cntr ON a.contract_id = cntr.contract_id
JOIN services s ON cntr.service_id = s.service_id
WHERE a.period = '2024-02-01'
  AND cntr.status = 'Активен'
  AND s.service_name = 'Электроснабжение';