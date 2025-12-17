CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    isbn TEXT,
    title TEXT,
    description TEXT,
    year INTEGER,
    rating FLOAT,
    rating_count INTEGER,
    pages INTEGER,
    authors INTEGER[]
);