
SELECT 'CREATE DATABASE production'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'production')\gexec

\c production;

BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles  -- SELECT list can be empty for this
      WHERE  rolname = 'postgres') THEN

      CREATE ROLE my_user WITH PASSWORD postgres;
   END IF;
END

GRANT ALL PRIVILEGES ON DATABASE production TO postgres;

-- User table
CREATE TABLE IF NOT EXISTS [public].users (
  userid SERIAL PRIMARY KEY,
  username VARCHAR NOT NULL,
  password VARCHAR NOT NULL,
  dateCreated timestamp DEFAULT current_timestamp,
  UNIQUE (username)
);

-- Favourites table
CREATE TABLE IF NOT EXISTS [public].userFavourites (
  id SERIAL PRIMARY KEY,
  userId INTEGER REFERENCES users(userid),
  ticker VARCHAR,
  dateAdded timestamp DEFAULT current_timestamp
  UNIQUE (userId,ticker)
);