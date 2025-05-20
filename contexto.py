from utils.poligonos import dicionario_poligonos
from utils.geografia import definir_geografia

class Contexto:
    def __init__(self, fator=7):
        self.fator = fator
        self.poligonos = dicionario_poligonos(fator)
        self.geografia, self.num_civ = definir_geografia(self.poligonos, fator)
        self.ctx_mgl = None
        self.selected_province = None