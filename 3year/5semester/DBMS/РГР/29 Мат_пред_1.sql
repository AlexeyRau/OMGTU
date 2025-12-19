DROP MATERIALIZED VIEW IF EXISTS mv_contract_summary;

CREATE MATERIALIZED VIEW mv_contract_summary AS
SELECT
    cntr.contract_id,
    cntr.contract_number,
    c.full_name AS client_name,
    c.client_type,
    s.service_name,
    cntr.start_date,
    cntr.end_date,
    cntr.status AS contract_status,
    COALESCE(SUM(a.amount), 0) AS total_accrued,
    COALESCE(SUM(pa.allocated_amount), 0) AS total_paid,
    (COALESCE(SUM(a.amount), 0) - COALESCE(SUM(pa.allocated_amount), 0)) AS contract_balance
FROM contracts cntr
JOIN clients c ON cntr.client_id = c.client_id
JOIN services s ON cntr.service_id = s.service_id
LEFT JOIN accruals a ON cntr.contract_id = a.contract_id
LEFT JOIN payment_allocations pa ON a.accrual_id = pa.accrual_id
GROUP BY cntr.contract_id, cntr.contract_number, c.full_name, c.client_type,
         s.service_name, cntr.start_date, cntr.end_date, cntr.status;