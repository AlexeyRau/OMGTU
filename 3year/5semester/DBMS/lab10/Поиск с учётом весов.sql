SELECT 
    title,
    ts_rank(weighted_vector, plainto_tsquery('english', 'Harry Potter')) AS rank
FROM books 
WHERE weighted_vector @@ plainto_tsquery('english', 'Harry Potter')
ORDER BY rank DESC
LIMIT 20;