GRANT ALL PRIVILEGES ON DATABASE production TO postgres1;

-- User table
CREATE TABLE IF NOT EXISTS users (
  userid SERIAL PRIMARY KEY,
  username VARCHAR NOT NULL,
  password VARCHAR NOT NULL,
  dateCreated timestamp DEFAULT current_timestamp,
  UNIQUE (username)
);

-- Favourites table
CREATE TABLE IF NOT EXISTS userFavourites (
  id SERIAL PRIMARY KEY,
  userId INTEGER REFERENCES users(userid),
  ticker VARCHAR,
  dateAdded timestamp DEFAULT current_timestamp
  UNIQUE (userId,ticker)
);