# Exercise 5
## Normal computation

By calculating the partial derivatives of the world space position
of the vertex, we obtain two vectors tangential to the model surface.
Using the cross product, the surface normal is calculated:

```glsl
// Compute the normal
vec3 v1 = dFdx(position);
vec3 v2 = dFdy(position);
vec3 normalizedNormal = normalize(cross(v1, v2));
```

## Shadows

First, the light direction is transformed to tangent space, with z=up instead
of y=up:
```glsl
// Compute the transformation matrix to go from world space to tangent space.
//  y and z cols/rows are switched compared to lecture, we want z=up
mat3 transMat = mat3(tangent.x,  binormal.x, normal.x,
                     tangent.z,  binormal.z, normal.z,
                     tangent.y,  binormal.y, normal.y);
```

Then, a linear seach is performed along the light ray for geometry obsructing
the path between light source and current position:
```glsl
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
```
