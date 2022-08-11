#version 150

uniform vec3 lightDirection;
uniform vec4 inObjColor;
uniform vec4 inLightColor;
uniform vec3 camPos; 

in vec3 gsposition;
in vec3 gsnormal;

out vec4 outColor;

void main()
{
    vec3 normalizedNormal = normalize(gsnormal);
    vec3 normalizedLightDir = normalize(lightDirection);
    
    vec4 ambient = vec4(0.1, 0.1, 0.1, 1.0);
	vec4 diffuse = dot(normalizedLightDir, normalizedNormal)*inObjColor*inLightColor;
    vec3 hVec = normalize(normalizedLightDir + normalize(camPos-gsposition));
    vec4 specular = pow(dot(hVec, normalize(gsnormal)), 64.0)*vec4(1.0);            
    outColor = ambient + diffuse + specular;
}
