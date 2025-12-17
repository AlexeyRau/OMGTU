SELECT 
    title,
    rating,
    rating_count,
    ts_rank(search_vector, plainto_tsquery('english', 'fantasy')) *
    (rating / 5) *
    (log(rating_count + 1) / log(4899965)) AS custom_rank
FROM books 
WHERE search_vector @@ plainto_tsquery('english', 'fantasy')
ORDER BY custom_rank DESC
LIMIT 20;