# Exercise 7
## Horizon-based Screen Space Ambient Occlusion

The horizon angle is computed in multiple directions, as defined by `currentScreenVect`:

```glsl
for (int i = 0; i < NUM_ROTATIONS; i++) {
    // 2D ray in screen space
    vec2 currentScreenVect = rotationMatrix(i * augment) * initScreenVect;
```

Along this ray (in screen space), the world space position is sampled using the provided input texture:

```glsl
for (int j = 1; j <= NUM_SAMPLES_DIRECTION; j++) {
    // Get the current position along the ray.
    vec4 auxPosition = texture(posTex, uv + j * DISPLACEMENT * currentScreenVect);
```

The angle between the normal and the point along the ray is computed:

```glsl
// Compute the angle between the normal and the displacement vector
//  to the position we are checking.
float angle = acos(dot(normalPos, normalize(auxPosition - currPos)));
```

The minimum angle along each direction determines the occlusion in that direction, the occlusion values for each direction are averaged.

If the distance to the point along the ray exceeds a set maximum, it is clamped, which sets its contribution to the current ray occlusion to zero.

```glsl
// Compute the distance between the center point (currPos)
//  and the position we are checking.
float distance = length(auxPosition - currPos);
distance = min(MAX_EFFECT_DISTANCE, distance);
```
