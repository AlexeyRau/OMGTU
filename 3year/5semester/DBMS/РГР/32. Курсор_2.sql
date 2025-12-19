DO $$
DECLARE
    report_rec RECORD;
    report_cursor CURSOR(year_month DATE) FOR
        SELECT 
            c.full_name AS client_name,
            s.service_name,
            cntr.contract_number,
            m.serial_number AS meter_serial,
            mr.reading_date,
            mr.consumption,
            t.rate,
            (mr.consumption * t.rate) AS calculated_cost
        FROM meter_readings mr
        JOIN meters m ON mr.meter_id = m.meter_id
        JOIN contracts cntr ON m.contract_id = cntr.contract_id
        JOIN clients c ON cntr.client_id = c.client_id
        JOIN services s ON cntr.service_id = s.service_id
        JOIN tariffs t ON s.service_id = t.service_id
        WHERE DATE_TRUNC('month', mr.reading_date) = DATE_TRUNC('month', year_month)
          AND mr.reading_date BETWEEN t.start_date AND t.end_date
          AND cntr.status = 'Активен'
        ORDER BY c.full_name, s.service_name, mr.reading_date;
BEGIN
    OPEN report_cursor('2024-03-01');
    LOOP
        FETCH report_cursor INTO report_rec;
        EXIT WHEN NOT FOUND;
        
        RAISE NOTICE 'Клиент: %, Услуга: %, Договор: %, Счетчик: %, Дата: %, Расход: %, Тариф: %, Сумма: % руб.',
            report_rec.client_name,
            report_rec.service_name,
            report_rec.contract_number,
            report_rec.meter_serial,
            report_rec.reading_date,
            to_char(report_rec.consumption, 'FM9999999990.00'),
            report_rec.rate,
            to_char(report_rec.calculated_cost, 'FM9999999990.00');
    END LOOP;
    CLOSE report_cursor;
END $$;