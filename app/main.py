from cd import CD
from cd_crud import CDCrud
from welcome import (
    show_home_screen,
    interactive_menu,
    show_result,
    prompt_insert_cd_form,
    prompt_non_empty_text,
    prompt_id,
    prompt_edit_cd_form,
    prompt_remove_confirmation,
)

from store_crud import StoreCrud
store = StoreCrud()
import math
from rich.console import Console


crud = CDCrud()


def safe_input(message):
    try:
        return input(message)
    except EOFError:
        raise KeyboardInterrupt


def non_empty_input(message, max_length=None):
    while True:
        valor = safe_input(message).strip()

        if not valor:
            print("Esse campo não pode ser vazio.")
            continue

        if max_length is not None and len(valor) > max_length:
            print(f"Esse campo pode ter no máximo {max_length} caracteres.")
            continue

        return valor


def input_int(message, min_value=None, max_value=None):
    while True:
        try:
            valor = int(safe_input(message).strip())

            if min_value is not None and valor < min_value:
                print(f"O valor deve ser no mínimo {min_value}.")
                continue

            if max_value is not None and valor > max_value:
                print(f"O valor deve ser no máximo {max_value}.")
                continue

            return valor

        except ValueError:
            print("Entrada inválida. Deve ser um número inteiro.")

def input_forma_pagamento():
    while True:
        entrada = input("Forma de pagamento (1 - Cartão, 2 - Boleto): ").strip()

        if entrada not in ("1", "2"):
            print("[!] Opção inválida. Digite apenas 1 ou 2.")
            continue

        return int(entrada)
            
def quant_input_int(message, min_value=None, max_value=None):
    while True:
        try:
            valor = int(safe_input(message).strip())

            if min_value is not None and valor < min_value:
                print(f"O valor deve ser no mínimo {min_value}.")
                continue

            if max_value is not None and valor > max_value:
                print(f"Nossa loja tem o limite de {max_value} unidades por cd.")
                continue

            return valor

        except ValueError:
            print("Entrada inválida. Deve ser um número inteiro.")


def optional_quant_input_int(message, current_value, min_value=None, max_value=None):
    while True:
        entrada = safe_input(f"{message} [{current_value}] (Enter para manter): ").strip()

        if entrada == "":
            return current_value

        try:
            valor = int(entrada)

            if min_value is not None and valor < min_value:
                print(f"O valor deve ser no mínimo {min_value}.")
                continue

            if max_value is not None and valor > max_value:
                print(f"Nossa loja tem o limite de {max_value} unidades por cd.")
                continue

            return valor

        except ValueError:
            print("Entrada inválida. Deve ser um número inteiro.")

def input_float(message, min_value=None, max_value=None):
    while True:
        try:
            valor = float(safe_input(message).strip())

            if not math.isfinite(valor):
                print("Entrada inválida. Digite um número finito.")
                continue

            if min_value is not None and valor <= min_value:
                print(f"O valor deve ser maior que {min_value}.")
                continue

            if max_value is not None and valor > max_value:
                print(f"O valor deve ser no máximo {max_value}.")
                continue

            return valor

        except ValueError:
            print("Entrada inválida. Deve ser um número.")


def optional_text_input(message, current_value, max_length=None):
    while True:
        valor = safe_input(f"{message} [{current_value}] (Enter para manter): ").strip()

        if valor == "":
            return current_value

        if max_length is not None and len(valor) > max_length:
            print(f"Esse campo pode ter no máximo {max_length} caracteres.")
            continue

        return valor


def optional_int_input(message, current_value, min_value=None, max_value=None):
    while True:
        entrada = safe_input(f"{message} [{current_value}] (Enter para manter): ").strip()

        if entrada == "":
            return current_value

        try:
            valor = int(entrada)

            if min_value is not None and valor < min_value:
                print(f"O valor deve ser no mínimo {min_value}.")
                continue

            if max_value is not None and valor > max_value:
                print(f"O valor deve ser no máximo {max_value}.")
                continue

            return valor

        except ValueError:
            print("Entrada inválida. Deve ser um número inteiro.")

def optional_float_input(message, current_value, min_value=None, max_value=None):
    while True:
        entrada = safe_input(f"{message} [{current_value}] (Enter para manter): ").strip()

        if entrada == "":
            return current_value

        try:
            valor = float(entrada)

            if not math.isfinite(valor):
                print("Entrada inválida. Digite um número finito.")
                continue

            if min_value is not None and valor <= min_value:
                print(f"O valor deve ser maior que {min_value}.")
                continue

            if max_value is not None and valor > max_value:
                print(f"O valor deve ser no máximo {max_value}.")
                continue

            return valor

        except ValueError:
            print("Entrada inválida. Deve ser um número.")

def input_cliente_id_valido():
    while True:
        try:
            cliente_id = int(input("ID do cliente: "))
            dados = store.listar_dados_cliente(cliente_id)

            if not dados:
                print("[!] Cliente não encontrado. Tente novamente.")
                continue

            cliente = dados["cliente"]

            print("\n[✓] Cliente selecionado:")
            print(f"Nome: {cliente['nome']}")
            print(f"Email: {cliente['email']}")
            print(f"Cidade: {cliente['cidade']}\n")

            return cliente_id

        except ValueError:
            print("[!] Digite um número válido.")

