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