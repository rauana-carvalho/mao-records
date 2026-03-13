from database import connect
from cd import CD


class CDCrud:


    def create(self, cd):

        connection = connect()
        cursor = connection.cursor()

        sql = """
        INSERT INTO cds (titulo, artista, genero, ano_lancamento, preco, quantidade)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        valores = (
            cd.titulo,
            cd.artista,
            cd.genero,
            cd.ano,
            cd.preco,
            cd.quantidade
        )

        cursor.execute(sql, valores)

        connection.commit()

        cursor.close()
        connection.close()



    def update(self, id_cd, titulo, artista, genero, ano, preco, quantidade):

        connection = connect()
        cursor = connection.cursor()

        sql = """
        UPDATE cds
        SET titulo=%s, artista=%s, genero=%s, ano_lancamento=%s, preco=%s, quantidade=%s
        WHERE id=%s
        """

        valores = (titulo, artista, genero, ano, preco, quantidade, id_cd)

        cursor.execute(sql, valores)

        connection.commit()

        cursor.close()
        connection.close()



    def search_by_title(self, nome):

        connection = connect()
        cursor = connection.cursor()

        sql = "SELECT * FROM cds WHERE titulo LIKE %s"

        cursor.execute(sql, ("%" + nome + "%",))

        resultados = cursor.fetchall()

        cds = []

        for row in resultados:

            cd = CD(
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                row[0]
            )

            cds.append(cd)

        cursor.close()
        connection.close()

        return cds



    def delete(self, id_cd):

        connection = connect()
        cursor = connection.cursor()

        sql = "DELETE FROM cds WHERE id=%s"

        cursor.execute(sql, (id_cd,))

        connection.commit()

        cursor.close()
        connection.close()



    def list_all(self):

        connection = connect()
        cursor = connection.cursor()

        sql = "SELECT * FROM cds"

        cursor.execute(sql)

        resultados = cursor.fetchall()

        cds = []

        for row in resultados:

            cd = CD(
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                row[0]
            )

            cds.append(cd)

        cursor.close()
        connection.close()

        return cds
    


    def get_one(self, id_cd):

        connection = connect()
        cursor = connection.cursor()

        sql = "SELECT * FROM cds WHERE id=%s"

        cursor.execute(sql, (id_cd,))

        resultado = cursor.fetchone()

        cursor.close()
        connection.close()

        if resultado:

            return CD(
                resultado[1],
                resultado[2],
                resultado[3],
                resultado[4],
                resultado[5],
                resultado[6],
                resultado[0]
            )

        return None
    


    def report(self):

        connection = connect()
        cursor = connection.cursor()

        sql = "SELECT COUNT(*), SUM(quantidade), SUM(preco * quantidade) FROM cds"

        cursor.execute(sql)

        resultado = cursor.fetchone()

        total_cds = resultado[0]
        total_quantidade = resultado[1]
        valor_total = resultado[2]

        print("\n===== RELATÓRIO DE ESTOQUE =====")
        print("Total de CDs cadastrados:", total_cds)
        print("Quantidade total em estoque:", total_quantidade)
        print("Valor total do estoque: R$", valor_total)

        cursor.close()
        connection.close()

