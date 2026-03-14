class CD:

    def __init__(self, titulo, artista, genero, ano, preco, quantidade, id_cd=None):

        self.id_cd = id_cd
        self.titulo = titulo
        self.artista = artista
        self.genero = genero
        self.ano = ano
        self.preco = preco
        self.quantidade = quantidade

    def __str__(self):

        return (
            f"ID: {self.id_cd} | "
            f"Título: {self.titulo} | "
            f"Artista: {self.artista} | "
            f"Gênero: {self.genero} | "
            f"Ano: {self.ano} | "
            f"Preço: R${self.preco:.2f} | "
            f"Quantidade: {self.quantidade}"
        )