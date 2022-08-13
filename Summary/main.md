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
* Tessellation
  * Control
  * Evaluation
* Geometry Shader
* Fragment Shader

Additionally, compute shaders can perform arbitrary computation and can be used in various stages of the pipeline,
or without using the graphics pipeline at all.
