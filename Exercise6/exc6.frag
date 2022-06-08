#version 150

uniform vec3 lightDirection;
uniform vec3 camPos;
uniform sampler2D diffTexture;
uniform sampler2D specTexture;
uniform sampler2D normalTexture;
uniform sampler2D dispTexture;

in vec3 position;
in vec3 normal;
in vec3 tangent;
in vec3 binormal;
in vec2 texCoords;

out vec4 outColor;

#define MAX_ITER 50

bool belowSurface(float currH, vec2 stin, vec2 stout) {
  vec2 newTexCoords = stin * currH + stout * (1.0 - currH);
  float height = texture(dispTexture, newTexCoords).r;
  if (currH <= height) {
    return true;
  }
  return false;
}

void main() {
  vec3 tnormalized = normalize(tangent);
  vec3 nnormalized = normalize(normal);
  vec3 bnormalized = normalize(binormal);
  mat3 normTransform = mat3(tnormalized.x, nnormalized.x, bnormalized.x,
                            tnormalized.y, nnormalized.y, bnormalized.y,
                            tnormalized.z, nnormalized.z, bnormalized.z);

  vec3 viewVectTS = normalize(normTransform * normalize(camPos - position));
  vec3 lightVectTS = normalize(normTransform * normalize(lightDirection));

  vec2 stout = texCoords;
  vec2 stin = texCoords + (viewVectTS.xz / viewVectTS.y) * 0.1;

  vec2 newTexCoords;
  float currH = 1.0;
  float intersection = 0.0;

  /*
  for(int i = 0; i < MAX_ITER; ++i)
  {
      currH -= 1.0/float(MAX_ITER);
      newTexCoords = stin*currH + stout*(1.0-currH);
      float height = texture(dispTexture, newTexCoords).r;
      if(intersection == 0.0){
          if(currH <= height){
              intersection = currH;
          }
      }
  }*/
  

  float hMin = 0;
  float hMax = 1;

  for (int i = 0; i < MAX_ITER; i++) {
    float middle = hMin + 0.5 * (hMax - hMin);
    if (belowSurface(middle, stin, stout)) {
      
      hMin = middle;
    } else {
      hMax = middle;
    }
  }

  intersection = hMin + 0.5 * (hMax - hMin);

  newTexCoords = stin * intersection + stout * (1.0 - intersection);

  vec4 inColor = texture(diffTexture, newTexCoords);
  vec4 inSpecColor = texture(specTexture, newTexCoords);
  vec3 inNormal = texture(normalTexture, newTexCoords).xzy;
  vec3 normalizedNormal = normalize(normalize(inNormal * 2.0 - 1.0));

  vec4 ambient = vec4(0.1, 0.1, 0.1, 1.0);
  vec4 diffuse = dot(lightVectTS, normalizedNormal) * inColor;
  vec3 hVec = normalize(lightVectTS + viewVectTS);
  vec4 specular = pow(dot(hVec, normalizedNormal), 128.0) * inSpecColor *
                  vec4(1.25, 1.25, 1.25, 1.0);
  outColor = ambient + diffuse + specular;
}
