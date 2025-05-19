#version 330 core
uniform vec3 picking_color;

out vec4 outColor;

void main() {
    outColor = vec4(picking_color, 1.0);
}