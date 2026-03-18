from cd import CD
from cd_crud import CDCrud
from welcome import show_home_screen, interactive_menu, show_result
import math

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
            titulo = non_empty_input("Título: ", max_length=150)
            artista = non_empty_input("Artista: ", max_length=150)
            genero = non_empty_input("Gênero: ", max_length=100)
            ano = input_int("Ano de lançamento: ", min_value=1982, max_value=2026)
            preco = input_float("Preço: ", min_value=0, max_value=1000000.99)
            quantidade = quant_input_int("Quantidade: ", min_value=0, max_value=50)

            cd = CD(titulo, artista, genero, ano, preco, quantidade)
            crud.create(cd)

            show_result("Inserir CD", "CD inserido com sucesso!")

        elif opcao == "Alterar CD":
            id_cd = input_int("ID do CD a alterar: ", min_value=1)
            cd_existente = crud.get_by_id(id_cd)

            if not cd_existente:
                show_result(
                    "Alterar CD",
                    f"[!] Erro: Não foi encontrado nenhum CD com o ID {id_cd}. Alteração cancelada."
                )
                continue

            show_result("CD atual", str(cd_existente))

            titulo = optional_text_input("Novo título", cd_existente.titulo, max_length=150)
            artista = optional_text_input("Novo artista", cd_existente.artista, max_length=150)
            genero = optional_text_input("Novo gênero", cd_existente.genero, max_length=100)
            ano = optional_int_input("Novo ano", cd_existente.ano, min_value=1982, max_value=2026)
            preco = optional_float_input("Novo preço", cd_existente.preco, min_value=0, max_value=1000000.99)
            quantidade = optional_quant_input_int("Nova quantidade", cd_existente.quantidade, min_value=0, max_value=50)

            crud.update(id_cd, titulo, artista, genero, ano, preco, quantidade)
            show_result("Alterar CD", "CD alterado com sucesso!")

        elif opcao == "Pesquisar CD por nome":
            nome = non_empty_input("Digite o nome do CD: ", max_length=150)
            resultados = crud.search_by_title(nome)

            if not resultados:
                show_result("Pesquisar CD por nome", f"[!] Nenhum CD encontrado com o título: '{nome}'")
            else:
                show_result(
                    "Pesquisar CD por nome",
                    "\n\n".join(str(cd) for cd in resultados)
                )

        elif opcao == "Remover CD":
            id_cd = input_int("ID do CD para remover: ", min_value=1)
            cd_existente = crud.get_by_id(id_cd)

            if not cd_existente:
                show_result(
                    "Remover CD",
                    f"[!] Erro: Não foi encontrado nenhum CD com o ID {id_cd}. Remoção cancelada."
                )
                continue

            crud.delete(id_cd)
            show_result("Remover CD", f'CD "{cd_existente.titulo}" removido com sucesso!')

        elif opcao == "Listar todos":
            cds = crud.get_all()
            show_result("Lista de CDs", format_cd_list(cds))

        elif opcao == "Exibir CD":
            id_cd = input_int("Digite o ID do CD: ", min_value=1)
            cd = crud.get_by_id(id_cd)

            if cd:
                show_result("Exibir CD", format_cd(cd))
            else:
                show_result("Exibir CD", f"[!] CD com ID {id_cd} não encontrado.")

        elif opcao == "Relatório de estoque":
            relatorio = crud.report()
            show_result("Relatório de estoque", relatorio)

        elif opcao == "Sair":
            break

except (KeyboardInterrupt, EOFError):
    print("\n\nEncerrando sistema...\n")