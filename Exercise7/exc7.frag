#version 440

in vec4 vsOutPos;
in vec3 vsOutNormal;

layout(location=0) out vec4 outPosition;
layout(location=1) out vec4 outNormals;
layout(location=2) out vec4 outColors;

void main()
{
    vec3 normalizedNormal = normalize(vsOutNormal);
    outPosition = vsOutPos;
    outNormals = vec4(normalizedNormal, 0.0);
    outColors = vec4(1.0, 0.5, 0.5, 1.0);
}
