#version 450
uniform mat4 worldViewProjMatrix;
in vec4 sPos;
in vec3 sNormal;
out vec3 normal;

void main() {
    normal = sNormal;
    //TODO - Add the vertex transformation
}