def input_produto_id_valido():
    while True:
        try:
            produto_id = int(input("ID do produto: "))
            
            produto = store.get_produto_by_id(produto_id)

            if not produto:
                print("[!] Produto não encontrado. Tente novamente.")
                continue

            print("\n[✓] Produto selecionado:")
            print(f"Nome: {produto['nome']}")
            print(f"Artista: {produto['artista']}")
            print(f"Preço: R$ {produto['preco']}")
            print(f"Estoque: {produto['estoque']}\n")

            return produto_id

        except ValueError:
            print("[!] Digite um número válido.")

        except ValueError:
            print("[!] Digite um número válido.")

def input_vendedor_id_valido():
    while True:
        try:
            vendedor_id = int(input("ID do vendedor: "))
            vendedores = store.listar_vendedores()

            vendedor = next((v for v in vendedores if v["id"] == vendedor_id), None)

            if not vendedor:
                print("[!] Vendedor não encontrado.")
                continue

            if not vendedor["ativo"]:
                print("[!] Esse vendedor está inativo.")
                continue

            print("\n[✓] Vendedor selecionado:")
            print(f"Nome: {vendedor['nome']}\n")

            return vendedor_id

        except ValueError:
            print("[!] Digite um número válido.")

def format_cd(cd):
    return str(cd)


def format_cd_list(cds):
    if not cds:
        return "[!] O estoque está vazio. Nenhum CD cadastrado."

    return "\n\n".join(str(cd) for cd in cds)

def format_produto(p):
    return (
        f"[bold]{p['nome']}[/bold]\n"
        f"Artista: {p['artista']}\n"
        f"Categoria: {p['categoria']}\n"
        f"Ano: {p['ano_fabricacao']}\n"
        f"Preço: R$ {p['preco']}\n"
        f"Estoque: {p['estoque']}"
    )

def format_lista_produtos(produtos):
    if not produtos:
        return "[!] Nenhum produto encontrado."

    return "\n\n".join(format_produto(p) for p in produtos)

def format_pedido(p):
    return (
        f"[bold]Pedido #{p['compra_id']}[/bold]\n"
        f"Data: {p['data_compra']}\n"
        f"Cliente: {p['cliente_nome']}\n"
        f"Vendedor: {p['vendedor_nome']}\n"
        f"Produto: {p['produto_nome']} ({p['quantidade']}x)\n"
        f"Total: R$ {p['total']}\n"
        f"Status: {p['status_confirmacao']}"
    )

def format_lista_pedidos(pedidos):
    if not pedidos:
        return "[!] Nenhum pedido encontrado."

    return "\n\n".join(format_pedido(p) for p in pedidos)

def format_cliente(dados):
    cliente = dados["cliente"]
    compras = dados["compras"]

    texto = (
        f"[bold]{cliente['nome']}[/bold]\n"
        f"Email: {cliente['email']}\n"
        f"Cidade: {cliente['cidade']}\n\n"
        "[bold]Compras:[/bold]\n"
    )

    if not compras:
        texto += "Nenhuma compra."
    else:
        for c in compras:
            texto += (
                f"\n• ID {c['id']} | Total: R$ {c['total']} | Status: {c['status_confirmacao']}"
            )

    return texto

def format_relatorio(relatorio):
    if not relatorio:
        return "[!] Nenhum dado encontrado."

    return "\n\n".join(
        (
            f"[bold]{r['ano_mes']}[/bold]\n"
            f"Vendedor: {r['vendedor_nome']}\n"
            f"Pedidos: {r['total_pedidos']}\n"
            f"Total vendido: R$ {r['valor_total_vendido']}\n"
            f"Descontos: R$ {r['valor_total_descontos']}"
        )
        for r in relatorio
    )

