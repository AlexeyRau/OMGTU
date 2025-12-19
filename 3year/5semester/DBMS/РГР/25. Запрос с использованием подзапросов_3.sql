SELECT cntr.contract_id, cntr.contract_number, SUM(a.amount) as total_accrued
FROM contracts cntr
JOIN accruals a ON cntr.contract_id = a.contract_id
GROUP BY cntr.contract_id, cntr.contract_number
HAVING SUM(a.amount) > ANY (
    SELECT amount FROM accruals WHERE contract_id = 1
)
AND SUM(a.amount) > ALL (
    SELECT amount FROM accruals WHERE contract_id = 2
);