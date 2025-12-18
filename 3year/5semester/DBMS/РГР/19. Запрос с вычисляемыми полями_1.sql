SELECT 
    cl.full_name AS "Клиент",
    COALESCE(SUM(CASE WHEN a.status != 'Оплачено' THEN a.amount ELSE 0 END), 0) 
        AS "Задолженность, руб.",
    COALESCE(SUM(CASE WHEN a.status = 'Оплачено' THEN a.amount ELSE 0 END), 0) 
        AS "Оплачено, руб.",
    COALESCE(SUM(p.amount), 0) AS "Всего платежей, руб.",
    COALESCE(SUM(p.amount), 0) - 
    COALESCE(SUM(CASE WHEN a.status = 'Оплачено' THEN a.amount ELSE 0 END), 0) 
        AS "Переплата/недоплата, руб."
FROM clients cl
LEFT JOIN contracts c ON cl.client_id = c.client_id
LEFT JOIN accruals a ON c.contract_id = a.contract_id
LEFT JOIN payments p ON cl.client_id = p.client_id
WHERE (a.period BETWEEN '2024-01-01' AND '2024-12-31' OR a.period IS NULL)
    AND (p.payment_date BETWEEN '2024-01-01' AND '2024-12-31' OR p.payment_date IS NULL)
GROUP BY cl.client_id, cl.full_name
HAVING COALESCE(SUM(a.amount), 0) > 0
    OR COALESCE(SUM(p.amount), 0) > 0
ORDER BY "Задолженность, руб." DESC, "Клиент";