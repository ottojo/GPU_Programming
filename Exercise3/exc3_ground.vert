#version 150

uniform mat4 worldViewProjMatrix;

in vec4 sPos;
in vec2 sTexCoords;

out vec3 normal;
out vec2 texCoords;

void main()
{    
    normal = vec3(0.0, 1.0, 0.0);
    texCoords = sTexCoords;
    gl_Position = worldViewProjMatrix*sPos;
}
