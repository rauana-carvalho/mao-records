from decimal import Decimal, InvalidOperation

from rich.console import Console

from store_crud import StoreCrud
from store_models import Cliente, Produto, Vendedor, TipoMidia
from welcome import (
    interactive_menu,
    prompt_busca_produtos_form,
    prompt_cliente_form,
    prompt_cliente_id,
    prompt_compra_form,
    prompt_produto_form,
    prompt_vendedor_form,
    show_home_screen,
    show_result,
)

console = Console()
crud = StoreCrud()


def to_decimal(value):
    if value is None or value == "":
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def format_database_error(error):
    message = str(error)

    if "chk_vendedor_email" in message:
        return "O e-mail do vendedor é inválido. Digite um e-mail com @."

    if "chk_cliente_email" in message:
        return "O e-mail do cliente é inválido. Digite um e-mail com @."

    if "chk_vendedor_nome" in message:
        return "O nome do vendedor precisa ter pelo menos 3 caracteres."

    if "chk_cliente_nome" in message:
        return "O nome do cliente precisa ter pelo menos 3 caracteres."

    if "chk_cliente_telefone" in message:
        return "O telefone do cliente é inválido. Digite pelo menos 8 caracteres."

    if "chk_produto_nome" in message:
        return "O título do álbum não pode estar vazio."

    if "chk_produto_artista" in message:
        return "O artista do item musical não pode estar vazio."

    if "chk_produto_categoria" in message:
        return "A categoria musical não pode estar vazia."

    if "chk_produto_ano" in message:
        return "O ano de fabricação do item musical é inválido."

    if "chk_produto_preco" in message:
        return "O preço do item musical precisa ser maior que zero."

    if "chk_produto_estoque" in message:
        return "O estoque do item musical não pode ser negativo."

    if message == "'tipo_midia'":
        return "O filtro de tipo de mídia ainda não foi integrado corretamente no formulário de busca."

    if "Duplicate entry" in message and "clientes.email" in message:
        return "Já existe um cliente cadastrado com esse e-mail."

    if "Duplicate entry" in message and "vendedores.email" in message:
        return "Já existe um vendedor cadastrado com esse e-mail."

    if "Duplicate entry" in message and "for key 'clientes.email'" in message:
        return "Já existe um cliente cadastrado com esse e-mail."

    if "Duplicate entry" in message and "for key 'vendedores.email'" in message:
        return "Já existe um vendedor cadastrado com esse e-mail."

    if "Estoque insuficiente" in message:
        return "Não há estoque suficiente para efetivar a compra."

    if "Cliente nao encontrado" in message:
        return "Cliente não encontrado."

    if "Produto nao encontrado" in message:
        return "Item musical não encontrado."

    if "Forma de pagamento nao encontrada" in message:
        return "Forma de pagamento não encontrada."

    if "Vendedor nao encontrado" in message:
        return "Vendedor não encontrado."

    if "inativo" in message:
        return "O vendedor informado está inativo."

    if "Adicione pelo menos um item" in message:
        return "Adicione pelo menos um item à compra."

    if "Quantidade invalida" in message:
        return "A quantidade da compra precisa ser maior que zero."

    if "Unknown column 'cliente_id' in 'where clause'" in message:
        return "A visualização de pedidos está desatualizada no banco. Atualize a view 'vw_pedidos_detalhados'."

    return f"Ocorreu um erro no banco de dados:\n{message}"


def format_item_musical(produto):
    fabricado_em_mari = "Sim" if produto["fabricado_em_mari"] else "Não"

    return (
        f"ID: {produto['id']}\n"
        f"Título do álbum: {produto['nome']}\n"
        f"Artista: {produto['artista']}\n"
        f"Categoria musical: {produto['categoria']}\n"
        f"Tipo de mídia: {produto['tipo_midia']}\n"
        f"Ano de fabricação: {produto['ano_fabricacao']}\n"
        f"Fabricado em Mari: {fabricado_em_mari}\n"
        f"Preço: R$ {produto['preco']}\n"
        f"Estoque: {produto['estoque']}"
    )


def format_lista_itens_musicais(produtos):
    if not produtos:
        return "[!] Nenhum item musical encontrado."

    return "\n\n".join(format_item_musical(produto) for produto in produtos)


