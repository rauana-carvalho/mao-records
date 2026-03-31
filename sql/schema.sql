CREATE DATABASE IF NOT EXISTS mao_records;
USE mao_records;

SET FOREIGN_KEY_CHECKS = 0;
DROP VIEW IF EXISTS vw_pedidos_detalhados;
DROP VIEW IF EXISTS vw_vendas_mensais_por_vendedor;
DROP TABLE IF EXISTS itens_compra;
DROP TABLE IF EXISTS compras;
DROP TABLE IF EXISTS produtos;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS vendedores;
DROP TABLE IF EXISTS formas_pagamento;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    telefone VARCHAR(20) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    time_futebol VARCHAR(50) NOT NULL,
    anime_favorito VARCHAR(100) NOT NULL,
    CONSTRAINT chk_cliente_nome CHECK (CHAR_LENGTH(TRIM(nome)) >= 3),
    CONSTRAINT chk_cliente_email CHECK (email LIKE '%@%'),
    CONSTRAINT chk_cliente_telefone CHECK (CHAR_LENGTH(TRIM(telefone)) >= 8)
);

CREATE TABLE vendedores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT chk_vendedor_nome CHECK (CHAR_LENGTH(TRIM(nome)) >= 3),
    CONSTRAINT chk_vendedor_email CHECK (email LIKE '%@%')
);

CREATE TABLE formas_pagamento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(20) NOT NULL UNIQUE,
    exige_confirmacao BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT chk_forma_pagamento_nome CHECK (
        nome IN ('cartao', 'boleto', 'pix', 'berries', 'dinheiro')
    )
);

CREATE TABLE produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    artista VARCHAR(150) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    tipo_midia ENUM('CD', 'DVD', 'VINYL', 'CASSETE') NOT NULL,
    ano_fabricacao INT NOT NULL,
    fabricado_em_mari BOOLEAN NOT NULL DEFAULT FALSE,
    preco DECIMAL(10,2) NOT NULL,
    estoque INT NOT NULL
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT chk_produto_nome CHECK (CHAR_LENGTH(TRIM(nome)) >= 1),
    CONSTRAINT chk_produto_artista CHECK (CHAR_LENGTH(TRIM(artista)) >= 1),
    CONSTRAINT chk_produto_categoria CHECK (CHAR_LENGTH(TRIM(categoria)) >= 1),
    CONSTRAINT chk_produto_ano CHECK (ano_fabricacao BETWEEN 1900 AND 2026),
    CONSTRAINT chk_produto_preco CHECK (preco > 0 AND preco <= 1000000.99),
    CONSTRAINT chk_produto_estoque CHECK (estoque >= 0 AND estoque <= 10000)
);

CREATE TABLE compras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    vendedor_id INT NOT NULL,
    forma_pagamento_id INT NOT NULL,
    status_confirmacao ENUM('pendente', 'confirmado', 'dispensado', 'cancelado') NOT NULL DEFAULT 'dispensado',
    subtotal DECIMAL(10,2) NOT NULL DEFAULT 0,
    percentual_desconto DECIMAL(5,2) NOT NULL DEFAULT 0,
    valor_desconto DECIMAL(10,2) NOT NULL DEFAULT 0,
    total DECIMAL(10,2) NOT NULL DEFAULT 0,
    observacao VARCHAR(255) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_compras_cliente
        FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    CONSTRAINT fk_compras_vendedor
        FOREIGN KEY (vendedor_id) REFERENCES vendedores(id),
    CONSTRAINT fk_compras_forma_pagamento
        FOREIGN KEY (forma_pagamento_id) REFERENCES formas_pagamento(id),
    CONSTRAINT chk_compra_subtotal CHECK (subtotal >= 0),
    CONSTRAINT chk_compra_percentual_desconto CHECK (percentual_desconto >= 0 AND percentual_desconto <= 100),
    CONSTRAINT chk_compra_valor_desconto CHECK (valor_desconto >= 0),
    CONSTRAINT chk_compra_total CHECK (total >= 0)
);

