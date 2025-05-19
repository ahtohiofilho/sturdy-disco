# main.py

from window import Window
from contexto import Contexto

if __name__ == "__main__":
    contexto = Contexto()
    contexto.window = Window("Sturdy Disco", contexto)
    contexto.window.run()

