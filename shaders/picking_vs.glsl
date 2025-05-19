#version 330 core
layout(location = 0) in vec3 position;
uniform mat4 projection;
uniform mat4 view;

out vec3 fragPickingColor;  // Não usado aqui, mas pode ser útil no futuro

void main() {
    gl_Position = projection * view * vec4(position, 1.0);
}