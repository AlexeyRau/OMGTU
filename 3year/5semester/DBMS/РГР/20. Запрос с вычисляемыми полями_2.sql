SELECT 
    s.service_name AS "Услуга",
    s.unit AS "Единица измерения",
    COUNT(DISTINCT a.contract_id) AS "Кол-во договоров",
    COUNT(a.accrual_id) AS "Кол-во начислений",
    ROUND(AVG(a.consumption), 3) AS "Средний расход",
    MAX(a.consumption) AS "Максимальный расход",
    MIN(a.consumption) AS "Минимальный расход",
    ROUND(STDDEV(a.consumption), 3) AS "Стандартное отклонение",
    ROUND(AVG(a.amount), 2) AS "Средняя сумма",
    SUM(a.amount) AS "Общая сумма начислений"
FROM accruals a
JOIN contracts c ON a.contract_id = c.contract_id
JOIN services s ON c.service_id = s.service_id
WHERE EXTRACT(YEAR FROM a.period) = 2024
    AND a.consumption > 0
GROUP BY s.service_id, s.service_name, s.unit
ORDER BY "Общая сумма начислений" DESC;