SELECT COUNT 
FROM books 
WHERE search_vector @@ plainto_tsquery('english', 'Harry Potter Stone') 
LIMIT 10;