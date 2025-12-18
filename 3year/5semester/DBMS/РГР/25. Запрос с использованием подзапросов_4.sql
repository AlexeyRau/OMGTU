SELECT 
    c.contract_number AS "Номер договора",
    cl.full_name AS "Клиент",
    s.service_name AS "Услуга",
    c.start_date AS "Дата начала",
    c.status AS "Статус договора",
    (SELECT COUNT(*) 
     FROM accruals a 
     WHERE a.contract_id = c.contract_id 
        AND a.status != 'Оплачено'
        AND EXTRACT(YEAR FROM a.period) = 2024) AS "Кол-во неоплаченных",
    (SELECT COALESCE(SUM(amount), 0)
     FROM accruals a 
     WHERE a.contract_id = c.contract_id 
        AND a.status != 'Оплачено'
        AND EXTRACT(YEAR FROM a.period) = 2024) AS "Сумма задолженности, руб.",
    (SELECT MAX(period)
     FROM accruals a 
     WHERE a.contract_id = c.contract_id 
        AND a.status != 'Оплачено') AS "Период самой старой задолженности"
FROM contracts c
JOIN clients cl ON c.client_id = cl.client_id
JOIN services s ON c.service_id = s.service_id
WHERE EXISTS (
    SELECT 1
    FROM accruals a
    WHERE a.contract_id = c.contract_id
        AND a.status != 'Оплачено'
        AND EXTRACT(YEAR FROM a.period) = 2024
)
ORDER BY "Сумма задолженности, руб." DESC, "Клиент";