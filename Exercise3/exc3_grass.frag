#version 150


uniform sampler2D diffTexture;

in vec2 texCoords;
in float scaleColor;

out vec4 outColor;

void main()
{
    vec4 color = texture(diffTexture, texCoords);
    if(color.a < 1.0)
        discard;
    outColor = color*scaleColor*0.9;
}