try:
    if not show_home_screen():
        raise SystemExit

    while True:
        opcao = interactive_menu()

        if opcao == "Inserir CD":
            form_data = prompt_insert_cd_form()

            if form_data is None:
                show_result("Inserir CD", "Inserção cancelada.")
                continue

            cd = CD(
                form_data["titulo"],
                form_data["artista"],
                form_data["genero"],
                form_data["ano"],
                form_data["preco"],
                form_data["quantidade"],
            )
            crud.create(cd)

            show_result("Inserir CD", "CD inserido com sucesso!")

        elif opcao == "Alterar CD":
            id_cd = prompt_id("Alterar CD", "ID do CD a alterar:")
            if id_cd is None:
                show_result("Alterar CD", "Alteração cancelada.")
                continue

            cd_existente = crud.get_by_id(id_cd)

            if not cd_existente:
                show_result(
                    "Alterar CD",
                    f"[!] Não foi encontrado nenhum CD com o ID {id_cd}. Alteração cancelada."
                )
                continue

            novos_dados = prompt_edit_cd_form(cd_existente)
            if novos_dados is None:
                show_result("Alterar CD", "Alteração cancelada.")
                continue

            crud.update(
                id_cd,
                novos_dados["titulo"],
                novos_dados["artista"],
                novos_dados["genero"],
                novos_dados["ano"],
                novos_dados["preco"],
                novos_dados["quantidade"],
            )
            show_result("Alterar CD", "CD alterado com sucesso!")


        elif opcao == "Pesquisar CD por nome":
            nome = prompt_non_empty_text("Pesquisar CD por nome", "Digite o nome do CD:", 150)
            if nome is None:
                show_result("Pesquisar CD por nome", "Pesquisa cancelada.")
                continue

            resultados = crud.search_by_title(nome)

            if not resultados:
                show_result("Pesquisar CD por nome", f"[!] Nenhum CD encontrado com o título: '{nome}'")
            else:
                show_result(
                    "Pesquisar CD por nome",
                    format_cd_list(resultados)
                )

        elif opcao == "(NOVO)Buscar com filtros avançados":
            nome = input("Nome (opcional): ") or None
            preco_min = input("Preço mínimo: ")
            preco_max = input("Preço máximo: ")
            categoria = input("Categoria: ") or None
            baixo_estoque = input("Somente baixo estoque? (s/n): ").lower() == "s"

            resultados = store.buscar_produtos(
                nome=nome,
                preco_min=float(preco_min) if preco_min else None,
                preco_max=float(preco_max) if preco_max else None,
                categoria=categoria,
                somente_baixo_estoque=baixo_estoque
            )

            show_result(
                "Resultado da busca",
                format_lista_produtos(resultados)
            )

        elif opcao == "(NOVO) Realizar compra":

            cliente_id = input_cliente_id_valido()
            vendedor_id = input_vendedor_id_valido()
            forma_pagamento_id = input_forma_pagamento()
            produto_id = input_produto_id_valido()
            quantidade = int(input("Quantidade: "))

            produto = store.get_produto_by_id(produto_id)

            if not produto:
                show_result("Compra", "[bold red]Produto não encontrado![/bold red]")
                continue

            try:
                store.registrar_compra(
                    cliente_id,
                    vendedor_id,
                    forma_pagamento_id,
                    produto_id,
                    quantidade
                )

                total = produto["preco"] * quantidade

                resumo = (
                    f"[bold green]Compra realizada com sucesso![/bold green]\n\n"
                    f"[bold]{produto['nome']}[/bold]\n"
                    f"Artista: {produto['artista']}\n"
                    f"Quantidade: {quantidade}\n"
                    f"Preço unitário: R$ {produto['preco']}\n"
                    f"[bold]Total: R$ {total}[/bold]"
                )

                show_result("Resumo da Compra", resumo)

            except Exception as e:
                show_result("Erro", f"[bold red]{str(e)}[/bold red]")

        elif opcao == "(NOVO) Ver pedidos":
            pedidos = store.listar_pedidos_view()
            show_result(
                "Pedidos",
                format_lista_pedidos(pedidos)
            )

        elif opcao == "(NOVO) Histórico do cliente":
            cliente_id = int(input("ID do cliente: "))
            dados = store.listar_dados_cliente(cliente_id)

            if not dados:
                print("Cliente não encontrado")
            else:
                show_result(
                    "Histórico do Cliente",
                    format_cliente(dados)
                )
                        
        elif opcao == "(NOVO) Relatório mensal":
            relatorio = store.relatorio_vendas_mensais()

            show_result(
                "Relatório Mensal",
                format_relatorio(relatorio)
            )

        elif opcao == "Remover CD":
            id_cd = prompt_id("Remover CD", "ID do CD para remover:")
            if id_cd is None:
                show_result("Remover CD", "Remoção cancelada.")
                continue

            cd_existente = crud.get_by_id(id_cd)

            if not cd_existente:
                show_result(
                    "Remover CD",
                    f"[!] Não foi encontrado nenhum CD com o ID {id_cd}. Remoção cancelada."
                )
                continue

            confirm = prompt_remove_confirmation(cd_existente)
            if not confirm:
                show_result("Remover CD", "Remoção cancelada.")
                continue

            crud.delete(id_cd)
            show_result("Remover CD", f'CD "{cd_existente.titulo}" removido com sucesso!')

        elif opcao == "Listar todos":
            cds = crud.get_all()
            show_result("Lista de CDs", format_cd_list(cds))

        elif opcao == "Exibir CD":
            id_cd = prompt_id("Exibir CD", "Digite o ID do CD:")
            if id_cd is None:
                show_result("Exibir CD", "Operação cancelada.")
                continue

            cd = crud.get_by_id(id_cd)

            if not cd:
                show_result("Exibir CD", f"[!] Não foi encontrado nenhum CD com o ID {id_cd}.")
                continue

            show_result("Exibir CD", format_cd(cd))

        elif opcao == "Relatório de estoque":
            relatorio = crud.report()
            show_result("Relatório de estoque", relatorio)

        elif opcao == "Sair":
            break

except (KeyboardInterrupt, EOFError):
    console = Console()
    console.print("\n[!] Operação cancelada pelo usuário. Encerrando o programa.\n", style="#d16d9e")