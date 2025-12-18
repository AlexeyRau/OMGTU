SELECT 
    cl.full_name AS "Клиент",
    cl.client_type AS "Тип",
    SUM(p.amount) AS "Всего оплачено, руб.",
    RANK() OVER (ORDER BY SUM(p.amount) DESC) AS "Место в рейтинге",
    ROUND(SUM(p.amount) * 100.0 / SUM(SUM(p.amount)) OVER (), 2) AS "Доля от общей суммы, %"
FROM payments p
JOIN clients cl ON p.client_id = cl.client_id
WHERE EXTRACT(YEAR FROM p.payment_date) = 2024
GROUP BY cl.client_id, cl.full_name, cl.client_type
ORDER BY "Всего оплачено, руб." DESC;