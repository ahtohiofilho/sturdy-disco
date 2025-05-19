# window.py

import glfw
from OpenGL.GL import *
import sys
from rendering.renderer import Renderer
from camera import Camera

class Window:
    def __init__(self, title, contexto):
        self.title = title
        self.window = None
        self.contexto = contexto
        self.keys = {}
        self.renderer = None

        # Inicializa a câmera aqui, usando o fator do contexto
        self.camera = Camera(
            fator=contexto.fator,
            position=[0, 0, 10],
            target=[0, 0, 0],
            aspect_ratio=16/9  # Valor padrão (será atualizado após criar a janela)
        )
        contexto.camera = self.camera  # Atualiza o contexto com a câmera criada

    def key_callback(self, window, key, scancode, action, mods):
        if key == glfw.KEY_UP or key == glfw.KEY_DOWN or key == glfw.KEY_LEFT or key == glfw.KEY_RIGHT or key == glfw.KEY_ESCAPE:
            self.keys[key] = action != glfw.RELEASE

    def mouse_callback(self, window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            x, y = glfw.get_cursor_pos(window)
            width, height = glfw.get_framebuffer_size(window)
            key = self.read_pixel_at(x, y, width, height)
            if key is not None:
                self.show_province_menu(key)

    def read_pixel_at(self, x, y, width, height):
        glBindFramebuffer(GL_FRAMEBUFFER, self.renderer.picking_fbo)

        px = int(x)
        py = int(height - y - 1)

        # Garante que as coordenadas estão dentro da tela
        px = max(0, min(px, width - 1))
        py = max(0, min(py, height - 1))

        data = glReadPixels(px, py, 1, 1, GL_RGB, GL_FLOAT)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # Aqui está a correção: garante que data tem os 3 valores RGB
        if len(data.shape) == 3 and data.shape[0] == 1 and data.shape[1] == 1 and data.shape[2] == 3:
            r, g, b = data[0][0]
        elif len(data) == 3:
            r, g, b = data
        else:
            print(f"Erro ao ler pixel: dado inválido retornado {data}")
            return None

        id = int(r * 255) + int(g * 255) * 256 + int(b * 255) * 256 * 256
        nodes = list(self.contexto.geografia.nodes.keys())

        if id >= len(nodes):
            print(f"[ERRO] ID {id} fora do intervalo. Total de nós: {len(nodes)}")
            return None

        return nodes[id]
        
    def show_province_menu(self, key):
        node_data = self.contexto.geografia.nodes[key]
        print("=== Província Selecionada ===")
        print(f"Coordenadas: {key}")
        print(f"Bioma: {node_data.get('bioma', 'N/A')}")
        print(f"Temperatura: {node_data.get('temperatura', 'N/A')}°C")
        print(f"Altitude: {node_data.get('altitude', 'N/A')}")
        print(f"Umidade: {node_data.get('umidade', 'N/A')}")
        print(f"Placa Tectônica: {node_data.get('placa', 'N/A')}")
        print(f"Letra Grega: {node_data.get('letra_grega', 'N/A')}")
        print("==============================")

    def init_glfw(self):
        if not glfw.init():
            print("Erro: não foi possível inicializar o GLFW.")
            return False

        monitor = glfw.get_primary_monitor()
        video_mode = glfw.get_video_mode(monitor)
        """
        red_bits = video_mode.bits.red
        green_bits = video_mode.bits.green
        blue_bits = video_mode.bits.blue
        refresh_rate = video_mode.refresh_rate

        glfw.window_hint(glfw.RED_BITS, red_bits)
        glfw.window_hint(glfw.GREEN_BITS, green_bits)
        glfw.window_hint(glfw.BLUE_BITS, blue_bits)
        glfw.window_hint(glfw.REFRESH_RATE, refresh_rate)
        """
        self.window = glfw.create_window(video_mode.size.width, video_mode.size.height, self.title, monitor, None)

        if not self.window:
            print("Erro: falha ao criar a janela GLFW.")
            glfw.terminate()
            return False

        glfw.make_context_current(self.window)
        
        # Atualiza o aspect ratio da câmera com o tamanho real da janela
        self.width, self.height = glfw.get_framebuffer_size(self.window)
        self.camera.aspect_ratio = self.width / self.height if self.height != 0 else 16/9
        
        # Configura callbacks
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_mouse_button_callback(self.window, self.mouse_callback)

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
        self.renderer = Renderer(self.contexto)
        last_time = glfw.get_time()

        self.renderer.init_picking_framebuffer(self.width, self.height)

        while not glfw.window_should_close(self.window):
            glClearColor(0.0, 0.0, 0.0, 1.0)
            current_time = glfw.get_time()
            delta_time = current_time - last_time
            last_time = current_time

            # Movimento contínuo da câmera
            camera = self.contexto.camera
            sensitivity = 1.0

            if self.keys.get(glfw.KEY_UP):
                camera.rotate_pitch(sensitivity * delta_time * 100)
            if self.keys.get(glfw.KEY_DOWN):
                camera.rotate_pitch(-sensitivity * delta_time * 100)
            if self.keys.get(glfw.KEY_LEFT):
                camera.rotate_yaw(sensitivity * delta_time * 100)
            if self.keys.get(glfw.KEY_RIGHT):
                camera.rotate_yaw(-sensitivity * delta_time * 100)

            # Detecta ESC e fecha a janela
            if self.keys.get(glfw.KEY_ESCAPE):
                glfw.set_window_should_close(self.window, True)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # Atualiza câmera (ex: view matrix)
            self.contexto.camera.update()
            self.renderer.render_picking_pass()
            glBindFramebuffer(GL_FRAMEBUFFER, 0)

            # Renderiza os polígonos via Renderer
            self.renderer.render()

            glfw.swap_buffers(self.window)
            glfw.poll_events()