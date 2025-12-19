SELECT p.*, c.full_name
FROM payments p
JOIN clients c ON p.client_id = c.client_id
WHERE (p.payment_method = 'Карта' OR p.payment_method = 'Наличные')
  AND NOT p.amount < 500;