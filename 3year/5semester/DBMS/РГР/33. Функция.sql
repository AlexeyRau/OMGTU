CREATE OR REPLACE FUNCTION get_client_debt(client_id INTEGER, target_date DATE)
RETURNS DECIMAL(15,2) AS $$
DECLARE
    total_debt DECIMAL(15,2);
BEGIN
    SELECT COALESCE(SUM(a.amount), 0) - COALESCE(SUM(pa.allocated_amount), 0)
    INTO total_debt
    FROM contracts cntr
    LEFT JOIN accruals a ON cntr.contract_id = a.contract_id
    LEFT JOIN payment_allocations pa ON a.accrual_id = pa.accrual_id
    WHERE cntr.client_id = $1
    AND a.period <= $2
    AND a.status != 'Оплачено';
    
    RETURN total_debt;
END;
$$ LANGUAGE plpgsql;

SELECT full_name, get_client_debt(1, '2024-03-31') AS debt_on_2024_03_31
FROM clients WHERE client_id = 1;