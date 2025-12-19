DROP TRIGGER IF EXISTS trg_update_accrual_status ON payment_allocations;
DROP FUNCTION IF EXISTS update_accrual_status();

CREATE OR REPLACE FUNCTION update_accrual_status()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF (
        SELECT a.amount <= COALESCE(SUM(pa.allocated_amount), 0)
        FROM accruals a
        LEFT JOIN payment_allocations pa ON a.accrual_id = pa.accrual_id
        WHERE a.accrual_id = COALESCE(NEW.accrual_id, OLD.accrual_id)
        GROUP BY a.accrual_id, a.amount
    ) THEN
        UPDATE accruals 
        SET status = 'Оплачено' 
        WHERE accrual_id = COALESCE(NEW.accrual_id, OLD.accrual_id);
    ELSE
        UPDATE accruals 
        SET status = 'Частично оплачено' 
        WHERE accrual_id = COALESCE(NEW.accrual_id, OLD.accrual_id)
        AND status != 'Оплачено';
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_update_accrual_status
AFTER INSERT OR UPDATE OF allocated_amount OR DELETE
ON payment_allocations
FOR EACH ROW
EXECUTE FUNCTION update_accrual_status();