SELECT mr.*, m.serial_number
FROM meter_readings mr
JOIN meters m ON mr.meter_id = m.meter_id
WHERE mr.reading_date BETWEEN '2024-01-01' AND '2024-03-31';