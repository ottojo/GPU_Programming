#version 150

uniform mat4 worldViewProjMatrix;

in vec4 sPos;
in vec3 sNormal;
in vec3 sTangent;
in vec3 sBinormal;
in vec2 sTexCoords;

out vec3 position;
out vec3 normal;
out vec3 tangent;
out vec3 binormal;
out vec2 texCoords;

void main()
{
    gl_Position = worldViewProjMatrix*sPos;
    position = sPos.xyz;
    normal = sNormal;
    tangent = sTangent;
    binormal = sBinormal;
    texCoords = sTexCoords;
}


