USE IFPEBPT;

CREATE TABLE IF NOT EXISTS paciente(
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(120) NOT NULL,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    sex TINYINT NOT NULL,
    redo INT NOT NULL,
    cpb INT NOT NULL, 
    age INT NOT NULL,
    bsa FLOAT NOT NULL,
    hb FLOAT NOT NULL,
    probability FLOAT,
    prediction FLOAT,
    imagem TEXT
);