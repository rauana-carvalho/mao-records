from cd import CD
from cd_crud import CDCrud
from welcome import show_home_screen
import questionary

crud = CDCrud()


def menu():
    return questionary.select(
        "Escolha uma opção:",
        choices=[
            "Inserir CD",
            "Alterar CD",
            "Pesquisar CD por nome",
            "Remover CD",
            "Listar todos",
            "Exibir CD",
            "Relatório de estoque",
            "Sair",
        ],
        qmark="⋆",
        pointer="💿",
    ).ask()


try:
    if not show_home_screen():
        raise SystemExit

    while True:
        print("\n===== LOJA DE CDs =====")

        opcao = menu()

        if opcao == "Inserir CD":
            titulo = input("Título: ")
            artista = input("Artista: ")
            genero = input("Gênero: ")
            ano = int(input("Ano de lançamento: "))
            preco = float(input("Preço: "))
            quantidade = int(input("Quantidade: "))

            cd = CD(titulo, artista, genero, ano, preco, quantidade)
            crud.create(cd)

            print("CD inserido com sucesso!")

        elif opcao == "Alterar CD":
            id_cd = int(input("ID do CD a alterar: "))

            cd_existente = crud.get_by_id(id_cd)

            if not cd_existente:
                print(f"\n[!] Erro: Não foi encontrado nenhum CD com o ID {id_cd}. Alteração cancelada.")
                continue

            titulo = input("Novo título: ")
            artista = input("Novo artista: ")
            genero = input("Novo gênero: ")
            ano = int(input("Novo ano: "))
            preco = float(input("Novo preço: "))
            quantidade = int(input("Nova quantidade: "))

            crud.update(id_cd, titulo, artista, genero, ano, preco, quantidade)

            print("CD alterado com sucesso!")

        elif opcao == "Pesquisar CD por nome":
            nome = input("Digite o nome do CD: ")
            resultados = crud.search_by_title(nome)

            if not resultados:
                print(f"\n[!] Nenhum CD encontrado com o título: '{nome}'")
            else:
                for cd in resultados:
                    print(cd)

        elif opcao == "Remover CD":
            id_cd = int(input("ID do CD para remover: "))

            cd_existente = crud.get_by_id(id_cd)

            if not cd_existente:
                print(f"\n[!] Erro: Não foi encontrado nenhum CD com o ID {id_cd}. Remoção cancelada.")
                continue

            crud.delete(id_cd)

            print("CD removido com sucesso!")

        elif opcao == "Listar todos":
            cds = crud.get_all()

            if not cds:
                print("\n[!] O estoque está vazio. Nenhum CD cadastrado.")
            else:
                print("\n--- LISTA DE TODOS OS CDS ---")
                for cd in cds:
                    print(cd)

        elif opcao == "Exibir CD":
            id_cd = int(input("Digite o ID do CD: "))
            cd = crud.get_by_id(id_cd)

            if cd:
                print(cd)
            else:
                print(f"\n[!] CD com ID {id_cd} não encontrado.")

        elif opcao == "Relatório de estoque":
            crud.report()

        elif opcao == "Sair":
            print("Encerrando o programa")
            break

except KeyboardInterrupt:
    print("\n\nEncerrando sistema...\n")