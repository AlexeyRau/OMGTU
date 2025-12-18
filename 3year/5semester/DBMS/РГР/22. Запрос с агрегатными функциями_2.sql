SELECT 
    cl.client_type AS "Тип клиента",
    TO_CHAR(p.payment_date, 'YYYY-MM') AS "Период",
    p.payment_method AS "Способ оплаты",
    COUNT(p.payment_id) AS "Кол-во платежей",
    SUM(p.amount) AS "Сумма платежей, руб.",
    ROUND(AVG(p.amount), 2) AS "Средний платёж, руб.",
    ROUND(MAX(p.amount), 2) AS "Максимальный платёж, руб.",
    ROUND(MIN(p.amount), 2) AS "Минимальный платёж, руб."
FROM payments p
JOIN clients cl ON p.client_id = cl.client_id
WHERE EXTRACT(YEAR FROM p.payment_date) = 2024
    AND p.amount > 0
GROUP BY cl.client_type, TO_CHAR(p.payment_date, 'YYYY-MM'), p.payment_method
HAVING COUNT(p.payment_id) >= 1
    AND SUM(p.amount) > 1000
ORDER BY 
    CASE WHEN cl.client_type = 'Юридическое лицо' THEN 1 ELSE 2 END,
    "Период" ASC,
    "Сумма платежей, руб." DESC,
    p.payment_method;