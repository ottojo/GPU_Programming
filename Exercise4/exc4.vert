#version 150

uniform mat4 worldViewMatrix;
uniform mat4 ProjMatrix;
uniform vec3 lightPosition;
uniform vec4 inObjColor;
uniform vec4 inLightColor;
uniform vec3 camPos;

in vec4 sPos;
in vec3 sNormal;

out vec4 color;

void main()
{
    vec3 normalizedLightDir = normalize(lightPosition - sPos.xyz);
    vec3 normalizedNormal = normalize(sNormal);
        
    vec4 ambient = vec4(0.1, 0.1, 0.1, 1.0);
	vec4 diffuse = dot(normalizedLightDir, normalizedNormal)*inObjColor*inLightColor;
    vec3 hVec = normalize(normalizedLightDir + normalize(camPos.xyz-sPos.xyz));
    vec4 specular = pow(dot(hVec, normalizedNormal), 64.0)*vec4(1.0);            
    color = ambient + diffuse + specular;
        
	gl_Position = ProjMatrix*worldViewMatrix*sPos;
}