def format_cliente_detalhado(dados):
    cliente = dados["cliente"]
    compras = dados["compras"]

    info_cliente = (
        f"[bold]Cliente[/bold]\n"
        f"ID: {cliente['id']}\n"
        f"Nome: {cliente['nome']}\n"
        f"E-mail: {cliente['email']}\n"
        f"Telefone: {cliente['telefone']}\n"
        f"Cidade: {cliente['cidade']}\n"
        f"Time de futebol: {cliente['time_futebol']}\n"
        f"Anime favorito: {cliente['anime_favorito']}"
    )

    if not compras:
        return info_cliente + "\n\n[bold]Pedidos[/bold]\nNenhum pedido encontrado para este cliente."

    pedidos = []
    for compra in compras:
        pedidos.append(
            f"Pedido #{compra['id']} | Data: {compra['created_at']} | "
            f"Subtotal: R$ {compra['subtotal']} | "
            f"Desconto: {compra['percentual_desconto']}% | "
            f"Total: R$ {compra['total']} | "
            f"Status: {compra['status_confirmacao']}"
        )

    return info_cliente + "\n\n[bold]Pedidos[/bold]\n" + "\n".join(pedidos)


def format_relatorio_vendas(relatorio):
    if not relatorio:
        return "[!] Nenhum dado encontrado no relatório mensal."

    linhas = []
    for item in relatorio:
        linhas.append(
            f"Mês: {item['ano_mes']}\n"
            f"Vendedor ID: {item['vendedor_id']}\n"
            f"Vendedor: {item['vendedor_nome']}\n"
            f"Total de pedidos: {item['total_pedidos']}\n"
            f"Valor total vendido: R$ {item['valor_total_vendido']}\n"
            f"Valor total em descontos: R$ {item['valor_total_descontos']}"
        )

    return "\n\n".join(linhas)


