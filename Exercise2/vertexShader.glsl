#version 450

uniform mat4 worldViewProjMatrix;
uniform float time;

in vec4 sPos;
in vec3 sNormal;

out vec3 normal;

mat3 rotMat_z(float angle_rad) {
    float r = angle_rad;
    return mat3(cos(r),  sin(r), 0,
                -sin(r), cos(r), 0,
                0,       0,      1);
}

void main()
{
    float height = 0.1;
    float frequency = 10;

    float y_offset = height * sin(sPos.x * frequency + time);

    mat4 transformation =  mat4(1, 0,        0, 0,
                                0, 1,        0, 0,
                                0, 0,        1, 0,
                                0, y_offset, 0, 1);

    gl_Position = worldViewProjMatrix * transformation * sPos;

    float deriv = height * frequency * cos(sPos.x * frequency + time);
    float alpha = atan(deriv);
    mat3 normal_rotation = rotMat_z(alpha);

    normal = normal_rotation * sNormal;
}
