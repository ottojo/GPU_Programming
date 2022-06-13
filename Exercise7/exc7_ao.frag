#version 440

uniform sampler2D posTex;
uniform sampler2D normalTex;
uniform sampler2D colorTex;

in vec2 uv;

out vec4 outColor;

#define NUM_ROTATIONS 25
#define NUM_SAMPLES_DIRECTION 20
#define DISPLACEMENT 0.0025
#define PI 3.14159265359
#define MAX_EFFECT_DISTANCE 1.0



void main()
{
    vec4 currPos = texture(posTex, uv);
    vec4 normalPos = texture(normalTex, uv);
    vec4 colorPos = texture(colorTex, uv);
    
    if(currPos.w > 0.0){
        vec2 initScreenVect = vec2(1.0, 0.0);
        float ao = 0.0;
        float augment = PI*2.0/float(NUM_ROTATIONS);

        for(int i = 0; i < NUM_ROTATIONS; i++)
        {
            // TODO - Rotate along the circle and compute the orientation vector in screen space each iteration.

            float prevAngle = PI/2.0;
            float currAO = 1.0;

            for(int j = 1; j <=NUM_SAMPLES_DIRECTION; j++)
            {
                // TODO - Get the current position along the ray.
                //vec4 auxPosition = ...;

                // TODO - Check that it is not a background pixel.
                //if(...){

                    // TODO - Compute the distance between the center point (currPos) and the position we are checking.
                    float distance = 0.0f;

                    // TODO - Compute the angle between the normal and the displacement vector to the position we are checking.
                    float angle = PI/2.0;

                    if(angle < prevAngle){
                        //Compute the modulated contribution of the current pixel.
                        currAO -= (sin(prevAngle) - sin(angle))*(1.0-distance*distance);
                        prevAngle = angle;
                    }
                //}
            }

            ao += currAO;
        }
        ao = ao/float(NUM_ROTATIONS);
        ao = pow(ao, 3.5);
        outColor =  vec4(ao, ao, ao, 1.0)*colorPos;
    }else{
        outColor =  vec4(1.0);
    }
    
}