def main():
    try:
        if not show_home_screen():
            return

        while True:
            opcao = interactive_menu()

            if opcao == "Cadastrar item musical":
                dados = prompt_produto_form()
                if dados is None:
                    show_result("Cadastrar item musical", "Operação cancelada.")
                    continue

                try:
                    produto = Produto(
                        nome=dados["titulo_album"],
                        artista=dados["artista"],
                        categoria=dados["categoria"],
                        tipo_midia=TipoMidia(dados["tipo_midia"]),
                        ano_fabricacao=dados["ano_fabricacao"],
                        fabricado_em_mari=dados["fabricado_em_mari"],
                        preco=Decimal(str(dados["preco"])),
                        estoque=dados["estoque"],
                    )

                    produto_id = crud.create_produto(produto)
                    show_result(
                        "Cadastrar item musical",
                        f"Item musical cadastrado com sucesso!\nID gerado: {produto_id}",
                    )
                except Exception as error:
                    show_result("Cadastrar item musical", f"[!] {format_database_error(error)}")

            elif opcao == "Cadastrar cliente":
                dados = prompt_cliente_form()
                if dados is None:
                    show_result("Cadastrar cliente", "Operação cancelada.")
                    continue

                try:
                    cliente = Cliente(
                        nome=dados["nome"],
                        email=dados["email"],
                        telefone=dados["telefone"],
                        cidade=dados["cidade"],
                        time_futebol=dados["time_futebol"],
                        anime_favorito=dados["anime_favorito"],
                    )

                    cliente_id = crud.create_cliente(cliente)
                    show_result(
                        "Cadastrar cliente",
                        f"Cliente cadastrado com sucesso!\nID gerado: {cliente_id}",
                    )
                except Exception as error:
                    show_result("Cadastrar cliente", f"[!] {format_database_error(error)}")

            elif opcao == "Cadastrar vendedor":
                dados = prompt_vendedor_form()
                if dados is None:
                    show_result("Cadastrar vendedor", "Operação cancelada.")
                    continue

                try:
                    vendedor = Vendedor(
                        nome=dados["nome"],
                        email=dados["email"],
                        ativo=dados["ativo"],
                    )

                    vendedor_id = crud.create_vendedor(vendedor)
                    show_result(
                        "Cadastrar vendedor",
                        f"Vendedor cadastrado com sucesso!\nID gerado: {vendedor_id}",
                    )
                except Exception as error:
                    show_result("Cadastrar vendedor", f"[!] {format_database_error(error)}")

            elif opcao == "Buscar itens musicais":
                filtros = prompt_busca_produtos_form()
                if filtros is None:
                    show_result("Buscar itens musicais", "Operação cancelada.")
                    continue

                try:
                    resultados = crud.buscar_produtos(
                        nome=filtros["titulo_album"],
                        preco_min=to_decimal(filtros["preco_min"]),
                        preco_max=to_decimal(filtros["preco_max"]),
                        categoria=filtros["categoria"],
                        tipo_midia=filtros["tipo_midia"],
                        fabricado_em_mari=filtros["fabricado_em_mari"],
                        somente_baixo_estoque=filtros["somente_baixo_estoque"],
                    )

                    show_result("Buscar itens musicais", format_lista_itens_musicais(resultados))
                except Exception as error:
                    show_result("Buscar itens musicais", f"[!] {format_database_error(error)}")

            elif opcao == "Listar itens musicais":
                try:
                    produtos = crud.listar_produtos()
                    show_result("Listar itens musicais", format_lista_itens_musicais(produtos))
                except Exception as error:
                    show_result("Listar itens musicais", f"[!] {format_database_error(error)}")

            elif opcao == "Realizar compra":
                dados = prompt_compra_form()
                if dados is None:
                    show_result("Realizar compra", "Operação cancelada.")
                    continue

                try:
                    cliente_id = dados.get("cliente_id")

                    if cliente_id is None:
                        cliente = Cliente(
                            nome=dados["cliente"]["nome"],
                            email=dados["cliente"]["email"],
                            telefone=dados["cliente"]["telefone"],
                            cidade=dados["cliente"]["cidade"],
                            time_futebol=dados["cliente"]["time_futebol"],
                            anime_favorito=dados["cliente"]["anime_favorito"],
                        )
                        cliente_id = crud.create_cliente(cliente)

                    compra_id = crud.registrar_compra(
                        cliente_id=cliente_id,
                        vendedor_id=dados["vendedor_id"],
                        forma_pagamento_id=dados["forma_pagamento_id"],
                        itens=dados["itens"],
                        observacao=dados["observacao"],
                    )

                    show_result(
                        "Realizar compra",
                        f"Compra registrada com sucesso!\nID da compra: {compra_id}",
                    )
                except Exception as error:
                    show_result("Realizar compra", f"[!] {format_database_error(error)}")

            elif opcao == "Ver dados do cliente":
                cliente_id = prompt_cliente_id("Ver dados do cliente")
                if cliente_id is None:
                    show_result("Ver dados do cliente", "Operação cancelada.")
                    continue

                try:
                    dados_cliente = crud.listar_dados_cliente(cliente_id)
                    if not dados_cliente:
                        show_result(
                            "Ver dados do cliente",
                            f"[!] Nenhum cliente encontrado com o ID {cliente_id}.",
                        )
                        continue

                    show_result("Ver dados do cliente", format_cliente_detalhado(dados_cliente))
                except Exception as error:
                    show_result("Ver dados do cliente", f"[!] {format_database_error(error)}")

            elif opcao == "Ver pedidos do cliente":
                cliente_id = prompt_cliente_id("Ver pedidos do cliente")
                if cliente_id is None:
                    show_result("Ver pedidos do cliente", "Operação cancelada.")
                    continue

                try:
                    pedidos = crud.listar_pedidos_cliente(cliente_id)
                    if not pedidos:
                        show_result(
                            "Ver pedidos do cliente",
                            "Nenhum pedido encontrado para esse cliente.",
                        )
                        continue

                    pedidos = crud.listar_pedidos_cliente(cliente_id)

                    if not pedidos:
                        show_result("Ver pedidos do cliente", "Nenhum pedido encontrado para este cliente.")
                        continue

                    linhas = []
                    pedido_atual = None

                    for pedido in pedidos:
                        if pedido_atual != pedido["compra_id"]:
                            if linhas:
                                linhas.append("")

                            linhas.append(f"Pedido #{pedido['compra_id']}")
                            linhas.append(f"Data: {pedido['data_compra']}")
                            linhas.append(f"Forma de pagamento: {pedido['forma_pagamento']}")
                            linhas.append(f"Status: {pedido['status_confirmacao']}")
                            linhas.append("Itens:")

                            pedido_atual = pedido["compra_id"]

                        linhas.append(
                            f"- {pedido['produto_nome']} | Categoria: {pedido['categoria']} | "
                            f"Qtd: {pedido['quantidade']} | Preço unit.: R$ {pedido['preco_unitario']} | "
                            f"Total item: R$ {pedido['total_item']}"
                        )

                    show_result("Ver pedidos do cliente", "\n".join(linhas))
                except Exception as error:
                    show_result("Ver pedidos do cliente", f"[!] {format_database_error(error)}")

            elif opcao == "Relatório mensal por vendedor":
                try:
                    relatorio = crud.relatorio_vendas_mensais()
                    show_result(
                        "Relatório mensal por vendedor",
                        format_relatorio_vendas(relatorio),
                    )
                except Exception as error:
                    show_result("Relatório mensal por vendedor", f"[!] {format_database_error(error)}")

            elif opcao == "Sair":
                break

    except (KeyboardInterrupt, EOFError):
        console.print(
            "\n[!] Operação cancelada pelo usuário. Encerrando o programa.\n",
            style="#d16d9e",
        )
    except Exception as error:
        show_result("Erro", f"[!] {format_database_error(error)}")


if __name__ == "__main__":
    main()
