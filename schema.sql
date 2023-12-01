

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



