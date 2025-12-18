SELECT 
    p.payment_id AS "ID платежа",
    cl.full_name AS "Плательщик",
    p.payment_date AS "Дата платежа",
    p.amount AS "Сумма",
    p.payment_method AS "Способ оплаты"
FROM payments p
JOIN clients cl ON p.client_id = cl.client_id
WHERE (p.payment_method = 'Карта' OR p.payment_method = 'Наличные')
    AND p.payment_date BETWEEN '2024-01-01' AND '2024-03-31'
    AND p.payment_method NOT IN ('Банковский перевод')
ORDER BY p.payment_date DESC;