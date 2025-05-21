# utils/font_renderer.py
import numpy as np
from OpenGL.GL import *
from PIL import Image
import glm
from rendering.shader import Shader
import glfw

class FontRenderer:
    def __init__(self, font_texture_path, char_width=16, char_height=32):
        self.char_width = char_width
        self.char_height = char_height
        self.texture_id = self._load_texture(font_texture_path)
        self.shader = self._init_shader()
        self.vao, self.vbo = self._init_buffers()
        self.buffer_size = 0

    def _load_texture(self, path):
        img = Image.open(path).convert("RGBA")
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        self.tex_width, self.tex_height = img.size

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGBA,
            self.tex_width, self.tex_height, 0,
            GL_RGBA, GL_UNSIGNED_BYTE, img.tobytes()
        )
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        return texture_id

    def _init_shader(self):
        vertex_src = """
        #version 330 core
        layout(location = 0) in vec2 position;
        layout(location = 1) in vec2 texcoord;
        out vec2 uv;
        uniform mat4 projection;
        void main() {
            uv = texcoord;
            gl_Position = projection * vec4(position, 0.0, 1.0);
        }
        """
        fragment_src = """
        #version 330 core
        in vec2 uv;
        out vec4 color;
        uniform sampler2D font_atlas;
        void main() {
            color = texture(font_atlas, uv);
        }
        """
        return Shader(vertex_src, fragment_src)  # Usa sua classe Shader!

    def _init_buffers(self):
        vao = glGenVertexArrays(1)
        vbo = glGenBuffers(1)
        glBindVertexArray(vao)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        
        self.buffer_size = 0
        glBufferData(GL_ARRAY_BUFFER, self.buffer_size, None, GL_DYNAMIC_DRAW)
        
        # Atributos: posição (xy) + texcoord (uv)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(8))
        
        glBindVertexArray(0)
        return vao, vbo
    
    def prepare_ortho(self):
        width, height = glfw.get_framebuffer_size(glfw.get_current_context())
        projection = glm.ortho(0, width, height, 0, -1, 1)
        self.shader.use()
        self.shader.set_uniform("projection", projection)

    def draw_text(self, x, y, text, scale=1.0):
        vertices = []
        for char in text:
            if char == ' ':  # Pula espaços
                x += self.char_width * scale
                continue

            ascii_val = ord(char)

            # Se o caractere não estiver no atlas, pule
            if ascii_val < 32 or ascii_val > 126:
                x += self.char_width * scale
                continue

            # Calcula posição no atlas (sempre na linha 0)
            col = ascii_val - 32  # subtrai offset do primeiro caractere (espaço)

            # Coordenadas UV
            u0 = col * self.char_width / self.tex_width
            v0 = 0  # primeira linha
            u1 = u0 + self.char_width / self.tex_width
            v1 = 1.0  # altura total da imagem

            w = self.char_width * scale
            h = self.char_height * scale

            # Adiciona vértices do quad (x, y, u, v)
            vertices.extend([
                x,     y,     u0, v1,
                x + w, y,     u1, v1,
                x + w, y + h, u1, v0,
                x,     y + h, u0, v0,
            ])
            x += w

        if not vertices:
            return
        
        # Converter para array numpy
        vertex_data = np.array(vertices, dtype=np.float32)
        required_size = vertex_data.nbytes  # Tamanho necessário em bytes

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

        # Verificar se o buffer precisa ser redimensionado
        if required_size > self.buffer_size:
            # Realocar o buffer com o novo tamanho
            glBufferData(GL_ARRAY_BUFFER, required_size, vertex_data, GL_DYNAMIC_DRAW)
            self.buffer_size = required_size
        else:
            # Atualizar apenas os dados existentes
            glBufferSubData(GL_ARRAY_BUFFER, 0, required_size, vertex_data)

        # Upload dos vértices para o VBO
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferSubData(GL_ARRAY_BUFFER, 0, np.array(vertices, dtype=np.float32))

        # Configura estado de renderização
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Ativa shader e textura
        self.shader.use()
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        self.shader.set_uniform("font_atlas", 0)

        # Configura projeção ortográfica
        width, height = glfw.get_framebuffer_size(glfw.get_current_context())
        projection = glm.ortho(0, width, height, 0, -1, 1)
        self.shader.set_uniform("projection", projection)

        # Renderiza
        glBindVertexArray(self.vao)
        glDrawArrays(GL_QUADS, 0, len(vertices) // 4)

        # Restaura estado
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_BLEND)