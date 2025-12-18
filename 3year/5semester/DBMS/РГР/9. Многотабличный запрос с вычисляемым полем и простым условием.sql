SELECT 
    cl.full_name AS "Клиент",
    s.service_name AS "Услуга",
    co.contract_number AS "Номер договора",
    ac.period AS "Период",
    ac.consumption AS "Расход, ед.",
    ac.amount AS "Сумма, руб.",
    ROUND(ac.amount / NULLIF(ac.consumption, 0), 2) AS "Тариф, руб./ед."
FROM accruals ac
JOIN contracts co ON ac.contract_id = co.contract_id
JOIN clients cl ON co.client_id = cl.client_id
JOIN services s ON co.service_id = s.service_id
WHERE ac.period = '2024-01-01'
    AND ac.consumption > 0
ORDER BY cl.full_name, s.service_name;