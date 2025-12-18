DO $$
DECLARE
    cur_contracts CURSOR FOR
        SELECT 
            c.contract_number,
            cl.full_name,
            SUM(a.amount) AS total_debt
        FROM contracts c
        JOIN clients cl ON c.client_id = cl.client_id
        LEFT JOIN accruals a ON c.contract_id = a.contract_id
        WHERE a.status IN ('Не оплачено', 'Частично оплачено')
        GROUP BY c.contract_id, cl.full_name
        HAVING SUM(a.amount) > 0;
    
    rec RECORD;
BEGIN
    OPEN cur_contracts;
    LOOP
        FETCH cur_contracts INTO rec;
        EXIT WHEN NOT FOUND;
        RAISE NOTICE 'Договор: %, Клиент: %, Задолженность: % руб.', 
            rec.contract_number, rec.full_name, rec.total_debt;
    END LOOP;
    CLOSE cur_contracts;
END $$;