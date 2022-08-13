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
We express transformations using homogenous coordinates to allow translations.

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

> **_TODO:_** Change of coordinate system matrix
