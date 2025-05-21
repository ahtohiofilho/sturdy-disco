from planeta import Planeta

class Contexto:
    def __init__(self, fator=5):
        self.fator = fator
        self.planeta = Planeta(self)
        self.ctx_mgl = None
        self.selected_province = None