DO $$
DECLARE
    cur_rec RECORD;
    cur_cursor CURSOR FOR
        SELECT 
            c.full_name,
            c.contacts,
            a.accrual_id,
            a.period,
            a.amount
        FROM accruals a
        JOIN contracts cntr ON a.contract_id = cntr.contract_id
        JOIN clients c ON cntr.client_id = c.client_id
        WHERE a.status != 'Оплачено'
        AND a.period < CURRENT_DATE - INTERVAL '30 days'
        ORDER BY a.period;
BEGIN
    OPEN cur_cursor;
    LOOP
        FETCH cur_cursor INTO cur_rec;
        EXIT WHEN NOT FOUND;
        RAISE NOTICE 'Клиент: %, Контакты: %, Начисление ID: %, Период: %, Сумма: % руб.',
            cur_rec.full_name,
            cur_rec.contacts,
            cur_rec.accrual_id,
            cur_rec.period,
            cur_rec.amount;
    END LOOP;
    CLOSE cur_cursor;
END $$;