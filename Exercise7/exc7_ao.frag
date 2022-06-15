#version 440

uniform sampler2D posTex;    // Position in world space for each pixel
uniform sampler2D normalTex; // Normal in world space for each pixel
uniform sampler2D colorTex;  // Model color

in vec2 uv;

out vec4 outColor;

#define NUM_ROTATIONS 25
#define NUM_SAMPLES_DIRECTION 20
#define DISPLACEMENT 0.0025
#define PI 3.14159265359
#define MAX_EFFECT_DISTANCE 1.0

mat2 rotationMatrix(float angle) {
    return mat2(cos(angle), sin(angle), -sin(angle), cos(angle));
}

void main() {
    vec4 currPos = texture(posTex, uv);
    vec4 normalPos = texture(normalTex, uv);
    vec4 colorPos = texture(colorTex, uv);

    if (currPos.w > 0.0) {
        // Model pixel
        vec2 initScreenVect = normalize(vec2(1.0, 0.0));
        float ao = 0.0;
        float augment = PI * 2.0 / float(NUM_ROTATIONS);

        for (int i = 0; i < NUM_ROTATIONS; i++) {
            // Rotate along the circle and compute the orientation vector in screen space each iteration.

            // 2D ray in screen space
            vec2 currentScreenVect = rotationMatrix(i * augment) * initScreenVect;

            float prevAngle = PI / 2.0; // Minimum angle in current direction
            float currAO = 1.0;

            // Move along currentScreenVect ray
            for (int j = 1; j <= NUM_SAMPLES_DIRECTION; j++) {
                // Get the current position along the ray.
                vec4 auxPosition = texture(posTex, uv + j * DISPLACEMENT * currentScreenVect);

                // Check that it is not a background pixel.
                if (auxPosition.w > 0.0) {

                    // Compute the distance between the center point (currPos) and the position we are checking.
                    float distance = length(auxPosition - currPos);
                    distance = min(MAX_EFFECT_DISTANCE, distance);

                    // Compute the angle between the normal and the displacement vector to the position we are checking.
                    float angle = acos(dot(normalPos, normalize(auxPosition - currPos)));

                    if (angle < prevAngle) {
                        // Compute the modulated contribution of the current pixel.
                        currAO -= (sin(prevAngle) - sin(angle)) * (1.0 - distance * distance);
                        prevAngle = angle;
                    }
                }
            }

            ao += currAO;
        }
        ao = ao / float(NUM_ROTATIONS);
        ao = pow(ao, 3.5);
        outColor = vec4(ao, ao, ao, 1.0) * colorPos;

    } else {
        // Background pixel
        outColor = vec4(1.0);
    }
}
