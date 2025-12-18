CREATE MATERIALIZED VIEW mv_client_payment_summary_2024 AS
SELECT 
    c.client_id,
    c.full_name,
    c.client_type,
    COUNT(DISTINCT p.payment_id) AS payments_count,
    SUM(p.amount) AS total_payments,
    MIN(p.payment_date) AS first_payment_date,
    MAX(p.payment_date) AS last_payment_date,
    ROUND(AVG(p.amount), 2) AS avg_payment_amount,
    STRING_AGG(DISTINCT p.payment_method, ', ') AS used_payment_methods
FROM clients c
LEFT JOIN payments p ON c.client_id = p.client_id
WHERE EXTRACT(YEAR FROM p.payment_date) = 2024
GROUP BY c.client_id, c.full_name, c.client_type
ORDER BY total_payments DESC NULLS LAST;

CREATE INDEX idx_mv_client_payments ON mv_client_payment_summary_2024(client_id);