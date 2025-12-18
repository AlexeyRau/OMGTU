SELECT 
    contract_id AS "ID договора",
    contract_number AS "Номер договора",
    start_date AS "Дата начала",
    end_date AS "Дата окончания"
FROM contracts
WHERE start_date BETWEEN '2023-01-01' AND '2023-12-31'
    AND status = 'Активен'
    AND service_id NOT IN (
        SELECT service_id 
        FROM services 
        WHERE service_name = 'Газоснабжение'
    );