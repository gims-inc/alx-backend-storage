-- Create Table users
-- Desc
--    id, integer, never null, auto increment and primary key
--    email, string (255 characters), never null and unique
--   name, string (255 characters)
-- if table already exists, your script should not fail
-- script can be executed on any database
DROP TABLE IF EXISTS users;
CREATE TABLE users(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
	)