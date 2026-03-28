-- Create users table
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  email VARCHAR(255)
);

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
  id SERIAL PRIMARY KEY,
  user_id INT,
  amount INT
);

-- Seed users (avoid duplicates)
INSERT INTO users (name, email)
VALUES ('Abhinav', 'abhinav@test.com');

-- Seed orders
INSERT INTO orders (user_id, amount) 
VALUES (1, 100)