CREATE TABLE itens_compra (
    id INT AUTO_INCREMENT PRIMARY KEY,
    compra_id INT NOT NULL,
    produto_id INT NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,
    total_item DECIMAL(10,2) NOT NULL,
    CONSTRAINT fk_itens_compra_compra
        FOREIGN KEY (compra_id) REFERENCES compras(id) ON DELETE CASCADE,
    CONSTRAINT fk_itens_compra_produto
        FOREIGN KEY (produto_id) REFERENCES produtos(id),
    CONSTRAINT chk_item_quantidade CHECK (quantidade > 0),
    CONSTRAINT chk_item_preco_unitario CHECK (preco_unitario > 0),
    CONSTRAINT chk_item_total CHECK (total_item > 0)
);

CREATE INDEX idx_produtos_nome ON produtos(nome);
CREATE INDEX idx_produtos_categoria ON produtos(categoria);
CREATE INDEX idx_produtos_preco ON produtos(preco);
CREATE INDEX idx_produtos_mari_estoque ON produtos(fabricado_em_mari, estoque);
CREATE INDEX idx_clientes_cidade ON clientes(cidade);
CREATE INDEX idx_compras_cliente_data ON compras(cliente_id, created_at);
CREATE INDEX idx_compras_vendedor_data ON compras(vendedor_id, created_at);
CREATE INDEX idx_itens_compra_compra ON itens_compra(compra_id);
CREATE INDEX idx_itens_compra_produto ON itens_compra(produto_id);

INSERT INTO formas_pagamento (nome, exige_confirmacao) VALUES
('cartao', TRUE),
('boleto', TRUE),
('pix', TRUE),
('berries', TRUE),
('dinheiro', FALSE);

INSERT INTO vendedores (nome, email) VALUES
('Rauana Carvalho', 'rauana@maorecords.com'),
('Luis Gomes', 'luis@maorecords.com'),
('Romulo Alves', 'romulo@maorecords.com');

INSERT INTO clientes (nome, email, telefone, cidade, time_futebol, anime_favorito) VALUES
('Ana Sousa', 'ana@email.com', '83999990001', 'Sousa', 'Flamengo', 'One Piece'),
('Maria Lima', 'maria@email.com', '83999990002', 'Joao Pessoa', 'Botafogo', 'Naruto'),
('Joao Pedro', 'joao@email.com', '83999990003', 'Campina Grande', 'Flamengo', 'Bleach');

INSERT INTO produtos (nome, artista, categoria, ano_fabricacao, fabricado_em_mari, preco, estoque) VALUES
('Thriller', 'Michael Jackson', 'Pop', 1982, FALSE, 129.90, 10),
('Back in Black', 'AC/DC', 'Rock', 1980, TRUE, 99.90, 4),
('The Dark Side of the Moon', 'Pink Floyd', 'Rock Progressivo', 1973, FALSE, 149.90, 7),
('Hybrid Theory', 'Linkin Park', 'Nu Metal', 2000, TRUE, 89.90, 3),
('Random Access Memories', 'Daft Punk', 'Eletronica', 2013, FALSE, 119.90, 12);

CREATE OR REPLACE VIEW vw_pedidos_detalhados AS
SELECT
    c.id AS compra_id,
    c.created_at AS data_compra,
    cl.nome AS cliente_nome,
    cl.email AS cliente_email,
    v.nome AS vendedor_nome,
    fp.nome AS forma_pagamento,
    c.status_confirmacao,
    p.nome AS produto_nome,
    p.categoria,
    ic.quantidade,
    ic.preco_unitario,
    ic.total_item,
    c.subtotal,
    c.percentual_desconto,
    c.valor_desconto,
    c.total
FROM compras c
INNER JOIN clientes cl ON cl.id = c.cliente_id
INNER JOIN vendedores v ON v.id = c.vendedor_id
INNER JOIN formas_pagamento fp ON fp.id = c.forma_pagamento_id
INNER JOIN itens_compra ic ON ic.compra_id = c.id
INNER JOIN produtos p ON p.id = ic.produto_id;

CREATE OR REPLACE VIEW vw_vendas_mensais_por_vendedor AS
SELECT
    DATE_FORMAT(c.created_at, '%Y-%m') AS ano_mes,
    v.id AS vendedor_id,
    v.nome AS vendedor_nome,
    COUNT(DISTINCT c.id) AS total_pedidos,
    SUM(c.total) AS valor_total_vendido,
    SUM(c.valor_desconto) AS valor_total_descontos
