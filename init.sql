DROP DATABASE IF EXISTS production;

CREATE DATABASE production;

\c production;

-- User table
CREATE TABLE IF NOT EXISTS dbo.user (
  userid SERIAL PRIMARY KEY,
  username VARCHAR,
  password VARCHAR
);

-- Favourites table
CREATE TABLE IF NOT EXISTS dbo.userFavourites (
  id SERIAL PRIMARY KEY,
  userId INTEGER REFERENCES dbo.user(userid),
  tocker VARCHAR,
  fromDate DATE,
  toDate DATE,
  image VARCHAR,
  date DATE DEFAULT CURRENT_DATE
);