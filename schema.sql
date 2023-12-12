
DROP TABLE friends;
DROP TABLE favourites;
DROP TABLE reviews;
DROP TABLE books;
DROP TABLE users;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);


CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    bookname TEXT,
    author TEXT,
    year INTEGER
);


CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    book_id INTEGER REFERENCES books(id),
    name TEXT,
    status TEXT,
    grade INTEGER,
    review TEXT,
    review_date DATE
);


CREATE TABLE IF NOT EXISTS favourites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    book_id INTEGER REFERENCES books(id)
);


CREATE TABLE IF NOT EXISTS friends (
    id SERIAL PRIMARY KEY,
    user1 TEXT REFERENCES users(username),
    user2 TEXT REFERENCES users(username)
);

ALTER TABLE reviews
ADD CONSTRAINT user_book_unique_constraint UNIQUE (user_id, book_id);

INSERT INTO books (bookname, author, year) VALUES
    ('To Kill a Mockingbird', 'Harper Lee', 1960),
    ('1984', 'George Orwell', 1949),
    ('The Great Gatsby', 'F. Scott Fitzgerald', 1925),
    ('The Catcher in the Rye', 'J.D. Salinger', 1951),
    ('The Lord of the Rings', 'J.R.R. Tolkien', 1954),
    ('Pride and Prejudice', 'Jane Austen', 1813),
    ('The Hobbit', 'J.R.R. Tolkien', 1937),
    ('Harry Potter and the Sorcerer''s Stone', 'J.K. Rowling', 1997),
    ('To Kill a Mockingbird', 'Harper Lee', 1960),
    ('Animal Farm', 'George Orwell', 1945),
    ('The Chronicles of Narnia', 'C.S. Lewis', 1950),
    ('The Da Vinci Code', 'Dan Brown', 2003),
    ('The Shining', 'Stephen King', 1977),
    ('The Hitchhiker''s Guide to the Galaxy', 'Douglas Adams', 1979),
    ('The Grapes of Wrath', 'John Steinbeck', 1939);

