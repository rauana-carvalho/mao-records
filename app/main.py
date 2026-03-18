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


def format_cd(cd):
    return str(cd)


def format_cd_list(cds):
    if not cds:
        return "[!] O estoque está vazio. Nenhum CD cadastrado."

    return "\n\n".join(str(cd) for cd in cds)


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