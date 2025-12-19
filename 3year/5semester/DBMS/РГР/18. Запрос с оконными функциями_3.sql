SELECT
    DATE_TRUNC('month', payment_date) as month,
    SUM(amount) as monthly_total,
    to_char((AVG(SUM(amount)) OVER (ORDER BY DATE_TRUNC('month', payment_date) ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)), '9999999990.00') as moving_avg_3m
FROM payments
GROUP BY DATE_TRUNC('month', payment_date)
ORDER BY month;