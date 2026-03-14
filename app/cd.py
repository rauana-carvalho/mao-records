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
            f"\nID: {self.id_cd}\n"
            f"Título: {self.titulo}\n"
            f"Artista: {self.artista}\n"
            f"Gênero: {self.genero}\n"
            f"Ano: {self.ano}\n"
            f"Preço: R$ {self.preco:.2f}\n"
            f"Quantidade: {self.quantidade}\n"
        )