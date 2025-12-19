DROP MATERIALIZED VIEW IF EXISTS mv_client_balance;

CREATE MATERIALIZED VIEW mv_client_balance AS
SELECT
    c.client_id,
    c.full_name,
    c.client_type,
    COALESCE(SUM(a.amount), 0) as total_accrued,
    COALESCE(SUM(p.amount), 0) as total_paid,
    (COALESCE(SUM(a.amount), 0) - COALESCE(SUM(p.amount), 0)) as current_balance
FROM clients c
LEFT JOIN contracts cntr ON c.client_id = cntr.client_id
LEFT JOIN accruals a ON cntr.contract_id = a.contract_id
LEFT JOIN payments p ON c.client_id = p.client_id
GROUP BY c.client_id, c.full_name, c.client_type;