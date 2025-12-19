CREATE OR REPLACE PROCEDURE allocate_payments_fifo(
    p_client_id INTEGER,
    p_target_period DATE
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_payment_record RECORD;
    v_accrual_record RECORD;
    v_remaining_amount DECIMAL(15,2);
    v_allocated DECIMAL(15,2);
BEGIN
    CREATE TEMP TABLE IF NOT EXISTS temp_payments AS
    SELECT 
        p.payment_id,
        p.amount - COALESCE(SUM(pa.allocated_amount), 0) AS remaining
    FROM payments p
    LEFT JOIN payment_allocations pa ON p.payment_id = pa.payment_id
    WHERE p.client_id = p_client_id
    GROUP BY p.payment_id, p.amount
    HAVING p.amount - COALESCE(SUM(pa.allocated_amount), 0) > 0;

    FOR v_accrual_record IN 
        SELECT 
            a.accrual_id,
            a.amount - COALESCE(SUM(pa.allocated_amount), 0) AS debt
        FROM contracts c
        JOIN accruals a ON c.contract_id = a.contract_id
        LEFT JOIN payment_allocations pa ON a.accrual_id = pa.accrual_id
        WHERE c.client_id = p_client_id
            AND a.period <= p_target_period
            AND a.status != 'Оплачено'
        GROUP BY a.accrual_id, a.amount
        HAVING a.amount - COALESCE(SUM(pa.allocated_amount), 0) > 0
        ORDER BY a.period, a.created_date
    LOOP
        FOR v_payment_record IN 
            SELECT * FROM temp_payments WHERE remaining > 0 ORDER BY payment_id
        LOOP
            IF v_payment_record.remaining >= v_accrual_record.debt THEN
                v_allocated := v_accrual_record.debt;
                UPDATE temp_payments 
                SET remaining = remaining - v_allocated 
                WHERE payment_id = v_payment_record.payment_id;
            ELSE
                v_allocated := v_payment_record.remaining;
                UPDATE temp_payments 
                SET remaining = 0 
                WHERE payment_id = v_payment_record.payment_id;
            END IF;

            INSERT INTO payment_allocations (payment_id, accrual_id, allocated_amount)
            VALUES (v_payment_record.payment_id, v_accrual_record.accrual_id, v_allocated);

            v_accrual_record.debt := v_accrual_record.debt - v_allocated;

            EXIT WHEN v_accrual_record.debt <= 0;
        END LOOP;

        IF v_accrual_record.debt <= 0 THEN
            UPDATE accruals SET status = 'Оплачено' WHERE accrual_id = v_accrual_record.accrual_id;
        ELSE
            UPDATE accruals SET status = 'Частично оплачено' WHERE accrual_id = v_accrual_record.accrual_id;
        END IF;
    END LOOP;

    DROP TABLE temp_payments;
END;
$$;