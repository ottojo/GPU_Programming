#version 150

uniform mat4 worldViewProjMatrix;
uniform float time;

in vec4 sPos;
in vec3 sNormal;

out vec3 normal;

void main()
{
    gl_Position = worldViewProjMatrix*sPos;
    normal = sNormal;
}


