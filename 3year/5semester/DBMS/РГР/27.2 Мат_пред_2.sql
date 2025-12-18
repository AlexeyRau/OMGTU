CREATE MATERIALIZED VIEW mv_accruals_with_tariffs AS
SELECT 
    a.accrual_id,
    a.contract_id,
    a.period,
    a.consumption,
    a.amount,
    a.status,
    a.created_date,
    c.contract_number,
    s.service_name,
    t.rate AS tariff_rate,
    t.start_date AS tariff_start,
    t.end_date AS tariff_end
FROM accruals a
JOIN contracts c ON a.contract_id = c.contract_id
JOIN services s ON c.service_id = s.service_id
LEFT JOIN tariffs t ON s.service_id = t.service_id
    AND a.period BETWEEN t.start_date AND t.end_date
ORDER BY a.period DESC, a.contract_id;

CREATE INDEX idx_mv_accruals_period ON mv_accruals_with_tariffs(period);
CREATE INDEX idx_mv_accruals_status ON mv_accruals_with_tariffs(status);