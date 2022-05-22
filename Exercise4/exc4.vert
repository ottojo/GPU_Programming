#version 150

uniform mat4 worldViewMatrix;
uniform mat4 ProjMatrix;

in vec4 sPos;
in vec3 sNormal;

out vec3 position;
out vec3 normal;

void main() {
  position = sPos.xyz;
  normal = sNormal;

  gl_Position = ProjMatrix * worldViewMatrix * sPos;
}
