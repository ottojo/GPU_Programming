#version 150

uniform vec3 lightPosition;
uniform vec4 inObjColor;
uniform vec4 inLightColor;
uniform vec3 camPos;

in vec3 position;
in vec3 normal;

out vec4 outColor;

void main() {
  vec3 normalizedLightDir = normalize(lightPosition - position);
  vec3 normalizedNormal = normalize(normal);

  vec4 ambient = vec4(0.1, 0.1, 0.1, 1.0);
  vec4 diffuse =
      dot(normalizedLightDir, normalizedNormal) * inObjColor * inLightColor;
  vec3 hVec = normalize(normalizedLightDir + normalize(camPos.xyz - position));
  vec4 specular = pow(dot(hVec, normalizedNormal), 64.0) * vec4(1.0);
  outColor = ambient + diffuse + specular;
}