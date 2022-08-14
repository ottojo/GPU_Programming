# Vertex Shader
The vertex shader is executed once for every vertex in the scene.
It can transform the position and attributes of these vertices,
and can perform per-vertex calculations such as lighting (which can also be done per-pixel, as explained later).
A possible use case for moving vertices is also animating objects in the scene.

## Input Data Structures
Input vertex data is in the form of primitives, which can be points, lines, triangles and quads.
Multiple triangles can be represented in different ways:

* Triangle List: Each triangle consists of three points. Adjacent triangles mean some points are stored twice.
* Triangle Strip: The stored points make up a triangle strip in a zig-zag pattern,
  from the bottom left towards the right.
  This way each additional triangle only requires one additional point, the last two points
  implicitly belong to the triangle.
* Indexed Triangles: This performs deduplication of vertices by storing each point once
  and defining triangles by the indices of the points.

  Input data is stored and uploaded in buffers, which can then be associated to (vertex-)shader inputs.

## Uniform Variables
Uniform variables have the same value for each invocation of the shader (for every vertex/pixel).
They are set by the CPU.

## Transformations
Coordinate transformations are an important task of the vertex shader.
We express transformations using homogeneous coordinates to allow translations.

$$
\begin{bmatrix}
p_x * s_x + t_x \\
p_y * s_y + t_y \\
p_z * s_z + t_z \\
1
\end{bmatrix}
=
\begin{bmatrix}
s_x & 0   & 0   & t_x \\
0   & s_y & 0   & t_y \\
0   & 0   & s_z & t_z \\
0   & 0   & 0   & 1
\end{bmatrix}
\begin{bmatrix}
p_x \\
p_y \\
p_z \\
1
\end{bmatrix}
$$
(add rotations to taste.)

Care has to be taken with normals, as those can change if geometry is non-uniformly scaled.
For a point $p$ and normal $n$ under the transformation $M$:
$$
p' = Mp \\
$$
$$
n'=(M^{-1})^Tn
$$

A similar transformation matrix can be constructed for a change of basis,
projecting a point onto new axes.
Combined with a translation (changing the origin), this performs a change of
coordinate system.

### Perspective Projection
In order for correct perspective handling, the camera frustum is transformed
into a cube centered at $(0,0,0)$ with side lengths 2.


> **_TODO:_** World view transformation#

## Sprites
Sprites are polygons that are always rotated towards the camera.
This is a cheap to render alternative to a complete model.
Implementing sprites can be done by storing the central point as well as
displacement vectors for the points making up the polygon.
In the shader, these displacements are applied such that the polygon is facing
the camera.
Multiple variants of the sprite can be stored which show the object from
different sides.

## Animation
The vertex shader can be used to show animations, by providing two vertex
positions for keyframes before and after the current time, and configuring the
vertex shader to interpolate between those and correctly move the vertex.
This can also be used to store multiple model configurations (such as facial
expressions) as offsets from the base model and *morphing* continuously between
them.

## Skinning
A common task is animating or moving some sort of skeleton with attached
geometry.
Each bone contains a transformation matrix relative to its parent.
Those transformations can now be animated, and vertices which are associated
to a specific bone can be moved accordingly.

Problems arise for vertices near multiple bones.
Rigidly associating those with a single bone results in intersecting or
stretched geometry.
This can be solved by assigning a continuous weight instead of a rigid
assignment for associating vertices with bones.
