# Exercise 8: Signed Distance Functions
## Create a cylinder

Since the cylinder SDF is already provided, it is sufficient to call it in `f()`:

```glsl
float f(vec3 samplePoint) {
  // Slowly spin the whole scene
  samplePoint = rotateY(iTime / 2.0) * samplePoint;

  return cylinderSDF(samplePoint, 4, 0.5);
}
```
## Deform the cylinder

To achieve a deformation similar to the one displayed in the example image,
the y-coordinate of the sample point is shifted.
The amount of displacement is animated using the current time and z-position
(which is the position along the axis of the cylinder):

```glsl

float f(vec3 samplePoint) {
  // Slowly spin the whole scene
  samplePoint = rotateY(iTime / 2.0) * samplePoint;

  // Deform and animate the cylinder
  samplePoint.y += sin(iTime - samplePoint.z * 1.5);

  return cylinderSDF(samplePoint, 4, 0.5);
}
```

## Add another cylinder

The cylinder SDF is evaluated twice, and combined using `unionSDF`.
The sample point for the second cylinder is rotated by 90°, and the animation is
adjusted to animate along the length of the cylinder, which is now the x instead
of z axis.

```glsl
#define M_PI 3.1415926535897932384626433832795

float f(vec3 samplePoint) {
  // Slowly spin the whole scene
  vec3 samplePoint1 = rotateY(iTime / 2.0) * samplePoint;
  // Second cylinder is rotated another 90deg
  vec3 samplePoint2 = rotateY(M_PI / 2) * samplePoint1;

  // Deform and animate the cylinder
  samplePoint1.y += sin(iTime - samplePoint.z * 1.5);
  // Second cylinder is rotated -> animate along x
  samplePoint2.y += sin(iTime - samplePoint.x * 1.5);

  float cylinder1 = cylinderSDF(samplePoint1, 4, 0.5);
  float cylinder2 = cylinderSDF(samplePoint2, 4, 0.5);

  return unionSDF(cylinder1, cylinder2);
}
```

## Visual artifacts

When using the output of our SDF `f(samplePoint)` directly as the step size,
artifacts appear.
This is because of the transformations we apply to the sample point in `f`,
which results in `f(p)` not being the correct distance between the object and
`p`, but the distance between the object and the transformed and (non uniformly)
scaled `samplePoint`.
This is not a problem for rendering, since the sign is still correct.
It is important however to not overestimate the step size, since this could lead
to missing geometry during raycasting.
The scaling of `f(p)` ensures the distance is never overestimated, and the step
size is never too large.
