CREATE OR REPLACE FUNCTION calculate_penalty(
    p_contract_id INTEGER,
    p_calc_date DATE DEFAULT CURRENT_DATE
) RETURNS DECIMAL(15,2) AS $$
DECLARE
    total_penalty DECIMAL(15,2) := 0;
    penalty_rate DECIMAL(5,4) := 0.01; -- 1% в день
    days_delay INTEGER;
    debt_amount DECIMAL(15,2);
    payment_due_date DATE;
BEGIN
    SELECT COALESCE(SUM(amount), 0)
    INTO debt_amount
    FROM accruals
    WHERE contract_id = p_contract_id
        AND status IN ('Не оплачено', 'Частично оплачено')
        AND period < DATE_TRUNC('month', p_calc_date);
    
    IF debt_amount > 0 THEN
        payment_due_date := DATE_TRUNC('month', p_calc_date)::DATE 
            - INTERVAL '1 month' 
            + INTERVAL '10 days';
        
        days_delay := p_calc_date - payment_due_date;
        
        IF days_delay > 0 THEN
            total_penalty := debt_amount * penalty_rate * days_delay;
        END IF;
    END IF;
    
    RETURN ROUND(total_penalty, 2);
END;
$$ LANGUAGE plpgsql;

SELECT 
    c.contract_id,
    c.contract_number,
    cl.full_name,
    calculate_penalty(c.contract_id, '2024-04-20') AS penalty_amount,
    calculate_penalty(c.contract_id, '2024-04-05') AS penalty_early -- до 10 числа
FROM contracts c
JOIN clients cl ON c.client_id = cl.client_id
WHERE c.contract_id IN (1, 2, 3, 4)
ORDER BY penalty_amount DESC NULLS LAST;