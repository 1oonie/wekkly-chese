DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    password_hash TEXT NOT NULL
);

DROP TABLE IF EXISTS articles;

CREATE TABLE articles (
    url_name TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    content TEXT NOT NULL
);