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
