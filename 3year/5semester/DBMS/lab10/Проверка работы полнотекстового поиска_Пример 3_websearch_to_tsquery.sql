SELECT title, description 
FROM books 
WHERE search_vector @@ websearch_to_tsquery('english', '"Harry Potter" -stone') 
LIMIT 20;