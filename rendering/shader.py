# shader.py
import OpenGL.GL as gl
import ctypes

class Shader:
    def __init__(self, vertex_source=None, fragment_source=None):
        """
        Inicializa o programa de shader.
        
        :param vertex_source: Código-fonte do vertex shader (str)
        :param fragment_source: Código-fonte do fragment shader (str)
        """
        self.program = gl.glCreateProgram()

        # Compila shaders
        vertex_shader = self.compile_shader(vertex_source, gl.GL_VERTEX_SHADER)
        fragment_shader = self.compile_shader(fragment_source, gl.GL_FRAGMENT_SHADER)

        # Liga os shaders ao programa
        gl.glAttachShader(self.program, vertex_shader)
        gl.glAttachShader(self.program, fragment_shader)

        # Linka o programa
        gl.glLinkProgram(self.program)

        # Verifica se houve erro no link
        if not self.check_link_status():
            raise RuntimeError("Erro ao linkar o programa de shader.")

        # Limpa shaders intermediários
        gl.glDeleteShader(vertex_shader)
        gl.glDeleteShader(fragment_shader)

    def compile_shader(self, source, shader_type):
        if not source or len(source.strip()) == 0:
            raise ValueError("Fonte do shader está vazia.")

        shader = gl.glCreateShader(shader_type)

        # Forma mais simples e confiável
        gl.glShaderSource(shader, source)
        gl.glCompileShader(shader)

        if not self.check_compile_status(shader):
            info_log = gl.glGetShaderInfoLog(shader).decode('utf-8')
            gl.glDeleteShader(shader)
            raise RuntimeError(f"Erro ao compilar shader:\n{info_log}")

        return shader

    def check_compile_status(self, shader):
        """Verifica se o shader foi compilado com sucesso."""
        status = gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS)
        return status == gl.GL_TRUE

    def check_link_status(self):
        """Verifica se o programa de shader foi linkado com sucesso."""
        status = gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS)
        return status == gl.GL_TRUE

    def use(self):
        """Ativa o programa de shader."""
        gl.glUseProgram(self.program)

    def unuse(self):
        """Desativa qualquer programa ativo."""
        gl.glUseProgram(0)

    def get_uniform_location(self, name):
        """Retorna a localização de uma variável uniform."""
        return gl.glGetUniformLocation(self.program, name.encode('utf-8'))

    def set_uniform1f(self, name, value):
        loc = self.get_uniform_location(name)
        if loc != -1:
            gl.glUniform1f(loc, value)

    def set_uniform2f(self, name, x, y):
        loc = self.get_uniform_location(name)
        if loc != -1:
            gl.glUniform2f(loc, x, y)

    def set_uniform3f(self, name, x, y, z):
        loc = self.get_uniform_location(name)
        if loc != -1:
            gl.glUniform3f(loc, x, y, z)

    def set_uniform4f(self, name, x, y, z, w):
        loc = self.get_uniform_location(name)
        if loc != -1:
            gl.glUniform4f(loc, x, y, z, w)

    def set_uniform1i(self, name, value):
        loc = self.get_uniform_location(name)
        if loc != -1:
            gl.glUniform1i(loc, value)