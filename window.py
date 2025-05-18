# window.py

import glfw
from OpenGL.GL import *
import sys
from rendering.renderer import Renderer

class Window:
    def __init__(self, title, contexto):
        self.title = title
        self.window = None
        self.contexto = contexto

    def key_callback(self, window, key, scancode, action, mods):
        """Função de callback para teclas"""
        if action == glfw.PRESS or action == glfw.REPEAT:
            camera = self.contexto.camera  # Acessa a câmera do contexto
            sensibilidade = 1.0

            if key == glfw.KEY_UP:
                camera.rotate_pitch(sensibilidade)
            elif key == glfw.KEY_DOWN:
                camera.rotate_pitch(-sensibilidade)
            elif key == glfw.KEY_LEFT:
                camera.rotate_yaw(sensibilidade)
            elif key == glfw.KEY_RIGHT:
                camera.rotate_yaw(-sensibilidade)
            elif key == glfw.KEY_ESCAPE:
                glfw.set_window_should_close(window, True)

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

        # Define o callback de tecla
        glfw.set_key_callback(self.window, self.key_callback)

        return True

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

    def main_loop(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)

        # Inicializa o renderer com o contexto
        renderer = Renderer(self.contexto)

        while not glfw.window_should_close(self.window):
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # Atualiza câmera (ex: view matrix)
            self.contexto.camera.update()
            view_matrix = self.contexto.camera.get_view_matrix()

            # Passa a matriz de câmera para o shader (opcional por enquanto)
            # renderer.set_view_matrix(view_matrix)

            # Renderiza os polígonos via Renderer
            renderer.render()

            glfw.swap_buffers(self.window)
            glfw.poll_events()