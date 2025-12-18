SELECT 
    client_id AS "ID клиента",
    full_name AS "ФИО",
    identity_doc AS "Документ",
    contacts AS "Контакты"
FROM clients 
WHERE client_type = 'Физическое лицо'
ORDER BY full_name;