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
  float dist = length(lightPosition - position);
  vec3 normalizedNormal = normalize(normal);

  vec4 ambient = vec4(0.1, 0.1, 0.1, 1.0);

  float At_e = 0.15;
  float fallof = 1 / exp(At_e * dist);

  vec4 diffuse = dot(normalizedLightDir, normalizedNormal) * inObjColor *
                 inLightColor * fallof;
  vec3 hVec = normalize(normalizedLightDir + normalize(camPos.xyz - position));
  vec4 specular = pow(dot(hVec, normalizedNormal), 64.0) * vec4(1.0);
  outColor = ambient + diffuse + specular;

  vec3 viewDirection = normalize(camPos.xyz - position);
  if (dot(viewDirection, normalizedNormal) < 0.4) {
    outColor = vec4(0, 0, 0, 0);
  }
}
