CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  surname VARCHAR(255),
  phone VARCHAR(30) UNIQUE,
  email VARCHAR(255) UNIQUE,
  hashed_password TEXT
);
