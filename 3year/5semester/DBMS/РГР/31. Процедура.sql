CREATE OR REPLACE PROCEDURE generate_accruals_for_month(
    p_month DATE
) AS $$
DECLARE
    v_contract_id INTEGER;
    v_service_id INTEGER;
    v_total_consumption DECIMAL(15,3);
    v_current_tariff DECIMAL(10,2);
    v_accrual_amount DECIMAL(15,2);
    v_period DATE := DATE_TRUNC('month', p_month);
BEGIN
    FOR v_contract_id, v_service_id IN 
        SELECT contract_id, service_id 
        FROM contracts 
        WHERE status = 'Активен'
    LOOP
        SELECT COALESCE(SUM(mr.consumption), 0)
        INTO v_total_consumption
        FROM meter_readings mr
        JOIN meters m ON mr.meter_id = m.meter_id
        WHERE m.contract_id = v_contract_id
            AND DATE_TRUNC('month', mr.reading_date) = v_period;
        
        SELECT rate
        INTO v_current_tariff
        FROM tariffs
        WHERE service_id = v_service_id
            AND start_date <= v_period
            AND (end_date >= v_period OR end_date IS NULL)
        ORDER BY start_date DESC
        LIMIT 1;
        
        IF v_current_tariff IS NULL THEN
            SELECT rate
            INTO v_current_tariff
            FROM tariffs
            WHERE service_id = v_service_id
            ORDER BY start_date DESC
            LIMIT 1;
        END IF;
        
        v_accrual_amount := v_total_consumption * COALESCE(v_current_tariff, 0);
        
        INSERT INTO accruals (contract_id, period, consumption, amount, created_date, status)
        VALUES (
            v_contract_id,
            v_period,
            v_total_consumption,
            v_accrual_amount,
            CURRENT_DATE,
            CASE WHEN v_accrual_amount = 0 THEN 'Оплачено' ELSE 'Не оплачено' END
        );
    END LOOP;
    
    RAISE NOTICE 'Начисления за % сформированы.', p_month;
END;
$$ LANGUAGE plpgsql;

CALL generate_accruals_for_month('2024-04-01');