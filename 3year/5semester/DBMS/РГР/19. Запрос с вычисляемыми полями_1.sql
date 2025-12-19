SELECT
    accrual_id,
    contract_id,
    period,
    amount,
    status,
    CASE
        WHEN status != 'Оплачено' AND CURRENT_DATE > (period + INTERVAL '25 days')
        THEN ROUND((amount * 0.005 * EXTRACT(DAY FROM CURRENT_DATE - (period + INTERVAL '25 days')))::numeric, 2)
        ELSE 0
    END as penalty
FROM accruals;