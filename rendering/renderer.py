# rendering/renderer.py

from OpenGL.GL import *
import numpy as np
from rendering.buffers import prepare_buffers
from rendering.shader import Shader
import glm
import glfw

class Renderer:
    def __init__(self, contexto):
        self.contexto = contexto
        self.vao = None
        self.vertex_count = 0
        self.shader = None
        self.polygon_types = []
        self.setup()

    def setup(self):
        try:
            with open("shaders/vertex.glsl", "r") as f:
                vertex_source = f.read()
            with open("shaders/fragment.glsl", "r") as f:
                fragment_source = f.read()
        except FileNotFoundError as e:
            print(f"Erro: Arquivo de shader não encontrado - {e}")
            raise

        if not vertex_source or not fragment_source:
            raise ValueError("Fonte do shader não pode ser vazia.")

        self.shader = Shader(vertex_source, fragment_source)

        # Atualizado: agora pegamos 3 valores
        vertices, colors, self.polygon_types = prepare_buffers(self.contexto)
        self.vertex_count = len(vertices) // 3  # Número total de vértices

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        vbo_vertices = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_vertices)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

        vbo_colors = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_colors)
        glBufferData(GL_ARRAY_BUFFER, colors.nbytes, colors, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(1)

        glBindVertexArray(0)

    def render(self):
        self.shader.use()

        # Obter tamanho da janela para aspect ratio
        window_size = glfw.get_framebuffer_size(glfw.get_current_context())
        if window_size[1] == 0:
            aspect = 1.0
        else:
            aspect = window_size[0] / window_size[1]

        # Criar matriz de projeção perspectiva com pyglm
        projection = glm.perspective(glm.radians(45.0), aspect, 0.1, 100.0)

        # Obter matriz de view da câmera
        view = self.contexto.camera.get_view_matrix()  # Deve retornar glm.mat4

        # Passar as matrizes para o shader
        proj_loc = glGetUniformLocation(self.shader.program, "projection")
        view_loc = glGetUniformLocation(self.shader.program, "view")

        if proj_loc != -1:
            glUniformMatrix4fv(proj_loc, 1, GL_FALSE, glm.value_ptr(projection))

        if view_loc != -1:
            glUniformMatrix4fv(view_loc, 1, GL_FALSE, glm.value_ptr(view))

        # Desenhar os polígonos individualmente
        glBindVertexArray(self.vao)

        offset = 0
        for sides in self.polygon_types:
            mode = GL_TRIANGLE_FAN if sides == 5 or sides == 6 else GL_TRIANGLES
            glDrawArrays(mode, offset, sides)
            offset += sides

        glBindVertexArray(0)
        self.shader.unuse()