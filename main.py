# main.py

from window import Window
from contexto import Contexto

if __name__ == "__main__":
    contexto = Contexto()
    app = Window("Sturdy Disco", contexto)
    app.run()

