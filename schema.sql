

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
    review TEXT
);


CREATE TABLE IF NOT EXISTS favourites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    book_id INTEGER REFERENCES books(id)
);


CREATE TABLE IF NOT EXISTS friends (
    id SERIAL PRIMARY KEY,
    user1 INTEGER REFERENCES users(id),
    user2 INTEGER REFERENCES users(id)
);

-- DROP TABLE friends;
-- DROP TABLE favourites;
-- DROP TABLE reviews;
-- DROP TABLE books;
-- DROP TABLE users;