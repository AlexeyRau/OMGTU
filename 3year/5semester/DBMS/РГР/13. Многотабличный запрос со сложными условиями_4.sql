SELECT 
    contract_number AS "Номер договора",
    start_date AS "Дата начала",
    end_date AS "Дата окончания",
    status AS "Статус"
FROM contracts
WHERE start_date NOT BETWEEN '2023-01-01' AND '2023-12-31'
ORDER BY start_date;