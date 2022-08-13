# Tessellation Shader

Tessellation produces a more detailed model from a model with less triangles.
The tessellation shader allows us to subdivide triangles based on the distance
to the camera or other parameters.

In order to perform this tessellation, not one but two additional stages are 
introduced between the vertex- and geometry shader:
The Tessellation Control Shader and the Tessellation Evaluation Shader.

The Tessellation Control Shader is executed once for each vertex of the input
primitives. Its goal is to determine the tessellation level, or how much the
triangle should be subdivided.

The Tessellation Evaluation Shader  is executed once for each new vertex that
was created after subdivision. Its goal is to move the new vertex to the correct
position.

Actually generating the new primitives and vertices is done by the GPU hardware,
we can only configure that step using the control shader.

## Subdivision Patterns
Multiple subdivision patterns are available:

* Triangles: Smaller triangle inside triangle
* Quads: Smaller quads in quad
* Quads Isolines: Parallel lines (with midpoints) along one axis inside the quad

## Tessellation Control Shader
The goal of the TCS is to generate control points (inputs into subdivision:
three for triangles, four for quads) and to define the tessellation levels.

This shader is executed once for each output control point, but all executions
for the same patch are connected: They share the same output and can use
synchronization.

### Tessellation levels
For triangles, there is an *inner tessellation level* and three *outer tessellation levels*.
The inner tessellation level is applied first and controls how many inner
triangles are created (by dividing all outer lines into $n$ segments, with inner
tessellation level $n$). Then, the outer tessellation levels specify how many
segments each of the original outer lines should actually end up with.

The outer tessellation level is needed to correctly process adjacent triangles,
which may have different inner tessellation levels.

Usually, tessellation levels are dynamically calculated based on how far the
object is from the camera!

Tessellation of quads can be similarly controlled, although now there are four
outer tessellation levels and two inner tessellation levels (one for each axis).

Isolines require just two outer tessellation levels.

### Inputs
Some inputs are again provided in a `gl_in[]`, providing for example the vertex
positions. `gl_InvocationID` provides the ID of the vertex inside the current
primitive (indexing `gl_in`), and `gl_PrimitiveID` identifies the primitive.
`gl_PatchVerticesIn` contains the number of vertices in the current patch.

Custom shader inputs can be used as usual, in array form like in the geometry
shader.

### Outputs
`gl_out[i].gl_Position` contains the vertex position as usual, the tessellation
level as described above has to be written to `gl_TessLevelOuter[4]` and
`gl_TessLevelInner[2]`.

Custom outputs for the TES are per control point by default, but can be specified
to be per primitive using
```glsl
patch out vec3 customVar;
```

### Synchronization
TCS instantiations can read outputs from other instantiations belonging to the
same patch. This requires synchronization, which is provided by the `barrier()`
function, ensuring that all executions have written their outputs.

## Tessellation Evaluation Shader 

### Inputs + Outputs
The TES is executed for each new vertex.
It receives the barycentric coordinates of each vertex in the original triangle
as input, and interpolates the new position for the vertex:
`gl_in[i].gl_Position` contains the positions of the patch control points,
`gl_TessCoord` contains the barycentric coordinates of the current vertex.

The only required output is the position `gl_Position` of the vertex.

### Barycentric Coordinates

The order and spacing-mode of tesselation are specified:
```glsl
layout (triangles, equal_spacing, ccw) in;
```

Multiple spacing modes such as `equal_spacing`, `fractional_even_spacing` and
`fractional_even_spacing` are available.
The barycentric coordinates provides the vertex position as a weighted sum of
the control point positions.

For quads and isolines, the coordinates are given as $uv$ coordinates inside the
original quad.

## Advanced Application: Bezier Curves

An isolines tessellation with the first tessellation level being 1, a bezier
curve is rendered. The second tessellation level specifies the number of
segments in the curve.

The TES calculates the position of each vertex by evaluating the bezier curve
along the second axis of the quad (the one with varying tessellation level).

This can be extended to bezier surfaces using quad tessellation.
