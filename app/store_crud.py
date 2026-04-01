from decimal import Decimal
from typing import Any

from database import connect
from store_models import Cliente, Produto, Vendedor


class StoreCrud:
    def create_produto(self, produto: Produto) -> int:
        connection = connect()
        cursor = connection.cursor()

        try:
            sql = """
                INSERT INTO produtos
                    (nome, artista, categoria, tipo_midia, ano_fabricacao, fabricado_em_mari, preco, estoque)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                produto.nome,
                produto.artista,
                produto.categoria,
                produto.tipo_midia.value,
                produto.ano_fabricacao,
                produto.fabricado_em_mari,
                produto.preco,
                produto.estoque,
            )

            cursor.execute(sql, values)
            connection.commit()
            return cursor.lastrowid

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def create_cliente(self, cliente: Cliente) -> int:
        connection = connect()
        cursor = connection.cursor()

        try:
            sql = """
                INSERT INTO clientes
                    (nome, email, telefone, cidade, time_futebol, anime_favorito)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            values = (
                cliente.nome,
                cliente.email,
                cliente.telefone,
                cliente.cidade,
                cliente.time_futebol,
                cliente.anime_favorito,
            )

            cursor.execute(sql, values)
            connection.commit()
            return cursor.lastrowid

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def create_vendedor(self, vendedor: Vendedor) -> int:
        connection = connect()
        cursor = connection.cursor()

        try:
            sql = """
                INSERT INTO vendedores (nome, email, ativo)
                VALUES (%s, %s, %s)
            """
            values = (vendedor.nome, vendedor.email, vendedor.ativo)

            cursor.execute(sql, values)
            connection.commit()
            return cursor.lastrowid

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def listar_produtos(self) -> list[dict[str, Any]]:
        connection = connect()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT
                    id,
                    nome,
                    artista,
                    categoria,
                    tipo_midia,
                    ano_fabricacao,
                    fabricado_em_mari,
                    preco,
                    estoque
                FROM produtos
                ORDER BY nome ASC
                """
            )
            return cursor.fetchall()

        finally:
            cursor.close()
            connection.close()

    def get_produto_by_id(self, produto_id: int) -> dict[str, Any] | None:
        connection = connect()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT
                    id,
                    nome,
                    artista,
                    categoria,
                    tipo_midia,
                    ano_fabricacao,
                    fabricado_em_mari,
                    preco,
                    estoque
                FROM produtos
                WHERE id = %s
                """,
                (produto_id,),
            )
            return cursor.fetchone()

        finally:
            cursor.close()
            connection.close()

    def listar_clientes(self) -> list[dict[str, Any]]:
        connection = connect()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT
                    id,
                    nome,
                    email,
                    telefone,
                    cidade,
                    time_futebol,
                    anime_favorito
                FROM clientes
                ORDER BY nome ASC
                """
            )
            return cursor.fetchall()

        finally:
            cursor.close()
            connection.close()

    def get_cliente_by_id(self, cliente_id: int) -> dict[str, Any] | None:
        connection = connect()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM clientes WHERE id = %s", (cliente_id,))
            return cursor.fetchone()

        finally:
            cursor.close()
            connection.close()

    def listar_vendedores(self) -> list[dict[str, Any]]:
        connection = connect()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT
                    id,
                    nome,
                    email,
                    ativo
                FROM vendedores
                ORDER BY nome ASC
                """
            )
            return cursor.fetchall()

        finally:
            cursor.close()
            connection.close()

    def listar_formas_pagamento(self) -> list[dict[str, Any]]:
        connection = connect()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT
                    id,
                    nome,
                    exige_confirmacao
                FROM formas_pagamento
                ORDER BY id ASC
                """
            )
            return cursor.fetchall()

        finally:
            cursor.close()
            connection.close()

    def buscar_produtos(
        self,
        nome: str | None = None,
        preco_min: Decimal | None = None,
        preco_max: Decimal | None = None,
        categoria: str | None = None,
        tipo_midia: str | None = None,
        fabricado_em_mari: bool | None = None,
        somente_baixo_estoque: bool = False,
    ) -> list[dict[str, Any]]:
        connection = connect()
        cursor = connection.cursor(dictionary=True)

        try:
            conditions = []
            params: list[Any] = []

            if nome:
                conditions.append("nome LIKE %s")
                params.append(f"%{nome}%")

            if preco_min is not None:
                conditions.append("preco >= %s")
                params.append(preco_min)

            if preco_max is not None:
                conditions.append("preco <= %s")
                params.append(preco_max)

            if categoria:
                conditions.append("categoria = %s")
                params.append(categoria)

            if tipo_midia:
                conditions.append("tipo_midia = %s")
                params.append(tipo_midia)

            if fabricado_em_mari is not None:
                conditions.append("fabricado_em_mari = %s")
                params.append(fabricado_em_mari)

            if somente_baixo_estoque:
                conditions.append("estoque < 5")

            where_clause = ""
            if conditions:
                where_clause = "WHERE " + " AND ".join(conditions)

            sql = f"""
                SELECT
                    id,
                    nome,
                    artista,
                    categoria,
                    tipo_midia,
                    ano_fabricacao,
                    fabricado_em_mari,
                    preco,
                    estoque
                FROM produtos
                {where_clause}
                ORDER BY nome ASC
            """

            cursor.execute(sql, tuple(params))
            return cursor.fetchall()

        finally:
            cursor.close()
            connection.close()

    def listar_dados_cliente(self, cliente_id: int) -> dict[str, Any] | None:
        connection = connect()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM clientes WHERE id = %s", (cliente_id,))
            cliente = cursor.fetchone()

            if not cliente:
                return None

            cursor.execute(
                """
                SELECT
                    id,
                    created_at,
                    subtotal,
                    percentual_desconto,
                    valor_desconto,
                    total,
                    status_confirmacao
                FROM compras
                WHERE cliente_id = %s
                ORDER BY created_at DESC, id DESC
                """,
                (cliente_id,),
            )

            compras = cursor.fetchall()

            return {
                "cliente": cliente,
                "compras": compras,
            }

        finally:
            cursor.close()
            connection.close()

    def listar_pedidos_cliente(self, cliente_id: int) -> list[dict[str, Any]]:
        connection = connect()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT
                    compra_id,
                    data_compra,
                    cliente_nome,
                    cliente_email,
                    vendedor_nome,
                    forma_pagamento,
                    status_confirmacao,
                    produto_nome,
                    categoria,
                    quantidade,
                    preco_unitario,
                    total_item,
                    subtotal,
                    percentual_desconto,
                    valor_desconto,
                    total
                FROM vw_pedidos_detalhados
                WHERE cliente_id = %s
                ORDER BY data_compra DESC, compra_id DESC
                """,
                (cliente_id,),
            )
            return cursor.fetchall()

        finally:
            cursor.close()
            connection.close()

    def registrar_compra(
        self,
        cliente_id: int,
        vendedor_id: int,
        forma_pagamento_id: int,
        produto_id: int,
        quantidade: int,
        observacao: str | None = None,
    ) -> None:
        connection = connect()
        cursor = connection.cursor()

        try:
            cursor.callproc(
                "sp_registrar_compra",
                [
                    cliente_id,
                    vendedor_id,
                    forma_pagamento_id,
                    produto_id,
                    quantidade,
                    observacao,
                ],
            )
            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def listar_pedidos_view(self) -> list[dict[str, Any]]:
        connection = connect()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT *
                FROM vw_pedidos_detalhados
                ORDER BY data_compra DESC, compra_id DESC
                """
            )
            return cursor.fetchall()

        finally:
            cursor.close()
            connection.close()

    def relatorio_vendas_mensais(self) -> list[dict[str, Any]]:
        connection = connect()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT *
                FROM vw_vendas_mensais_por_vendedor
                ORDER BY ano_mes DESC, valor_total_vendido DESC
                """
            )
            return cursor.fetchall()

        finally:
            cursor.close()
            connection.close()