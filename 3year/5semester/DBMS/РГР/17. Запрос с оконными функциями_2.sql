SELECT 
    c.contract_number AS "Номер договора",
    a.period AS "Период",
    a.amount AS "Сумма начисления",
    SUM(a.amount) OVER (
        PARTITION BY c.contract_id 
        ORDER BY a.period
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS "Накопительная сумма",
    AVG(a.amount) OVER (PARTITION BY c.contract_id) AS "Среднее начисление"
FROM accruals a
JOIN contracts c ON a.contract_id = c.contract_id
WHERE EXTRACT(YEAR FROM a.period) = 2024
ORDER BY c.contract_number, a.period;