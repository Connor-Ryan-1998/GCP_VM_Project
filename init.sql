-- DROP DATABASE IF EXISTS production;

-- CREATE DATABASE production;
\c production;

CREATE postgres WITH password postgres;
GRANT ALL PRIVILEGES ON DATABASE production TO postgres;

-- User table
CREATE TABLE IF NOT EXISTS [production].[public].users (
  userid SERIAL PRIMARY KEY,
  username VARCHAR NOT NULL,
  password VARCHAR NOT NULL,
  dateCreated timestamp DEFAULT current_timestamp,
  UNIQUE (username)
);

-- Favourites table
CREATE TABLE IF NOT EXISTS [production].[public].userFavourites (
  id SERIAL PRIMARY KEY,
  userId INTEGER REFERENCES users(userid),
  ticker VARCHAR,
  dateAdded timestamp DEFAULT current_timestamp
  UNIQUE (userId,ticker)
);