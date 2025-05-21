# planeta.py
from utils.poligonos import dicionario_poligonos
from utils.geografia import definir_geografia
from civilizacao import Civilizacao
from networkx import shortest_path_length
from random import choice, sample

class Planeta:
    def __init__(self, contexto):
        self.poligonos = dicionario_poligonos(contexto.fator)
        self.geografia, self.num_civs = definir_geografia(self.poligonos, contexto.fator)
        self.civilizacoes = []

        prados = [n for n, attr in self.geografia.nodes(data=True) if attr['bioma'] == 'prado']
        self.lista_capitais = [choice(prados)]
        while len(self.lista_capitais) < self.num_civs:
            d2 = {}
            for candidato in prados:
                if candidato in self.lista_capitais:
                    continue
                d = {}
                for capital in self.lista_capitais:
                    d[capital] = shortest_path_length(self.geografia, source=candidato, target=capital, weight='custo_mobilidade')
                d2[candidato] = min(d.values())
            if not d2:  # Se não houver candidatos possíveis, o planeta não comporta a quantidade desejada
                print("d2 vazio")
                raise ValueError("O planeta não comporta essa quantidade de civilizações!")
            maior_valor = max(d2.values())
            chaves_maior_valor = [chave for chave, valor in d2.items() if valor == maior_valor]
            self.lista_capitais.append(choice(chaves_maior_valor))
        print(f"Lista de capitais: {self.lista_capitais}")
        self.civilizacoes = {}
        self.culturas = [
            'English', 'Chinese', 'Spanish',
            'French', 'Indian', 'Russian',
            'Vietnamese', 'Turkish', 'Arabic',
            'Indonesian', 'Persian', 'Hausa',
            'Swahili', 'Portuguese', 'Telugu',
            'Bengali', 'Japanese', 'Marathi',
            'Wu', 'Yue', 'Min',
            'Korean', 'Italian', 'German'
        ]
        self.civs_cores = {
            'Black': (16, 16, 16), 'Midnight Blue': (0, 0, 127), 'Blue': (0, 0, 255),
            'Dark Green': (0, 127, 0), 'Teal': (0, 127, 127), 'Sky Blue': (32, 127, 223),
            'Green': (0, 255, 0), 'Spring Green': (0, 255, 127), 'Cyan': (0, 223, 223),
            'Maroon': (127, 0, 0), 'Purple': (127, 0, 127), 'Violet': (127, 0, 255),
            'Olive': (127, 127, 0), 'Gray': (127, 127, 127), 'Lavender': (127, 127, 255),
            'Chartreuse': (127, 255, 0), 'Light Green': (127, 223, 127), 'Pale Cyan': (127, 255, 255),
            'Red': (234, 33, 37), 'Rose': (255, 0, 127), 'Magenta': (255, 0, 255),
            'Orange': (223, 127, 32), 'Salmon': (255, 127, 127), 'Orchid': (255, 127, 255),
            'Yellow': (255, 255, 0), 'Light Yellow': (255, 255, 127), 'White': (250, 255, 253)
        }
        for _ in range(self.num_civs):
            civilizacao = Civilizacao(self)
            self.civilizacoes[civilizacao.nome] = civilizacao

        self.circulo_civilizacoes = sample(list(self.civilizacoes.values()), len(self.civilizacoes))
        # Define as relações de inimizade iniciais
        self.definir_inimigos()
        self.rodada = 0

    def definir_inimigos(self):
        """Define as relações de inimizade entre as civilizações no círculo."""
        n = len(self.circulo_civilizacoes)
        for i in range(n):
            civ_atual = self.circulo_civilizacoes[i]
            civ_esquerda = self.circulo_civilizacoes[(i - 1) % n]  # Civilização à esquerda
            civ_direita = self.circulo_civilizacoes[(i + 1) % n]   # Civilização à direita

            # Define as civilizações adjacentes como inimigas
            civ_atual.inimigos = {civ_esquerda.nome: civ_esquerda, civ_direita.nome: civ_direita}