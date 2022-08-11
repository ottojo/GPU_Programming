#version 440

uniform mat4 worldViewMatrix;
uniform mat4 ProjMatrix;

in vec4 sPos;
in vec3 sNormal;

out vec4 vsOutPos;
out vec3 vsOutNormal;

void main()
{        
    vsOutPos = sPos;
    vsOutNormal = sNormal;
	gl_Position = ProjMatrix*worldViewMatrix*sPos;
}
