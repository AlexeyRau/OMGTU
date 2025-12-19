SELECT *
FROM mv_contract_summary
WHERE contract_balance > 0
ORDER BY contract_balance DESC;