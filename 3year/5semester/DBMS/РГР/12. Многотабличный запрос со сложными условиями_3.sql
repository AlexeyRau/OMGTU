SELECT 
    s.service_name AS "Услуга",
    t.start_date AS "Начало действия",
    t.end_date AS "Окончание",
    t.rate AS "Ставка, руб./ед.",
    (t.end_date - t.start_date + 1) AS "Дней действия"
FROM tariffs t
JOIN services s ON t.service_id = s.service_id
WHERE t.start_date <= '2024-12-31'
    AND t.end_date >= '2024-01-01'
ORDER BY s.service_name, t.start_date;