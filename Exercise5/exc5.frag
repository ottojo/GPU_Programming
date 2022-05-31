#version 150

uniform vec3 lightDirection;
uniform vec3 camPos; 
uniform sampler2D diffTexture;
uniform sampler2D specTexture;
uniform sampler2D displTexture;

in vec3 position;
in vec3 normal;
in vec3 tangent;
in vec3 binormal;
in vec2 texCoords;
in float height;

out vec4 outColor;

#define HEIGHT_SCALE 0.15
#define MAX_ITERS 50
#define DISPLACEMENT 0.005
#define EPSILON 1e-2

void main()
{
    // Compute the normal
    vec3 v1 = dFdx(position);
    vec3 v2 = dFdy(position);
    vec3 normalizedNormal = normalize(cross(v1, v2));
    
    // Get the colors from the texture.
    vec4 inColor = texture(diffTexture, texCoords);
    vec4 inSpecColor = texture(specTexture, texCoords);
    
    // Compute the lighting.
    vec3 normalizedLightDir = normalize(lightDirection);
    vec4 ambient = vec4(0.1, 0.1, 0.1, 1.0);
	vec4 diffuse = dot(normalizedLightDir, normalizedNormal) * inColor;
    vec3 hVec = normalize(normalizedLightDir + normalize(camPos - position));
    vec4 specular = pow(dot(hVec, normalizedNormal), 128.0) * inSpecColor * vec4(1.0);            
    
    // Compute the transformation matrix to go from world space to tangent space.
    //  y and z cols/rows are switched compared to lecture, we want z=up
    mat3 transMat = mat3(tangent.x,  binormal.x, normal.x,
                         tangent.z,  binormal.z, normal.z,
                         tangent.y,  binormal.y, normal.y);

    // Tansform the light direction to tangent space and initialize the variables for the loop.
    vec3 transLightDir = normalize(transMat * normalizedLightDir);
    vec3 curTexCoords = vec3(texCoords, height) + transLightDir * DISPLACEMENT;

    // Compute the occlusion
    float occlusion = 1.0;
    for(int i = 0; i < MAX_ITERS; i++){
        if(curTexCoords.z < HEIGHT_SCALE * texture(displTexture, curTexCoords.xy).r) {
            // Point below surface!
            occlusion = 0.1;
            break;
        }
        curTexCoords += transLightDir * DISPLACEMENT;
    }

    // Combine everything.
    outColor = ambient + (diffuse + specular) * occlusion;
}
