# Exercise 4

## 1: Blinn-Phong Shading
An improved result is achieved by moving the lighting calculation from the
vertex shader to the fragment shader, interpolating normal and position instead
of color.

Vertex Shader:
```glsl
#version 150

uniform mat4 worldViewMatrix;
uniform mat4 ProjMatrix;

in vec4 sPos;
in vec3 sNormal;

out vec3 position;
out vec3 normal;

void main() {
  position = sPos.xyz;
  normal = sNormal;

  gl_Position = ProjMatrix * worldViewMatrix * sPos;
}
```

Fragment Shader:
```glsl
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
```

## 2: Exponential falloff
A `fallof` term was introduced with the required scaling factor.
The falloff is multiplied with the existing Lambertian reflection calculating in
the diffuse lighting calculation:

```glsl
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
}
```

## 3: Silhouette
At the edge of the model the normal is approximately orthogonal to the view
direction. This is checked by testing if the dot product between view direction
and normal is close to zero:

```glsl
vec3 viewDirection = normalize(camPos.xyz - position);
if (dot(viewDirection, normalizedNormal) < 0.4) {
  outColor = vec4(0, 0, 0, 0);
}
```

The color is set to zero if the test determines the pixel belongs to the
silhouette.

```glsl
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
```
