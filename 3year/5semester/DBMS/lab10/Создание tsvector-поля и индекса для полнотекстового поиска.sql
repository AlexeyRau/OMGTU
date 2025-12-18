ALTER TABLE books
ADD COLUMN search_vector tsvector 
GENERATED ALWAYS AS (
    to_tsvector('english', coalesce(title, '') || ' ' || coalesce(description, ''))
) STORED;

CREATE INDEX search_vector_idx ON books USING GIN (search_vector);