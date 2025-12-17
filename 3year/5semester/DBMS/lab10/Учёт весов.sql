ALTER TABLE books 
ADD COLUMN weighted_vector tsvector 
GENERATED ALWAYS AS (
    setweight(to_tsvector('english', coalesce(title, '')), 'A') || 
    setweight(to_tsvector('english', coalesce(description, '')), 'B')
) STORED;

CREATE INDEX weighted_vector_idx ON books USING GIN (weighted_vector);