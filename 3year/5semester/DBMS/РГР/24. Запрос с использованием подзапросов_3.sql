SELECT 
    cl.full_name AS "Клиент",
    SUM(p.amount) AS "Общая сумма платежей, руб.",
    (SELECT MIN(amount) FROM payments WHERE client_id = 1) AS "Мин. платёж Иванова, руб.",
    (SELECT MAX(amount) FROM payments WHERE client_id = 1) AS "Макс. платёж Иванова, руб.",
    CASE 
        WHEN SUM(p.amount) > ANY (
            SELECT amount FROM payments WHERE client_id = 1
        ) THEN 'Выше некоторых платежей Иванова'
        WHEN SUM(p.amount) = ANY (
            SELECT amount FROM payments WHERE client_id = 1
        ) THEN 'Равен некоторым платежам Иванова'
        ELSE 'Ниже всех платежей Иванова'
    END AS "Сравнение с Ивановым"
FROM payments p
JOIN clients cl ON p.client_id = cl.client_id
WHERE p.client_id != 1
    AND EXTRACT(YEAR FROM p.payment_date) = 2024
GROUP BY cl.client_id, cl.full_name
HAVING SUM(p.amount) > 0
ORDER BY "Общая сумма платежей, руб." DESC;