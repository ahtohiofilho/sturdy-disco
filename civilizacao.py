# civilizacao.py
from random import shuffle, choice, randint
from provincia import Provincia
import os
from OpenGL.GL import *
import pygame
from bandeiras import bandeira

class Civilizacao:
    def __init__(self, planeta):
        self.planeta = planeta
        if planeta.culturas:
            shuffle(planeta.culturas)
            self.cultura = planeta.culturas.pop()
        else:
            planeta.culturas = [
                'English', 'Chinese', 'Spanish',
                'French', 'Indian', 'Russian',
                'Vietnamese', 'Turkish', 'Arabic',
                'Indonesian', 'Persian', 'Hausa',
                'Swahili', 'Portuguese', 'Telugu',
                'Bengali', 'Japanese', 'Marathi',
                'Wu', 'Yue', 'Min',
                'Korean', 'Italian', 'German'
            ]
            shuffle(planeta.culturas)
            self.cultura = planeta.culturas.pop()

        tons_de_pele = [(245, 212, 205), (212, 160, 147), (163, 106, 95), (101, 61, 53)]
        tons_de_cabelo = [(209, 195, 2), (140, 106, 0), (99, 55, 26), (52, 48, 47)]
        self.pele = choice(tons_de_pele)
        self.cabelo = choice(tons_de_cabelo)
        self.nome = choice(list(planeta.civs_cores.keys()))
        self.cor = planeta.civs_cores[self.nome]
        del planeta.civs_cores[self.nome]
        self.bandeira_nome = self.nome
        self.bandeira_modalidade = randint(0, 82)
        shuffle(planeta.lista_capitais)
        self.ponto_inicial = planeta.lista_capitais.pop()
        self.provincias = {}
        self.adicionar_provincia(planeta, self.ponto_inicial)
        self.unidades = []
        self.gerar_bandeira()
        self.textura_bandeira = self.carregar_bandeira_opengl()

    def adicionar_provincia(self, planeta, coordenadas):
        """Cria uma nova província e adiciona ao dicionário de províncias."""
        # Cria a província
        provincia = Provincia(self, planeta, coordenadas)
        self.provincias[coordenadas] = provincia

        # Adiciona a informação da civilização ao nó correspondente no grafo
        if coordenadas in planeta.geografia.nodes:
            planeta.geografia.nodes[coordenadas]['civilizacao'] = self
        else:
            # Se o nó não existir no grafo, adiciona-o com a informação da civilização
            planeta.geografia.add_node(coordenadas, civilizacao=self)

        return provincia
    
    def gerar_bandeira(self):
        """Gera a bandeira da civilização e salva no disco se ainda não existir."""
        caminho = f"assets/imagens/bandeiras_civilizacoes/{self.bandeira_nome}.png"

        if not os.path.exists(caminho):
            bandeira_surface = bandeira(self.bandeira_nome, self.bandeira_modalidade)  # Gera a bandeira
            pygame.image.save(bandeira_surface, caminho)  # Salva no disco

    def carregar_bandeira_opengl(self):
        """Carrega a bandeira salva no disco como textura OpenGL."""
        caminho = os.path.join("assets/imagens/bandeiras_civilizacoes", f"{self.bandeira_nome}.png")
        
        bandeira_surface = pygame.image.load(caminho)  # Carrega a imagem gerada
        texture_id = glGenTextures(1)  # Cria uma textura OpenGL
        glBindTexture(GL_TEXTURE_2D, texture_id)  # Ativa a textura
        
        # Extrai os pixels da superfície
        pixels = pygame.image.tostring(bandeira_surface, "RGBA", True)

        # Configura a textura no OpenGL
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                    bandeira_surface.get_width(), bandeira_surface.get_height(),
                    0, GL_RGBA, GL_UNSIGNED_BYTE, pixels)

        glGenerateMipmap(GL_TEXTURE_2D)  # Gera mipmaps para otimizar visualização
        return texture_id
