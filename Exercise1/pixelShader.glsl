#version 450
uniform vec3 lightDirection;
uniform vec4 inColor;
in vec3 normal;
out vec4 outColor;

void main() {
    outColor = dot(lightDirection, normal)*inColor;
}

