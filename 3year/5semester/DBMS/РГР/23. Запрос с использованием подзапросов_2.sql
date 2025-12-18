SELECT 
    cl.client_id AS "ID клиента",
    cl.full_name AS "Клиент",
    cl.client_type AS "Тип",
    cl.contacts AS "Контакты",
    (SELECT COUNT(*) 
     FROM payments p 
     WHERE p.client_id = cl.client_id 
        AND EXTRACT(YEAR FROM p.payment_date) = 2024) AS "Кол-во платежей в 2024",
    (SELECT COALESCE(SUM(amount), 0)
     FROM payments p 
     WHERE p.client_id = cl.client_id 
        AND EXTRACT(YEAR FROM p.payment_date) = 2024) AS "Сумма платежей в 2024, руб.",
    (SELECT MAX(payment_date)
     FROM payments p 
     WHERE p.client_id = cl.client_id 
        AND EXTRACT(YEAR FROM p.payment_date) = 2024) AS "Дата последнего платежа"
FROM clients cl
WHERE cl.client_id IN (
    SELECT DISTINCT client_id 
    FROM payments 
    WHERE EXTRACT(YEAR FROM payment_date) = 2024
)
ORDER BY "Сумма платежей в 2024, руб." DESC;