FROM compras c
INNER JOIN vendedores v ON v.id = c.vendedor_id
WHERE c.status_confirmacao IN ('confirmado', 'dispensado')
GROUP BY DATE_FORMAT(c.created_at, '%Y-%m'), v.id, v.nome;

DELIMITER $$

CREATE PROCEDURE sp_registrar_compra (
    IN p_cliente_id INT,
    IN p_vendedor_id INT,
    IN p_forma_pagamento_id INT,
    IN p_produto_id INT,
    IN p_quantidade INT,
    IN p_observacao VARCHAR(255)
)
BEGIN
    DECLARE v_preco DECIMAL(10,2);
    DECLARE v_estoque INT;
    DECLARE v_subtotal DECIMAL(10,2);
    DECLARE v_percentual_desconto DECIMAL(5,2) DEFAULT 0;
    DECLARE v_valor_desconto DECIMAL(10,2) DEFAULT 0;
    DECLARE v_total DECIMAL(10,2);
    DECLARE v_exige_confirmacao BOOLEAN;
    DECLARE v_status_confirmacao VARCHAR(20);
    DECLARE v_time_futebol VARCHAR(50);
    DECLARE v_anime_favorito VARCHAR(100);
    DECLARE v_cidade VARCHAR(100);
    DECLARE v_compra_id INT;

    IF p_quantidade IS NULL OR p_quantidade <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Quantidade invalida para a compra.';
    END IF;

    SELECT preco, estoque
    INTO v_preco, v_estoque
    FROM produtos
    WHERE id = p_produto_id;

    IF v_preco IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Produto nao encontrado.';
    END IF;

    IF v_estoque < p_quantidade THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Estoque insuficiente para efetivar a compra.';
    END IF;

    SELECT time_futebol, anime_favorito, cidade
    INTO v_time_futebol, v_anime_favorito, v_cidade
    FROM clientes
    WHERE id = p_cliente_id;

    IF v_time_futebol IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cliente nao encontrado.';
    END IF;

    SELECT exige_confirmacao
    INTO v_exige_confirmacao
    FROM formas_pagamento
    WHERE id = p_forma_pagamento_id;

    IF v_exige_confirmacao IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Forma de pagamento nao encontrada.';
    END IF;

    SET v_subtotal = v_preco * p_quantidade;

    IF LOWER(v_time_futebol) = 'flamengo' THEN
        SET v_percentual_desconto = v_percentual_desconto + 10;
    END IF;

    IF LOWER(v_anime_favorito) = 'one piece' THEN
        SET v_percentual_desconto = v_percentual_desconto + 5;
    END IF;

    IF LOWER(v_cidade) = 'sousa' THEN
        SET v_percentual_desconto = v_percentual_desconto + 5;
    END IF;

    IF v_percentual_desconto > 20 THEN
        SET v_percentual_desconto = 20;
    END IF;

    SET v_valor_desconto = ROUND(v_subtotal * (v_percentual_desconto / 100), 2);
    SET v_total = ROUND(v_subtotal - v_valor_desconto, 2);

    IF v_exige_confirmacao THEN
        SET v_status_confirmacao = 'pendente';
    ELSE
        SET v_status_confirmacao = 'dispensado';
    END IF;

    START TRANSACTION;

    INSERT INTO compras (
        cliente_id,
        vendedor_id,
        forma_pagamento_id,
        status_confirmacao,
        subtotal,
        percentual_desconto,
        valor_desconto,
        total,
        observacao
    ) VALUES (
        p_cliente_id,
        p_vendedor_id,
        p_forma_pagamento_id,
        v_status_confirmacao,
        v_subtotal,
        v_percentual_desconto,
        v_valor_desconto,
        v_total,
        p_observacao
    );

    SET v_compra_id = LAST_INSERT_ID();

    INSERT INTO itens_compra (
        compra_id,
        produto_id,
        quantidade,
        preco_unitario,
        total_item
    ) VALUES (
        v_compra_id,
        p_produto_id,
        p_quantidade,
        v_preco,
        v_subtotal
    );

    UPDATE produtos
    SET estoque = estoque - p_quantidade
    WHERE id = p_produto_id;

    COMMIT;
END$$

DELIMITER ;
