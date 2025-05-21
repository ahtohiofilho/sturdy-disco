# unidade.py
class Unidade:
    def __init__(self, tipo, local, civilizacao):
        self.tipo = tipo
        self.local = local
        self.civilizacao = civilizacao
        self.vida = 100
        self.movimento = 2  # número de passos por turno

    def mover_para(self, destino):
        if self.movimento > 0:
            self.local = destino
            self.movimento -= 1
        else:
            print("Sem movimentos restantes.")

    def coletar_recurso(self, recurso, quantidade):
        # Exemplo simples de coleta
        print(f"{self.tipo} coletou {quantidade} de {recurso}.")