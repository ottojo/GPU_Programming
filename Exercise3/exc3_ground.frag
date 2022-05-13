#version 150

uniform sampler2D diffTexture;

in vec3 normal;
in vec2 texCoords;

out vec4 outColor;

void main()
{
    //Get the color from the texture.
    outColor = texture(diffTexture, texCoords)*0.75;
}
