# Geometry Shader
The geometry shader is located between the vertex- and pixel shader in our pipeline.
It is executed once for every geometric primitive.

## Inputs and Outputs
Primitives for use in the geometry shader are

* Points
* Lines
* Triangles

As well as lines and triangles with adjacency information.
The input is defined in the shader as
```glsl
layout (triangles) in;
```

The output of the geometry stage can be

* Points
* Line strips
* Triangle strips

And is defined in the shader as
```glsl
layout (triangle_strip, max_vertices = 3) out;
```

The `max_vertices` parameter is required to specify the maximum number of vertices
that the shader may output.

The geometry shader receives inputs just as any other shader, but since it processes
a primitive instead of a single vertex, the inputs will be arrays containing
each input for each of the vertices making up the primitive.

The usual `gl_Position` output from the vertex shader is available at
`gl_in[i].gl_Position`. Additional inputs are available to receive an ID of the
current primitive and shader invocation.

Outputs do not become arrays, we instead call `EmitVertex()` to emit the output
variables for each vertex one after another.
Once all vertices have been output, we call `EndPrimitive()`.

## Geometry Generation Example: Normal visualization
The geometry shader can also generate new geometry.
This is explained here with an example in which a steep pyramid shall be generated
in the middle of each triangle, visualizing its normal.

This requires generating four output triangles from one input triangle primitive
(the original triangle as well as all three sides of the pyramid).
To accomplish this, the `max_vertices` parameter is increased to 12.
The triangles are output individually (not as a triangle strip), and
`EndPrimitive()` is thus called four times in the shader.

Another example given is the billboard example for molecule visualization,
with the difference being that the vertices for the displaced billboard corners
are not generated on the CPU, but created in the geometry shader.

An example for the adjancency feature of the input is given by the application of
creating borders around a model:
The input data now consists of six vertices per triangle, containing not only
the current triangle but also the remaining vertices of the three triangles that
share an edge with the current triangle.

## Shadow volumes
A way of generating shadows is to produce geometry representing the projection
of our objects based on the light position (the shaded volume). When rendering,
we can check if a point is inside a shadow volume or not.

Using triangle adjacency, the contour edges of an object with respect to the light
(instead of the camera, like in the "borders" example) can be found.
These edges are then used to create a side of the shadow volume.

The process of rendering shadows using shadow volumes is as follows:

1. Render the scene using only ambient lighting, filling the Z-buffer
2. Render the shadow volumes using the geometry shader, storing the results in a
   "mask buffer". This way the geometry does not need to be explicitly stored.
   This is basically counting the number of front- and back-facing sides of the
   shadow volumes between the camera and object. If there are the same number of
   front- and back-facing sides, the object is not in shadow.
3. Render the scene again, updating only pixels which are not marked in the mask
   using diffuse and specular lighting 

Shadow volumes produce higher resolution (sharper) shadows than shadow-mapping,
at the cost of more expensive computation.

## Layered rendering
Another feature of the geometry shader is rendering the same object to multiple
images in one draw-call.

The geometry shader can calculate the projection of each object into multiple
camera configurations. The pixel shader is then executed for each of those images.
An example where this is needed is a CUBE map, where the scene is rendered into
the six faces of a cube.

In the geometry shader, before `EmitVertex()` we can update `gl_Layer` to select
which layer of the current texture we want to render to.
It is also not required to loop over layers in the shader, instead *instancing*
can be used to execute the shader more than once for every primitive.
The number of incocations is specified in the shader:

```glsl
layout (invocations = 16, points) in;
```
