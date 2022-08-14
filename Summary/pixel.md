# Pixel Shader
The pixel shader (fragment shader) runs after rasterization, for every pixel.
Its output is the desired color of the pixel, the inputs are the outputs of the previous stages.

## Rasterization
## G-Buffer
## Z-Buffer

## Lighting

### Types of Light

* Directional light: Parallel light rays, used for example for the sun
* Point light: Light rays originate from single point in space
* Spot light: Rays originate from single point in a specific direction

### Surface Interaction
On each point on a surface, light gets refracted (entering the surface,
changing its direction) and reflected. The roughness of a surface changes how
much the direction of reflected light varies.
Surface materials are roughly grouped into metals, which only reflect light,
and non-metals which involve refraction and subsurface scattering.
To approximate scattering, we consider two types of reflected light:
specular and diffuse light. The specular light is almost entirely reflected in
the same angle as the incoming light, depending on the surface roughness.
The diffuse light exits at a more uniform distribution of directions.

The material properties are defined by the Bidirectional Reflectance
Distribution Function *BRDF*, $f(l,v)$, taking the input and output directions
and modeling how much light is reflected in the specified output direction.

In the following, simple BRDFs are presented.

### Lambertian Reflectance Model
This simulates perfectly diffuse surface, light is reflected equally in each
direction. It models the amount of reflected light depending on incident angle.

$$
I_d = (N \cdot L) * C_d * k_d
$$
With surface normal $N$, light direction $L$, light color $C_d$ and object color
$k_d$.

Light attenuation is used to simulate decrease in light intensity depending on
distance $d$ to the source:

$$
L_p = \frac{L_i}{At_c + At_l * d + At_e * d^2}
$$
with constant component $At_c$, linear component $At_l$ and exponential
component $At_e$

### Phong Reflectance Model
The Phong reflectance model adds ambient and specular lighting.
The ambient light is simulated to be constant:
$$
I_a = C_a * k_a
$$

The diffuse light is simulated using the Lambertian model:
$$
I_d = (N \cdot L) * C_d * k_d
$$

The specular light is introduced based on the dot product between the view
vector $V$ and the reflect vector (direction of reflected light) $R$:
$$
I_s = (V \cdot R) ^ \alpha * C_s * k_s
$$
The parameter $\alpha$ controls the roughness of the object.

A problem occurs if the angle between $R$ and $V$ is greater than 90°, leading
to a negative value for $V \cdot R$. This is solved by the Blinn-Phong model.

### Blinn-Phong Reflectance Model
Here, the specular term is calculated using the surface normal and the newly
introduced $H$ vector, instead of the view vector.
The $H$ vector is the sum of the view- and light vector.
This results in a dot product that is always positive:
$$
I_s = (N \cdot H) ^ \alpha * C_s * k_s
$$

### General Considerations
The final lighting is dependent on where lighting is computed, and how normals
are computed.
Using normals per vertex, instead of per triangle, allows for interpolation
and smoother lighting.
Computing lighting per pixel (interpolating normals), instead of per vertex
(interpolating lighting), produces better results.

## Texturing
Instead of using a constant material color when calculating lighting, we can
query a texture. The texture is mapped to a coordinate space from $(0,0)$ to
$(1,1)$ ($s t$ texture coordinates). Each vertex now has an additional $(s,t)$
texture coordinate.

### Mipmapping
Aliasing artifacts can occur when textured objects appear on different scales
in the scene. This is solved by storing the texture in multiple (correctly 
down-scaled) sizes, and using a smaller texture for far away objects.

### Anisotropic Filtering
Since a square screen pixel may not map nicely to a single texture pixel, OpenGL
provides anisotropic filtering, which queries multiple texture pixels to improve
this behavior.

### Specular Textures
Specular lighting should also be affected by the texture.
We introduce a separate texture that provides the color for the specular color.
This can also be a one-channel texture just specifying how much light should be
reflected.

### Problems with Textures
Photo textures already contain illumination information for a specific condition.
Instead, textures should be used which only contain the material properties.
For this to look good however, we need to simulate the lighting (such as small
shadows) which previously was present (but static) in the texture.
This is done by storing geometric information in the texture, such as the normal
map in the next section.

### Normal Mapping
An additional texture is created containing the normal direction at each texel
position.
This allows light computation as if a more detailed surface structure was
present, without actually modifying the geometry, by querying the normal map
texture in the pixel shader.

Care has to be taken to transform the normal from texture space into the
coordinate system in which the light is defined (world space).
This requires defining a new coordinate frame for each surface on which a
texture is applied.
The vertex data can be appended by a tangent and binormal vector defining the
directions of the texture $s$ and $t$ axes.

### Parallax + Relief Mapping
To correctly render textures more detailed, including occlusions within the
texture, more effort has to be made.
One option is displacement mapping: The idea is to use a highly tessellated
surface, and use a height map or displacement texture to displace the vertices
in the vertex shader.
This works, but is not scalable since it requires generating a large amount of
additional vertices.

An alternative technique, not requiring additional vertices, is
*Parallax Mapping*.
This technique assumes a locally constant surface height, and chooses a
different texel to use in the pixel shader depending on the angle between the
surface and view vector.
If the height at the original texel $(u,v)$ is $h$, the view vector intersects
the point $h$ above the new texel $(u',v')$.

This technique produces suboptimal results especially for shallow viewing
angles.
Another technique is presented by *Parallax Mapping*:

In parallax mapping, the texel is always displaced by the height at the original
texel.
This may not be a very accurate approximation, but is free of the artifacts
at shallow viewing angles.

### More Accurate Surface Rendering using Ray Intersections
> **_TODO:_** texturing 2

## Frame Buffers
### Ambient Occlusion
## SDFs
