SELECT
    c.client_type,
    c.full_name,
    COALESCE(SUM(a.amount), 0) as total_accrued_2024,
    COALESCE(SUM(p.amount), 0) as total_paid_2024,
    (COALESCE(SUM(a.amount), 0) - COALESCE(SUM(p.amount), 0)) as debt_2024
FROM clients c
LEFT JOIN contracts cntr ON c.client_id = cntr.client_id
LEFT JOIN accruals a ON cntr.contract_id = a.contract_id AND EXTRACT(YEAR FROM a.period) = 2024
LEFT JOIN payments p ON c.client_id = p.client_id AND EXTRACT(YEAR FROM p.payment_date) = 2024
GROUP BY c.client_id, c.client_type, c.full_name
HAVING (COALESCE(SUM(a.amount), 0) - COALESCE(SUM(p.amount), 0)) > 0
ORDER BY c.client_type, debt_2024 DESC, c.full_name;