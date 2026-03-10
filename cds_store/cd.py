class CD:

    def __init__(self, titulo, artista, genero, ano, preco, quantidade, id_cd=None):

        self.id_cd = id_cd
        self.titulo = titulo
        self.artista = artista
        self.genero = genero
        self.ano = ano
        self.preco = preco
        self.quantidade = quantidade
