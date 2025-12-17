SELECT 
    title,
    ts_headline('english', description, plainto_tsquery('english', 'magic'), 'StartSel=->, StopSel=<-, MaxWords=30') AS snippet
FROM books 
WHERE search_vector @@ plainto_tsquery('english', 'magic')
LIMIT 10;