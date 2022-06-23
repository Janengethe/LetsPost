-- prepares a MySQL database with sample data in database


CREATE DATABASE IF NOT EXISTS post_dev_db;
USE post_dev_db;
GRANT ALL PRIVILEGES ON post_dev_db TO 'root'@'localhost';
USE performance_schema;
GRANT SELECT ON performance_schema.* TO 'root'@'localhost';
FLUSH PRIVILEGES;

USE post_dev_db;
DROP TABLE IF EXISTS lpost;
DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users
(
       id INT UNIQUE NOT NULL AUTO_INCREMENT PRIMARY KEY,
       password VARCHAR(255) NOT NULL,
       email VARCHAR(255) NOT NULL
);
INSERT INTO users
    (id, password, email)
VALUES
    (0, "not_hashed_sample", "sample@gmail.com");

CREATE TABLE IF NOT EXISTS lpost
(
       id INT UNIQUE NOT NULL AUTO_INCREMENT PRIMARY KEY,
       title VARCHAR(12) NOT NULL,
       ingridients VARCHAR(1000) NOT NULL,
       recipe VARCHAR(1000) NOT NULL,
       user_id INT, 
       FOREIGN KEY(user_id) REFERENCES users(id)
);
INSERT INTO lpost
(id, title, ingridients, recipe, user_id)
VALUES
(0, "Cake", "wheat flour, sugar, butter, oil", "Stir all to mix. Put on oven", 0);