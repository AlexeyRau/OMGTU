DO $$
DECLARE
    cur_service_consumption CURSOR FOR
        SELECT 
            s.service_name,
            s.unit,
            COUNT(DISTINCT mr.meter_id) AS meters_count,
            SUM(mr.consumption) AS total_consumption,
            AVG(mr.consumption) AS avg_consumption,
            MIN(mr.consumption) AS min_consumption,
            MAX(mr.consumption) AS max_consumption
        FROM meter_readings mr
        JOIN meters m ON mr.meter_id = m.meter_id
        JOIN contracts c ON m.contract_id = c.contract_id
        JOIN services s ON c.service_id = s.service_id
        WHERE DATE_TRUNC('month', mr.reading_date) = '2024-03-01'
        GROUP BY s.service_id, s.service_name, s.unit
        ORDER BY total_consumption DESC;
    
    rec RECORD;
BEGIN
    OPEN cur_service_consumption;
    LOOP
        FETCH cur_service_consumption INTO rec;
        EXIT WHEN NOT FOUND;
        
        RAISE NOTICE 'Услуга: % (%), Счётчиков: %, Общий расход: % %, Средний: % %, Min: % %, Max: % %',
            rec.service_name,
            rec.unit,
            rec.meters_count,
            rec.total_consumption,
            rec.unit,
            rec.avg_consumption,
            rec.unit,
            rec.min_consumption,
            rec.unit,
            rec.max_consumption,
            rec.unit;
    END LOOP;
    CLOSE cur_service_consumption;
END $$;