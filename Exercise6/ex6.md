# Exercise 6
## Displacement mapping - Binary search

A utility function is implemented to check if a point along the ray is below the surface:
```glsl
bool belowSurface(float currH, vec2 stin, vec2 stout) {
  vec2 newTexCoords = stin * currH + stout * (1.0 - currH);
  float height = texture(dispTexture, newTexCoords).r;
  if (currH <= height) {
    return true;
  }
  return false;
}
```

This is then used to implement the binary search algorithm:
```glsl
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
```

## Displacement mapping - Relief mapping

Combination of linear and binary search combines benefits of good performance and accuracy.
Different iteration limits are defined:

```glsl
#define MAX_ITER_LINEAR 50
#define MAX_ITER_BINARY 10
```

The linear search runs first and determines a rough interval around the intersection:

```glsl
// Binary search interval
float hMin = 1.0;
float hMax = 0.0;

// Linear search from h=1 (stin) towards h=0 (stout)
for (int i = 0; i < MAX_ITER_LINEAR; ++i) {
  currH -= 1.0 / float(MAX_ITER_LINEAR);
  if (belowSurface(currH, stin, stout)) {
    // First point below surface -> Binary search
    hMin = currH;
    break;
  }
  hMax = currH;
}
```

Then, binary search refines the solution within this interval:

```glsl
for (int i = 0; i < MAX_ITER_BINARY; i++) {
  float middle = hMin + 0.5 * (hMax - hMin);
  if (belowSurface(middle, stin, stout)) {
    hMin = middle;
  } else {
    hMax = middle;
  }
}

intersection = hMin + 0.5 * (hMax - hMin);
```
