SELECT title, description 
FROM books 
WHERE search_vector @@ phraseto_tsquery('english', 'Harry Potter Stone') 
LIMIT 10;