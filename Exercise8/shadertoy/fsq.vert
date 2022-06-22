#version 430

in vec2 in_vert;
out vec2 texCoord;

void main() {
    gl_Position = vec4(in_vert, 0.0, 1.0);
    texCoord = in_vert / 2.0 + 0.5;
}