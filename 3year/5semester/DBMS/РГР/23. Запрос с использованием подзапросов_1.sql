SELECT 
    c.contract_number AS "Номер договора",
    cl.full_name AS "Клиент",
    s.service_name AS "Услуга",
    COUNT(a.accrual_id) AS "Кол-во начислений",
    SUM(a.amount) AS "Общая сумма, руб.",
    ROUND(AVG(a.amount), 2) AS "Среднее начисление, руб.",
    ROUND(SUM(a.amount) / NULLIF(SUM(a.consumption), 0), 2) AS "Средний тариф, руб./ед."
FROM contracts c
JOIN clients cl ON c.client_id = cl.client_id
JOIN services s ON c.service_id = s.service_id
JOIN accruals a ON c.contract_id = a.contract_id
WHERE c.contract_id IN (
    SELECT contract_id
    FROM accruals
    WHERE EXTRACT(YEAR FROM period) = 2024
    GROUP BY contract_id
    HAVING SUM(amount) > (
        SELECT AVG(total_amount)
        FROM (
            SELECT SUM(amount) AS total_amount
            FROM accruals
            WHERE EXTRACT(YEAR FROM period) = 2024
            GROUP BY contract_id
        ) AS contract_totals
    )
)
GROUP BY c.contract_id, c.contract_number, cl.full_name, s.service_name
ORDER BY "Общая сумма, руб." DESC;