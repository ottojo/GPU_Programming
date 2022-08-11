---
title: GPU Programming
author: Jonas Otto
date: August 2022
lang: en
---

# Overview: Graphics Pipeline
The graphics pipeline running on the GPU consists of multiple consecutive stages, some of which are programmable.
The focus in this lecture is on those programmable Stages, and how to program these using GLSL shaders.

The basic pipeline consists of
* Vertex Shader
* Tesselation
  * Control
  * Evaluation
* Geometry Shader
* Fragment Shader

Additionally, compute shaders can perform arbitrary computation and can be used in various stages of the pipeline,
or without using the graphics pipeline at all.

# Vertex Shader
The vertex shader is executed once for every vertex in the scene.
It can transform the position and attributes of these vertices,
and can perform per-vertex calculations such as lighting (which can also be done per-pixel, as explained later).
A possible use case for moving vertices is also animating objects in the scene.

# Pixel Shader
The pixel shader (fragment shader) runs after rasterization, for every pixel.
Its output is the desired color of the pixel, the inputs are the outputs of the previous stages.

## Rasterization
## Z-Buffer
## Lighting
### Lambertian Reflectance Model
### Phong Reflectance Model
### Blinn-Phong Reflectance Model
## Texturing
## Frame Buffers
## SDFs

# Geometry Shader
## Example: Normal visualization
## Example: Shadow volumes

# Tessellation Shader

# Advanced GLSL
## Transform Feedback
## Uniform Buffer Objects
## Shader Storage Buffer Objects

# GPU Architecture
## Processor Architecture
## Thread Divergence
## Memory

# Compute Shader

# Cuda

## Synchronization
## Concurrency: Streams
