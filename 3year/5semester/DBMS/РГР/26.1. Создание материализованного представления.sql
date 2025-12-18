DROP MATERIALIZED VIEW IF EXISTS mv_client_financial_status;

CREATE MATERIALIZED VIEW mv_client_financial_status AS
SELECT 
    cl.client_id,
    cl.full_name AS "Клиент",
    cl.client_type AS "Тип",
    
    COALESCE(SUM(CASE 
        WHEN a.status IN ('Не оплачено', 'Частично оплачено') 
        AND EXTRACT(YEAR FROM a.period) = 2024 
        THEN a.amount ELSE 0 
    END), 0) AS "Текущая задолженность",
    
    COALESCE(SUM(CASE 
        WHEN a.status = 'Оплачено' 
        AND EXTRACT(YEAR FROM a.period) = 2024 
        THEN a.amount ELSE 0 
    END), 0) AS "Оплачено в 2024",
    
    COALESCE(SUM(CASE 
        WHEN EXTRACT(YEAR FROM p.payment_date) = 2024 
        THEN p.amount ELSE 0 
    END), 0) AS "Всего внесено в 2024",
    
    COALESCE(SUM(CASE 
        WHEN EXTRACT(YEAR FROM p.payment_date) = 2024 
        THEN p.amount ELSE 0 
    END), 0) - 
    COALESCE(SUM(CASE 
        WHEN a.status = 'Оплачено' 
        AND EXTRACT(YEAR FROM a.period) = 2024 
        THEN a.amount ELSE 0 
    END), 0) AS "Сальдо",
    
    CASE 
        WHEN COALESCE(SUM(CASE 
                WHEN a.status IN ('Не оплачено', 'Частично оплачено') 
                AND EXTRACT(YEAR FROM a.period) = 2024 
                THEN a.amount ELSE 0 
            END), 0) > 0 
            THEN 'Есть задолженность'
        WHEN COALESCE(SUM(CASE 
                WHEN EXTRACT(YEAR FROM p.payment_date) = 2024 
                THEN p.amount ELSE 0 
            END), 0) - 
            COALESCE(SUM(CASE 
                WHEN a.status = 'Оплачено' 
                AND EXTRACT(YEAR FROM a.period) = 2024 
                THEN a.amount ELSE 0 
            END), 0) > 0 
            THEN 'Переплата'
        ELSE 'Баланс'
    END AS "Финансовый статус"
    
FROM clients cl
LEFT JOIN contracts c ON cl.client_id = c.client_id
LEFT JOIN accruals a ON c.contract_id = a.contract_id
LEFT JOIN payments p ON cl.client_id = p.client_id
GROUP BY cl.client_id, cl.full_name, cl.client_type;

CREATE INDEX idx_mv_cfs_client ON mv_client_financial_status("Клиент");