SELECT 
    client_id,
    client_type AS "Тип клиента",
    full_name AS "Наименование",
    contacts AS "Контакты"
FROM clients
WHERE client_type = 'Юридическое лицо'
    OR contacts LIKE '%@%';