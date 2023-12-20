DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT, 
    password TEXT,
    role INTEGER
);

CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users(id),
    message TEXT
);