CREATE DATABASE IF NOT EXISTS mao_records;
USE mao_records;

DROP TABLE IF EXISTS cds;

CREATE TABLE IF NOT EXISTS cds (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    artista VARCHAR(150) NOT NULL,
    genero VARCHAR(100) NOT NULL,
    ano_lancamento INT NOT NULL,
    preco DECIMAL(10,2) NOT NULL CHECK (preco >= 0),
    quantidade INT NOT NULL CHECK (quantidade >= 0)
);