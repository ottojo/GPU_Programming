#version 440

uniform mat4 worldViewProjMatrix;
uniform sampler2D displTexture;

in vec4 sPos;
in vec2 sTexCoords;

out vec3 position;
out vec3 normal;
out vec3 tangent;
out vec3 binormal;
out vec2 texCoords;
out float height;

#define HEIGHT_SCALE 0.15

void main()
{    
    binormal = vec3(0.0, 0.0, -1.0);
    tangent = vec3(1.0, 0.0, 0.0);
    normal = vec3(0.0, 1.0, 0.0);

    float inDisp = texture(displTexture, sTexCoords).r;
    height = inDisp*HEIGHT_SCALE;
    position = sPos.xyz + normal*height;
    
    texCoords = sTexCoords;
    gl_Position = worldViewProjMatrix*vec4(position, 1.0);
}
