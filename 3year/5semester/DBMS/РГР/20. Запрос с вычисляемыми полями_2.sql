SELECT
    c.client_id,
    c.full_name,
    c.client_type,
    COALESCE(SUM(p.amount), 0) as total_paid,
    CASE
        WHEN COALESCE(SUM(p.amount), 0) < 1000 THEN 'Малый'
        WHEN COALESCE(SUM(p.amount), 0) BETWEEN 1000 AND 5000 THEN 'Средний'
        ELSE 'Крупный'
    END as payment_category
FROM clients c
LEFT JOIN payments p ON c.client_id = p.client_id
GROUP BY c.client_id, c.full_name, c.client_type;