SELECT
    payment_method,
    COUNT(*) as payment_count,
    SUM(amount) as total_amount
FROM payments
GROUP BY payment_method
ORDER BY total_amount DESC;