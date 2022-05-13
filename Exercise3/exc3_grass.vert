#version 330

uniform mat4 worldViewProjMatrix;
uniform float time;

in vec4 sPos;
in vec2 sTexCoords;

out vec2 texCoords;
out float scaleColor;

uint hash( uint x ) {
    x += ( x << 10u );
    x ^= ( x >>  6u );
    x += ( x <<  3u );
    x ^= ( x >> 11u );
    x += ( x << 15u );
    return x;
}
uint hash( uvec2 v ) { return hash( v.x ^ hash(v.y)                         ); }
float floatConstruct( uint m ) {
    const uint ieeeMantissa = 0x007FFFFFu; 
    const uint ieeeOne      = 0x3F800000u; 
    m &= ieeeMantissa;                     
    m |= ieeeOne;                          
    float  f = uintBitsToFloat( m );       
    return f - 1.0;                        
}
float random( vec2  v ) { return floatConstruct(hash(floatBitsToUint(v*100.0))); }

void main()
{    
    texCoords = sTexCoords;
    vec4 wind_direction = vec4(0.04, 0.0, 0.04, 0.0);

    float outputScaleColor = 1.0;
    vec4 position = sPos;
    
    scaleColor = outputScaleColor;
    gl_Position = worldViewProjMatrix*position;
}
