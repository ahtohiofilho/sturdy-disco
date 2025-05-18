# window.py

import sys
import glfw
from OpenGL.GL import *

class Window:
    def __init__(self, title="Janela Fullscreen"):
        self.title = title
        self.window = None

    def init_glfw(self):
        if not glfw.init():
            print("Erro: não foi possível inicializar o GLFW.")
            return False

        monitor = glfw.get_primary_monitor()
        if not monitor:
            print("Erro: monitor principal não encontrado.")
            glfw.terminate()
            return False

        video_mode = glfw.get_video_mode(monitor)
        if not video_mode:
            print("Erro: não foi possível obter o modo de vídeo.")
            glfw.terminate()
            return False

        width = video_mode.size.width
        height = video_mode.size.height
        red_bits = video_mode.bits.red
        green_bits = video_mode.bits.green
        blue_bits = video_mode.bits.blue
        refresh_rate = video_mode.refresh_rate

        glfw.window_hint(glfw.RED_BITS, red_bits)
        glfw.window_hint(glfw.GREEN_BITS, green_bits)
        glfw.window_hint(glfw.BLUE_BITS, blue_bits)
        glfw.window_hint(glfw.REFRESH_RATE, refresh_rate)

        self.window = glfw.create_window(width, height, self.title, monitor, None)

        if not self.window:
            print("Erro: falha ao criar a janela GLFW.")
            glfw.terminate()
            return False

        glfw.make_context_current(self.window)
        return True

    def main_loop(self):
        glClearColor(0.1, 0.2, 0.5, 1.0)  # Cor de fundo

        while not glfw.window_should_close(self.window):
            glClear(GL_COLOR_BUFFER_BIT)

            # Lógica de renderização vai aqui

            glfw.swap_buffers(self.window)
            glfw.poll_events()

    def run(self):
        if not self.init_glfw():
            sys.exit(1)

        try:
            self.main_loop()
        finally:
            self.cleanup()

    def cleanup(self):
        if self.window:
            glfw.destroy_window(self.window)
        glfw.terminate()
