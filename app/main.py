from cd import CD
from cd_crud import CDCrud
from welcome import show_home_screen, interactive_menu, show_result

crud = CDCrud()

def input_int(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Entrada inválida. Deve ser um número inteiro.")

def input_float(message):
    while True:
        try:
            return float(input(message))
        except ValueError:
            print("Entrada inválida. Deve ser um número.")

def non_empty_input(message):
    while True:
        valor = input(message).strip()
        if valor:
            return valor
        print("Esse campo não pode ser vazio.")

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
            titulo = non_empty_input("Título: ")
            artista = non_empty_input("Artista: ")
            genero = non_empty_input("Gênero: ")
            ano = input_int("Ano de lançamento: ")
            preco = input_float("Preço: ")
            quantidade = int(input_int("Quantidade: "))

            cd = CD(titulo, artista, genero, ano, preco, quantidade)
            crud.create(cd)

            show_result("Inserir CD", "CD inserido com sucesso!")

        elif opcao == "Alterar CD":
            id_cd = input_int("ID do CD a alterar: ")

            cd_existente = crud.get_by_id(id_cd)

            if not cd_existente:
                show_result("Alterar CD", f"[!] Erro: Não foi encontrado nenhum CD com o ID {id_cd}. Alteração cancelada.")
                continue

            titulo = non_empty_input("Novo título: ")
            artista = non_empty_input("Novo artista: ")
            genero = non_empty_input("Novo gênero: ")
            ano = input_int("Novo ano: ")
            preco = input_float("Novo preço: ")
            quantidade = int(input_int("Nova quantidade: "))

            crud.update(id_cd, titulo, artista, genero, ano, preco, quantidade)

            show_result("Alterar CD", "CD alterado com sucesso!")

        elif opcao == "Pesquisar CD por nome":
            nome = non_empty_input("Digite o nome do CD: ")
            resultados = crud.search_by_title(nome)

            if not resultados:
                show_result("Pesquisar CD por nome", f"[!] Nenhum CD encontrado com o título: '{nome}'")
            else:
                show_result(
                    "Pesquisar CD por nome",
                    "\n\n".join(str(cd) for cd in resultados)
                )

        elif opcao == "Remover CD":
            id_cd = input_int("ID do CD para remover: ")

            cd_existente = crud.get_by_id(id_cd)

            if not cd_existente:
                show_result("Remover CD", f"[!] Erro: Não foi encontrado nenhum CD com o ID {id_cd}. Remoção cancelada.")
                continue

            crud.delete(id_cd)

            show_result("Remover CD", "CD removido com sucesso!")

        elif opcao == "Listar todos":
            cds = crud.get_all()
            show_result("Lista de CDs", format_cd_list(cds))

        elif opcao == "Exibir CD":
            id_cd = input_int("Digite o ID do CD: ")
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

except KeyboardInterrupt:
    print("\n\nEncerrando sistema...\n")