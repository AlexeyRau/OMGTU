SELECT 
    m.serial_number AS "Счётчик",
    s.service_name AS "Услуга",
    mr.reading_date AS "Дата",
    mr.consumption AS "Текущий расход",
    LAG(mr.consumption) OVER (
        PARTITION BY mr.meter_id 
        ORDER BY mr.reading_date
    ) AS "Предыдущий расход",
    ROUND(
        (mr.consumption - LAG(mr.consumption) OVER (
            PARTITION BY mr.meter_id 
            ORDER BY mr.reading_date
        )) * 100.0 / NULLIF(LAG(mr.consumption) OVER (
            PARTITION BY mr.meter_id 
            ORDER BY mr.reading_date
        ), 0), 2
    ) AS "Изменение, %"
FROM meter_readings mr
JOIN meters m ON mr.meter_id = m.meter_id
JOIN contracts c ON m.contract_id = c.contract_id
JOIN services s ON c.service_id = s.service_id
WHERE mr.reading_date >= '2024-01-01'
ORDER BY m.serial_number, mr.reading_date;