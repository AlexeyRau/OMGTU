SELECT * 
FROM contracts
WHERE EXTRACT(YEAR FROM start_date) = 2023
  AND status = 'Активен'
  AND service_id != 3;