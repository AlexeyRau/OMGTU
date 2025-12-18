SELECT 
    s.service_name AS "Услуга",
    COUNT(a.accrual_id) AS "Кол-во начислений",
    SUM(a.consumption) AS "Общий расход, ед.",
    SUM(a.amount) AS "Общая сумма, руб.",
    ROUND(AVG(a.amount), 2) AS "Среднее начисление, руб.",
    ROUND(MAX(a.amount), 2) AS "Максимальное начисление, руб.",
    ROUND(MIN(a.amount), 2) AS "Минимальное начисление, руб."
FROM accruals a
JOIN contracts c ON a.contract_id = c.contract_id
JOIN services s ON c.service_id = s.service_id
WHERE EXTRACT(YEAR FROM a.period) = 2024
GROUP BY s.service_name
ORDER BY "Общая сумма, руб." DESC;