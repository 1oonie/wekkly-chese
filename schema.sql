DROP TABLE IF EXISTS articles;

CREATE TABLE articles (
    url_name TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    content TEXT NOT NULL
);

DROP TABLE IF EXISTS tba;

CREATE TABLE tba (
    url_name TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    content TEXT NOT NULL
);