SELECT c.full_name, SUM(p.amount) as total_paid
FROM clients c
JOIN payments p ON c.client_id = p.client_id
GROUP BY c.client_id, c.full_name
HAVING SUM(p.amount) > (SELECT AVG(amount) FROM payments);