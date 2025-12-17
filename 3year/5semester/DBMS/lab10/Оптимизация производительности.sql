EXPLAIN ANALYZE 
SELECT title, ts_rank(search_vector, plainto_tsquery('english', 'Harry Potter')) AS rank
FROM books 
WHERE search_vector @@ plainto_tsquery('english', 'Harry Potter')
ORDER BY rank DESC
LIMIT 10;