CREATE OR REPLACE FUNCTION update_accrual_status_on_allocation()
RETURNS TRIGGER AS $$
DECLARE
    v_total_allocated DECIMAL(15,2);
    v_accrual_amount DECIMAL(15,2);
BEGIN
    SELECT COALESCE(SUM(allocated_amount), 0)
    INTO v_total_allocated
    FROM payment_allocations
    WHERE accrual_id = NEW.accrual_id;
    
    SELECT amount INTO v_accrual_amount
    FROM accruals
    WHERE accrual_id = NEW.accrual_id;
    
    UPDATE accruals
    SET status = CASE
        WHEN v_total_allocated >= v_accrual_amount THEN 'Оплачено'
        WHEN v_total_allocated > 0 THEN 'Частично оплачено'
        ELSE 'Не оплачено'
    END
    WHERE accrual_id = NEW.accrual_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_accrual_status
AFTER INSERT OR UPDATE ON payment_allocations
FOR EACH ROW
EXECUTE FUNCTION update_accrual_status_on_allocation();