SELECT 
    m.serial_number AS "Серийный номер",
    m.model AS "Модель",
    m.installation_date AS "Дата установки",
    c.contract_number AS "Номер договора"
FROM meters m
JOIN contracts c ON m.contract_id = c.contract_id
WHERE m.installation_date > '2023-07-01'
    AND c.status = 'Активен'
    AND c.end_date IS NULL;