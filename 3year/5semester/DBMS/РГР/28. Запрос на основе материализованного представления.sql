SELECT *
FROM mv_client_balance
WHERE current_balance > 0
ORDER BY current_balance DESC;