#version 440

in vec2 inPos;

out vec2 uv;

void main() {
    uv = inPos;
    gl_Position = vec4(inPos * 2.0 - 1.0, 0.0, 1.0);
}
