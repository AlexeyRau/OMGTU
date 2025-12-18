SELECT 
    m.serial_number AS "Счётчик",
    s.service_name AS "Услуга",
    mr.reading_date AS "Дата показания",
    mr.current_value AS "Текущее",
    mr.previous_value AS "Предыдущее",
    mr.consumption AS "Расход"
FROM meter_readings mr
JOIN meters m ON mr.meter_id = m.meter_id
JOIN contracts c ON m.contract_id = c.contract_id
JOIN services s ON c.service_id = s.service_id
WHERE mr.reading_date = '2024-02-01'
    AND mr.consumption > 0
ORDER BY s.service_name, m.serial_number;