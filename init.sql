
\c production

-- User table
CREATE TABLE IF NOT EXISTS users (
  userid SERIAL PRIMARY KEY,
  username VARCHAR,
  password VARCHAR,
  dateCreated DATE,
  UNIQUE(username)
);

-- Favourites table
CREATE TABLE IF NOT EXISTS userFavourites (
  id SERIAL PRIMARY KEY,
  userId INTEGER REFERENCES users(userid),
  ticker VARCHAR,
  date DATE DEFAULT CURRENT_DATE
);