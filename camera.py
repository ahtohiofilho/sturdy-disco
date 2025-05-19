# camera.py
import numpy as np
from math import sin, cos, radians, pi
import glm
import glfw
import math


class Camera:
    def __init__(self, fator, position=(0, 0, 5), target=(0, 0, 0), up=(0, 1, 0), aspect_ratio=16/9):
        self.target = np.array(target, dtype=np.float32)
        self.world_up = np.array(up, dtype=np.float32)
        self.yaw = -90.0   # Olhando para +z inicialmente
        self.pitch = 0.0
        self.speed = 0.5
        self.sensitivity = 0.3
        self.aspect_ratio = aspect_ratio

        # Calcula o raio do planeta com base no fator
        self.raio_planeta = fator / (2 * math.sin(math.pi / 5))

        # Define posição inicial com base no raio
        distance = 3.0 * self.raio_planeta  # 3 raios de distância
        self.position = np.array(position if position is not None else [0, 0, distance], dtype=np.float32)

        # Obter proporção da tela
        self.aspect_ratio = self.get_screen_aspect_ratio() or 16 / 9

        # Inicializa vetores de câmera
        self.front = np.array([0.0, 0.0, 0.0])
        self.right = np.array([0.0, 0.0, 0.0])
        self.up = np.array([0.0, 0.0, 0.0])

        # Atualiza vetores com base na posição inicial
        self.update()
        self._update_position_from_angles()

    @staticmethod
    def get_screen_aspect_ratio():
        if not glfw.init():
            print("Erro ao inicializar GLFW")
            return None

        # Criar uma janela temporária para obter informações
        glfw.window_hint(glfw.VISIBLE, False)  # Ocultar a janela
        window = glfw.create_window(800, 600, "Temp", None, None)

        if not window:
            print("Erro ao criar janela GLFW")
            glfw.terminate()
            return None

        glfw.make_context_current(window)
        width, height = glfw.get_framebuffer_size(window)
        glfw.destroy_window(window)
        glfw.terminate()

        return width / height

    def get_view_matrix(self):
        return glm.lookAt(
            glm.vec3(*self.position),
            glm.vec3(*self.target),
            glm.vec3(*self.world_up)
        )

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(45.0), self.aspect_ratio, 0.1, 100.0 * self.raio_planeta)

    def update(self):
        front = np.array([
            cos(radians(self.yaw)) * cos(radians(self.pitch)),
            sin(radians(self.pitch)),
            sin(radians(self.yaw)) * cos(radians(self.pitch))
        ])
        self.front = front / np.linalg.norm(front)
        self.right = np.cross(self.front, self.world_up)
        self.right /= np.linalg.norm(self.right)
        self.up = np.cross(self.right, self.front)
        self.up /= np.linalg.norm(self.up)

    def rotate_yaw(self, angle):
        self.yaw += angle
        self.update()
        self._update_position_from_angles()

    def rotate_pitch(self, angle):
        self.pitch = np.clip(self.pitch + angle, -89.0, 89.0)
        self.update()
        self._update_position_from_angles()

    def _update_position_from_angles(self):
        radius = np.linalg.norm(self.position - self.target)
        self.position = self.target + np.array([
            cos(radians(self.yaw)) * cos(radians(self.pitch)),
            sin(radians(self.pitch)),
            sin(radians(self.yaw)) * cos(radians(self.pitch))
        ]) * radius

    def _look_at(self, eye, center, up):
        f = (center - eye)
        f /= np.linalg.norm(f)
        s = np.cross(f, up)
        s /= np.linalg.norm(s)
        u = np.cross(s, f)
        u /= np.linalg.norm(u)

        view = np.identity(4, dtype=np.float32)
        view[0, :3] = s
        view[1, :3] = u
        view[2, :3] = -f
        view[:3, 3] = -np.dot(s, eye), -np.dot(u, eye), np.dot(f, eye)
        return view