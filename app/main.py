from cd import CD
from cd_crud import CDCrud
from welcome import show_home_screen, interactive_menu, show_result

crud = CDCrud()


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
            titulo = input("Título: ")
            artista = input("Artista: ")
            genero = input("Gênero: ")
            ano = int(input("Ano de lançamento: "))
            preco = float(input("Preço: "))
            quantidade = int(input("Quantidade: "))

            cd = CD(titulo, artista, genero, ano, preco, quantidade)
            crud.create(cd)

            show_result("Inserir CD", "CD inserido com sucesso!")

        elif opcao == "Alterar CD":
            id_cd = int(input("ID do CD a alterar: "))

            cd_existente = crud.get_by_id(id_cd)

            if not cd_existente:
                show_result("Alterar CD", f"[!] Erro: Não foi encontrado nenhum CD com o ID {id_cd}. Alteração cancelada.")
                continue

            titulo = input("Novo título: ")
            artista = input("Novo artista: ")
            genero = input("Novo gênero: ")
            ano = int(input("Novo ano: "))
            preco = float(input("Novo preço: "))
            quantidade = int(input("Nova quantidade: "))

            crud.update(id_cd, titulo, artista, genero, ano, preco, quantidade)

            show_result("Alterar CD", "CD alterado com sucesso!")

        elif opcao == "Pesquisar CD por nome":
            nome = input("Digite o nome do CD: ")
            resultados = crud.search_by_title(nome)

            if not resultados:
                show_result("Pesquisar CD por nome", f"[!] Nenhum CD encontrado com o título: '{nome}'")
            else:
                show_result(
                    "Pesquisar CD por nome",
                    "\n\n".join(str(cd) for cd in resultados)
                )

        elif opcao == "Remover CD":
            id_cd = int(input("ID do CD para remover: "))

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
            id_cd = int(input("Digite o ID do CD: "))
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