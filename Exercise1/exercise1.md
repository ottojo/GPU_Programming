# Exercise 1

## Creating your first shaders

Vertex shader `vertexShader.glsl` including the vertex transformation:

```glsl
#version 450
uniform mat4 worldViewProjMatrix;
in vec4 sPos;
in vec3 sNormal;
out vec3 normal;

void main() {
    normal = sNormal;
    gl_Position = worldViewProjMatrix * sPos;
}
```

## Shader description

The lecture example computed a color for each vertex by scaling the input color with the
dot product of the light direction and the vertex normal.
In the exercise, this calculation is moved to the pixel shader.
This might produce a different result as the pixel shader input may be interpolated between
multiple vertex shader outputs, and interpolating the normal is different from (and perhaps less
useful than) interpolating the vertex color.


> In which coordinate system the light is defined?

The light direction is specified in model space, since the dot product with the vertex normal is
used, which is also in model space.

> Will this implementation work if we have multiple instances of the same model?

Yes, if a separate `worldViewProjMatrix` is supplied for each model, multiple instances could be
displayed at different locations. The lighting calculations are not affected, as they operate in
model space.
