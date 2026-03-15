# main.py
from cd import CD
from cd_crud import CDCrud
from welcome import show_home_screen

crud = CDCrud()

def menu():

    print("\n===== LOJA DE CDs =====")
    print("1 - Inserir CD")
    print("2 - Alterar CD")
    print("3 - Pesquisar CD por nome")
    print("4 - Remover CD")
    print("5 - Listar todos")
    print("6 - Exibir CD")
    print("7 - Relatório de estoque")
    print("0 - Sair")

try:
    if not show_home_screen():
        raise SystemExit

    while True:

        menu()

        opcao = input("Escolha uma opção: ")

        if opcao == "1":

            titulo = input("Título: ")
            artista = input("Artista: ")
            genero = input("Gênero: ")
            ano = int(input("Ano de lançamento: "))
            preco = float(input("Preço: "))
            quantidade = int(input("Quantidade: "))

            cd = CD(titulo, artista, genero, ano, preco, quantidade)

            crud.create(cd)

            print("CD inserido com sucesso!")


        elif opcao == "2":

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


        elif opcao == "3":
            nome = input("Digite o nome do CD: ")
            resultados = crud.search_by_title(nome)

            if not resultados:
                print(f"\n[!] Nenhum CD encontrado com o título: '{nome}'")
            else:
                for cd in resultados:
                    print(cd)


        elif opcao == "4":

            id_cd = int(input("ID do CD para remover: "))

            cd_existente = crud.get_by_id(id_cd)
            
            if not cd_existente:
                print(f"\n[!] Erro: Não foi encontrado nenhum CD com o ID {id_cd}. Alteração cancelada.")
                continue

            crud.delete(id_cd)

            print("CD removido com sucesso!")


        elif opcao == "5":
            cds = crud.get_all()

            if not cds:
                print("\n[!] O estoque está vazio. Nenhum CD cadastrado.")
            else:
                print("\n--- LISTA DE TODOS OS CDS ---")
                for cd in cds:
                    print(cd)


        elif opcao == "6":
            id_cd = int(input("Digite o ID do CD: "))
            cd = crud.get_by_id(id_cd)

            if cd:
                print(cd)
            else:
                print(f"\n[!] CD com ID {id_cd} não encontrado.")


        elif opcao == "7":

            crud.report()


        elif opcao == "0":

            print("Encerrando o programa")
            break

        else:

            print("Opção inválida")

except KeyboardInterrupt:
    print("\n\nEncerrando sistema...\n")