# Exercise 9: Geometry Shader
## 2: Move triangle along the normal

To move all the triangles along the normal direction, the displacement vector is
added to both the `gl_Position` (before projection) and the `gsposition`
outputs:

```glsl
#version 430 core
layout(triangles) in;
layout(triangle_strip, max_vertices = 3) out;

uniform mat4 worldViewProjMatrix;

out vec3 gsposition;
out vec3 gsnormal;

void main() {
  vec3 vect1 = normalize(gl_in[1].gl_Position.xyz - gl_in[0].gl_Position.xyz);
  vec3 vect2 = normalize(gl_in[2].gl_Position.xyz - gl_in[0].gl_Position.xyz);
  vec3 normal = normalize(cross(vect1, vect2));

  vec4 disp = 0.5 * vec4(normal.x, normal.y, normal.z, 0);

  gl_Position = worldViewProjMatrix * (gl_in[0].gl_Position + disp);
  gsposition = gl_in[0].gl_Position.xyz + disp.xyz;
  gsnormal = normal;
  EmitVertex();

  gl_Position = worldViewProjMatrix * (gl_in[1].gl_Position + disp);
  gsposition = gl_in[1].gl_Position.xyz + disp.xyz;
  gsnormal = normal;
  EmitVertex();

  gl_Position = worldViewProjMatrix * (gl_in[2].gl_Position + disp);
  gsposition = gl_in[2].gl_Position.xyz + disp.xyz;
  gsnormal = normal;
  EmitVertex();

  EndPrimitive();
}
```

## 3: Subdivide triangles

For subdivision of the triangle, the `max_vertices` limit is increased to 5:
In addition to the new vertex, the first vertex has to be duplicated in order to
complete the triangle strip.

```glsl
#version 430 core
layout(triangles) in;
layout(triangle_strip, max_vertices = 5) out;

uniform mat4 worldViewProjMatrix;

out vec3 gsposition;
out vec3 gsnormal;

void main() {
  vec3 vect1 = normalize(gl_in[1].gl_Position.xyz - gl_in[0].gl_Position.xyz);
  vec3 vect2 = normalize(gl_in[2].gl_Position.xyz - gl_in[0].gl_Position.xyz);
  vec3 normal = normalize(cross(vect1, vect2));

  gl_Position = worldViewProjMatrix * gl_in[0].gl_Position;
  gsposition = gl_in[0].gl_Position.xyz;
  gsnormal = normal;
  EmitVertex();

  gl_Position = worldViewProjMatrix * gl_in[1].gl_Position;
  gsposition = gl_in[1].gl_Position.xyz;
  gsnormal = normal;
  EmitVertex();

  vec4 disp = 0.5 * vec4(normal.x, normal.y, normal.z, 0);
  vec4 center =
      (gl_in[0].gl_Position + gl_in[1].gl_Position + gl_in[2].gl_Position) / 3 +
      disp;
  gl_Position = worldViewProjMatrix * center;
  gsposition = center.xyz;
  gsnormal = normal;
  EmitVertex();

  gl_Position = worldViewProjMatrix * gl_in[2].gl_Position;
  gsposition = gl_in[2].gl_Position.xyz;
  gsnormal = normal;
  EmitVertex();

  // Emit first vertex again, to complete triangle strip
  gl_Position = worldViewProjMatrix * gl_in[0].gl_Position;
  gsposition = gl_in[0].gl_Position.xyz;
  gsnormal = normal;
  EmitVertex();

  EndPrimitive();
}
```

## 4: Compute correct normals

In order to assign the same normal to each vertex of the three new sides,
`max_vertices` is set to 9.
Three separate primitives of three vertices (with the same normal) each are
output:

```glsl
#version 430 core
layout(triangles) in;
layout(triangle_strip, max_vertices = 9) out;

uniform mat4 worldViewProjMatrix;

out vec3 gsposition;
out vec3 gsnormal;

void main() {
  // Input triangle verticies
  vec4 v0 = gl_in[0].gl_Position;
  vec4 v1 = gl_in[1].gl_Position;
  vec4 v2 = gl_in[2].gl_Position;

  // Triangle sides
  vec3 vect1 = normalize(gl_in[1].gl_Position.xyz - gl_in[0].gl_Position.xyz);
  vec3 vect2 = normalize(gl_in[2].gl_Position.xyz - gl_in[0].gl_Position.xyz);
  vec3 vect3 = normalize(gl_in[2].gl_Position.xyz - gl_in[1].gl_Position.xyz);

  // Normal of the input triangle
  vec3 origNormal = normalize(cross(vect1, vect2));

  vec4 disp = 0.5 * vec4(origNormal.x, origNormal.y, origNormal.z, 0);
  vec4 center = (v0 + v1 + v2) / 3 + disp;

  // Output triangle normals
  vec3 n1 = normalize(cross(vect1, normalize(center.xyz - v0.xyz)));
  vec3 n2 = normalize(cross(vect3, normalize(center.xyz - v1.xyz)));
  vec3 n3 = normalize(cross(normalize(center.xyz - v0.xyz), vect3));

  // Triangle 1
  gl_Position = worldViewProjMatrix * gl_in[0].gl_Position;
  gsposition = gl_in[0].gl_Position.xyz;
  gsnormal = n1;
  EmitVertex();

  gl_Position = worldViewProjMatrix * gl_in[1].gl_Position;
  gsposition = gl_in[1].gl_Position.xyz;
  gsnormal = n1;
  EmitVertex();

  gl_Position = worldViewProjMatrix * center;
  gsposition = center.xyz;
  gsnormal = n1;
  EmitVertex();

  EndPrimitive();

  // Triangle 2
  gl_Position = worldViewProjMatrix * gl_in[1].gl_Position;
  gsposition = gl_in[1].gl_Position.xyz;
  gsnormal = n2;
  EmitVertex();

  gl_Position = worldViewProjMatrix * gl_in[2].gl_Position;
  gsposition = gl_in[2].gl_Position.xyz;
  gsnormal = n2;
  EmitVertex();

  gl_Position = worldViewProjMatrix * center;
  gsposition = center.xyz;
  gsnormal = n2;
  EmitVertex();

  EndPrimitive();

  // Triangle 3
  gl_Position = worldViewProjMatrix * gl_in[2].gl_Position;
  gsposition = gl_in[2].gl_Position.xyz;
  gsnormal = n3;
  EmitVertex();

  gl_Position = worldViewProjMatrix * gl_in[0].gl_Position;
  gsposition = gl_in[0].gl_Position.xyz;
  gsnormal = n3;
  EmitVertex();

  gl_Position = worldViewProjMatrix * center;
  gsposition = center.xyz;
  gsnormal = n3;
  EmitVertex();

  EndPrimitive();
}
```