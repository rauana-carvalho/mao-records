USE mao_records;

DROP TABLE IF EXISTS cds;

CREATE TABLE cds (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    artista VARCHAR(150) NOT NULL,
    genero VARCHAR(100) NOT NULL,
    ano_lancamento INT NOT NULL CHECK (ano_lancamento >= 1982 AND ano_lancamento <= 2026),
    preco DECIMAL(10,2) NOT NULL CHECK (preco > 0 AND preco <= 1000000.99),
    quantidade INT NOT NULL CHECK (quantidade >= 0 AND quantidade <= 50)
);