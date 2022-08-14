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
> **_TODO:_** Texturing

### Parallax + Relief Mapping
## Frame Buffers
### Ambient Occlusion
## SDFs
