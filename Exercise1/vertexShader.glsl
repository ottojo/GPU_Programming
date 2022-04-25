#version 450
uniform mat4 worldViewProjMatrix;
in vec4 sPos;
in vec3 sNormal;
out vec3 normal;

void main() {
    normal = sNormal;
    // Model space -> world space -> view space -> projection space
    gl_Position = worldViewProjMatrix * sPos;
}
