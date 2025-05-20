# rendering/renderer.py
from OpenGL.GL import *
import numpy as np
from rendering.buffers import prepare_buffers
from rendering.shader import Shader
import glm
import glfw
from utils.font_renderer import FontRenderer

class Renderer:
    def __init__(self, contexto):
        self.contexto = contexto
        self.vao = None
        self.vertex_count = 0
        self.polygon_types = []
        self.render_shader = None
        self.picking_shader = None

        self.ubuntu_font = FontRenderer("assets/fonts/ubuntu_mono_atlas.png")


        # Inicializa shaders e buffers
        self.setup()
        self.init_picking_framebuffer(contexto.window.width, contexto.window.height)

    def init_picking_framebuffer(self, width, height):
        self.picking_fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.picking_fbo)

        # Textura do picking
        self.picking_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.picking_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB32F, width, height, 0, GL_RGB, GL_FLOAT, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.picking_texture, 0)

        # Renderbuffer para profundidade
        self.depth_rb = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.depth_rb)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, width, height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.depth_rb)

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def render_picking_pass(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.picking_fbo)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.picking_shader.use()

        # Obter tamanho da janela para aspect ratio
        window_size = glfw.get_framebuffer_size(glfw.get_current_context())
        if window_size[1] == 0:
            aspect = 1.0
        else:
            aspect = window_size[0] / window_size[1]

        # Criar matriz de projeção perspectiva com pyglm
        projection = glm.perspective(glm.radians(45.0), aspect, 0.1, 100.0)
        view = self.contexto.camera.get_view_matrix()

        # Passar uniforms
        proj_loc = glGetUniformLocation(self.picking_shader.program, "projection")
        view_loc = glGetUniformLocation(self.picking_shader.program, "view")

        if proj_loc != -1:
            glUniformMatrix4fv(proj_loc, 1, GL_FALSE, glm.value_ptr(projection))
        if view_loc != -1:
            glUniformMatrix4fv(view_loc, 1, GL_FALSE, glm.value_ptr(view))

        # Desenhar vértices
        glBindVertexArray(self.vao)
        offset = 0
        for i, sides in enumerate(self.polygon_types):
            r = ((i >> 0) & 0xFF) / 255.0
            g = ((i >> 8) & 0xFF) / 255.0
            b = ((i >> 16) & 0xFF) / 255.0
            glUniform3f(glGetUniformLocation(self.picking_shader.program, "picking_color"), r, g, b)

            mode = GL_TRIANGLE_FAN if sides == 5 or sides == 6 else GL_TRIANGLES
            glDrawArrays(mode, offset, sides)
            offset += sides

        glBindVertexArray(0)
        self.picking_shader.unuse()

    def setup(self):
        try:
            # Carregar shaders normais
            with open("shaders/render_vs.glsl", "r") as f:
                vertex_source = f.read()
            with open("shaders/render_fs.glsl", "r") as f:
                fragment_source = f.read()

            # Carregar shaders de picking
            with open("shaders/picking_vs.glsl", "r") as f:
                picking_vertex_source = f.read()
            with open("shaders/picking_fs.glsl", "r") as f:
                picking_fragment_source = f.read()

        except FileNotFoundError as e:
            print(f"Erro: Arquivo de shader não encontrado - {e}")
            raise

        if not all([vertex_source, fragment_source, picking_vertex_source, picking_fragment_source]):
            raise ValueError("Fonte do shader não pode ser vazia.")

        # Compilar dois shaders distintos
        self.render_shader = Shader(vertex_source, fragment_source)
        self.picking_shader = Shader(picking_vertex_source, picking_fragment_source)

        # Preparar buffers
        vertices, colors, self.polygon_types = prepare_buffers(self.contexto)
        self.vertex_count = len(vertices) // 3

        # Configurar VAO/VBOs
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
        self.render_shader.use()

        # Obter tamanho da janela para aspect ratio
        window_size = glfw.get_framebuffer_size(glfw.get_current_context())
        if window_size[1] == 0:
            aspect = 1.0
        else:
            aspect = window_size[0] / window_size[1]

        # Criar matriz de projeção perspectiva com pyglm
        projection = glm.perspective(glm.radians(45.0), aspect, 0.1, 100.0)

        # Obter view matrix da câmera
        view = self.contexto.camera.get_view_matrix()

        # Passar as matrizes para o shader
        proj_loc = glGetUniformLocation(self.render_shader.program, "projection")
        view_loc = glGetUniformLocation(self.render_shader.program, "view")

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
        self.render_shader.unuse()

    def render_hud(self):
        # Desenha apenas se houver província selecionada
        if hasattr(self.contexto, 'selected_province') and self.contexto.selected_province:
            node_data = self.contexto.geografia.nodes[self.contexto.selected_province]
            lines = [
                f"Província: {self.contexto.selected_province}",
                f"Bioma: {node_data.get('bioma', 'N/A')}",
                f"Temperatura: {node_data.get('temperatura', 'N/A')}°C",
                f"Altitude: {node_data.get('altitude', 'N/A')}",
                f"Umidade: {node_data.get('umidade', 'N/A')}"
            ]

            # Garante que estamos usando a projeção ortográfica
            self.ubuntu_font.prepare_ortho()

            # Posição inicial do texto
            x, y = 20, 20

            # Escala padrão
            scale = 0.5

            # Desenha linha por linha
            for i, line in enumerate(lines):
                self.ubuntu_font.draw_text(x, y + i * 25, line, scale)