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
                ORDER BY id ASC
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
                ORDER BY id ASC
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
                    cliente_id,
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

    def _get_cliente_desconto_percentual(self, cursor, cliente_id: int) -> Decimal:
        cursor.execute(
            """
            SELECT time_futebol, anime_favorito, cidade
            FROM clientes
            WHERE id = %s
            """,
            (cliente_id,),
        )
        cliente = cursor.fetchone()

        if not cliente:
            raise ValueError("Cliente nao encontrado.")

        percentual = Decimal("0.00")

        time_futebol = (cliente["time_futebol"] or "").strip().lower()
        anime_favorito = (cliente["anime_favorito"] or "").strip().lower()
        cidade = (cliente["cidade"] or "").strip().lower()

        if time_futebol == "flamengo":
            percentual += Decimal("10.00")

        if anime_favorito == "one piece":
            percentual += Decimal("5.00")

        if cidade == "sousa":
            percentual += Decimal("5.00")

        return min(percentual, Decimal("20.00"))

    def _get_status_confirmacao(self, cursor, forma_pagamento_id: int) -> str:
        cursor.execute(
            """
            SELECT exige_confirmacao
            FROM formas_pagamento
            WHERE id = %s
            """,
            (forma_pagamento_id,),
        )
        resultado = cursor.fetchone()

        if not resultado:
            raise ValueError("Forma de pagamento nao encontrada.")

        exige_confirmacao = bool(resultado["exige_confirmacao"])
        return "pendente" if exige_confirmacao else "dispensado"

    def registrar_compra(
        self,
        cliente_id: int,
        vendedor_id: int,
        forma_pagamento_id: int,
        itens: list[dict[str, int]],
        observacao: str | None = None,
    ) -> int:
        connection = connect()
        cursor = connection.cursor(dictionary=True)

        try:
            if not itens:
                raise ValueError("Adicione pelo menos um item à compra.")

            cursor.execute(
                """
                SELECT id, ativo
                FROM vendedores
                WHERE id = %s
                """,
                (vendedor_id,),
            )
            vendedor = cursor.fetchone()

            if not vendedor:
                raise ValueError("Vendedor nao encontrado.")

            if not vendedor["ativo"]:
                raise ValueError("O vendedor informado está inativo.")

            percentual_desconto = self._get_cliente_desconto_percentual(cursor, cliente_id)
            status_confirmacao = self._get_status_confirmacao(cursor, forma_pagamento_id)

            subtotal = Decimal("0.00")
            itens_processados: list[dict[str, Any]] = []

            for item in itens:
                produto_id = item["produto_id"]
                quantidade = item["quantidade"]

                if quantidade <= 0:
                    raise ValueError("Quantidade invalida para a compra.")

                cursor.execute(
                    """
                    SELECT id, nome, preco, estoque
                    FROM produtos
                    WHERE id = %s
                    """,
                    (produto_id,),
                )
                produto = cursor.fetchone()

                if not produto:
                    raise ValueError(f"Produto nao encontrado: ID {produto_id}.")

                if produto["estoque"] < quantidade:
                    raise ValueError(
                        f"Estoque insuficiente para o item '{produto['nome']}' (ID {produto_id})."
                    )

                preco_unitario = Decimal(str(produto["preco"]))
                total_item = preco_unitario * quantidade
                subtotal += total_item

                itens_processados.append(
                    {
                        "produto_id": produto_id,
                        "quantidade": quantidade,
                        "preco_unitario": preco_unitario,
                        "total_item": total_item,
                    }
                )

            valor_desconto = (subtotal * percentual_desconto / Decimal("100")).quantize(Decimal("0.01"))
            total = (subtotal - valor_desconto).quantize(Decimal("0.01"))

            cursor.execute(
                """
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
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    cliente_id,
                    vendedor_id,
                    forma_pagamento_id,
                    status_confirmacao,
                    subtotal,
                    percentual_desconto,
                    valor_desconto,
                    total,
                    observacao,
                ),
            )
            compra_id = cursor.lastrowid

            for item in itens_processados:
                cursor.execute(
                    """
                    INSERT INTO itens_compra (
                        compra_id,
                        produto_id,
                        quantidade,
                        preco_unitario,
                        total_item
                    ) VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        compra_id,
                        item["produto_id"],
                        item["quantidade"],
                        item["preco_unitario"],
                        item["total_item"],
                    ),
                )

                cursor.execute(
                    """
                    UPDATE produtos
                    SET estoque = estoque - %s
                    WHERE id = %s
                    """,
                    (item["quantidade"], item["produto_id"]),
                )

            connection.commit()
            return compra_id

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