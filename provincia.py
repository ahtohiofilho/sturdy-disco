import numpy as np
from nomenclaturas import formar_nome

class Provincia:
    def __init__(self, civilizacao, planeta, coordenadas):
        self.civilizacao = civilizacao
        self.coordenadas = coordenadas
        self.produtividade_agricultura = planeta.geografia.nodes[coordenadas]['prod_agric']
        self.bioma = planeta.geografia.nodes[coordenadas]['bioma']
        self.placa = planeta.geografia.nodes[coordenadas]['placa']
        self.nome = formar_nome(civilizacao.cultura)
        self.capital_humano = 1