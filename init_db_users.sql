USE IFPEBPT;

CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100),
    matricula VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255)
);
