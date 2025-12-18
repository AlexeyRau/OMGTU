SELECT title, description 
FROM books 
WHERE search_vector @@ phraseto_tsquery('english', 'Harry Potter Time') 
LIMIT 10;