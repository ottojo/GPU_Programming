import math
import numpy as np

import OpenGL
from OpenGL import GL

FLOAT_SIZE = 4
SHORT_SIZE = 2

class ShaderLoader:
    
    def __init__(self):
        pass

    def _link_(self, program):
        GL.glLinkProgram(program)

        status = GL.glGetProgramiv(program, GL.GL_LINK_STATUS)
        if not status:
            log = GL.glGetProgramInfoLog(program)
            raise RuntimeError("Linking failue: "+str(log))

    def _compile_(self, shaderPath, shaderCode, shaderType):
        shader = GL.glCreateShader(shaderType)

        GL.glShaderSource(shader, shaderCode)

        GL.glCompileShader(shader)

        status = GL.glGetShaderiv(shader,GL.GL_COMPILE_STATUS)
        if not status:
            log = GL.glGetShaderInfoLog(shader)
            raise RuntimeError("Compile failure in shader: "+shaderPath+ "\n "+str(log))

        return shader

    def _load_shader_code_(self, shaderPath):
        shaderCode = ""
        with open(shaderPath, 'r') as modelFile:        
            for line in modelFile:
                shaderCode += line
        return shaderCode
    
    def load_shader(self, shaderPathList, shaderTypes):
        currProgram = GL.glCreateProgram()

        shadeList = []
        for shaderPath, shaderType in zip(shaderPathList, shaderTypes):
            shadeList.append(self._compile_(shaderPath, 
                self._load_shader_code_(shaderPath), shaderType))
        
        for shade in shadeList:
            GL.glAttachShader(currProgram,shade)
        
        self._link_(currProgram)

        for shade in shadeList:
            GL.glDetachShader(currProgram,shade)
            GL.glDeleteShader(shade)

        return currProgram

    
class MeshRenderer:
    
    def __init__(self, verts, trians, elements, attribLoc):
        self.verts_ = verts
        self.trians_ = trians
        self.elements_ = elements
        self.attribLoc_ = attribLoc
        self._create_buffers_()
        self._init_vao_()

    def _create_buffers_(self):
        flattenVerts = self.verts_.tolist()
        self.vbo_ = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo_)
        ArrayType = (GL.GLfloat*len(flattenVerts))
        GL.glBufferData(GL.GL_ARRAY_BUFFER, len(flattenVerts)*FLOAT_SIZE,
                        ArrayType(*flattenVerts), GL.GL_DYNAMIC_DRAW)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER,0)

        flattenIndexs = self.trians_.tolist()
        self.ibo_ = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.ibo_)
        ArrayType = (GL.GLushort*len(flattenIndexs))
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, len(flattenIndexs)*SHORT_SIZE,
                        ArrayType(*flattenIndexs), GL.GL_STATIC_DRAW)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER,0)

    def _init_vao_(self):
        self.vao_ = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao_)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo_)
        vertexSize = 0
        for currElem in self.elements_:
            vertexSize += currElem
        accumVertexSize = 0
        for it, currElem in enumerate(self.elements_): 
            GL.glEnableVertexAttribArray(self.attribLoc_[it])
            GL.glVertexAttribPointer(self.attribLoc_[it], currElem, GL.GL_FLOAT, GL.GL_FALSE, 
                vertexSize*FLOAT_SIZE, GL.GLvoidp(accumVertexSize*FLOAT_SIZE))
            accumVertexSize += currElem
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.ibo_)
        GL.glBindVertexArray(0)

    def render_mesh(self):
        GL.glBindVertexArray(self.vao_)
        GL.glDrawElements(GL.GL_TRIANGLES, len(self.trians_), GL.GL_UNSIGNED_SHORT, None)
        GL.glBindVertexArray(0)


class Camera:

    def __init__(self, vrp, obs, upVec, ar, fov, zNear, zFar):
        self.vrp_ = np.array(vrp)
        self.obs_ = np.array(obs)
        self.upVec_ = np.array(upVec)
        self.ar_ = ar
        self.fov_ = fov
        self.zNear_ = zNear
        self.zFar_ = zFar


    def _normalize_(self, v):
        m = math.sqrt(np.sum(v ** 2))
        if m == 0:
            return v
        return v / m


    def rotate_y(self, angle):
        cosVal = np.cos(angle)
        sinVal = np.sin(angle)
        T = np.array([[cosVal, 0.0, -sinVal],
                       [0.0, 1.0, 0.0],
                       [sinVal, 0.0, cosVal]])
        auxPos = self.obs_ - self.vrp_
        auxPos = np.dot(T, auxPos)[:3]
        self.obs_ = auxPos + self.vrp_


    def rotate_x(self, angle):
        F = self.vrp_ - self.obs_
        f = self._normalize_(F)
        U = self._normalize_(self.upVec_)
        axis = np.cross(f, U)
        
        x, y, z = self._normalize_(axis)
        s = math.sin(-angle)
        c = math.cos(-angle)
        nc = 1 - c
        T = np.array([[x*x*nc +   c, x*y*nc - z*s, x*z*nc + y*s],
                        [y*x*nc + z*s, y*y*nc +   c, y*z*nc - x*s],
                        [x*z*nc - y*s, y*z*nc + x*s, z*z*nc +   c]])
                        

        auxPos = self.obs_ - self.vrp_
        auxPos = np.dot(T, auxPos)
        self.obs_ = auxPos + self.vrp_


    def get_view_natrix(self):
        F = self.vrp_ - self.obs_
        f = self._normalize_(F)
        U = self._normalize_(self.upVec_)
        s = self._normalize_(np.cross(f, U))
        u = self._normalize_(np.cross(s, f))
        M = np.matrix(np.identity(4))
        M[:3,:3] = np.vstack([s,u,-f])
        T = np.matrix([[1.0, 0.0, 0.0, -self.obs_[0]],
                       [0.0, 1.0, 0.0, -self.obs_[1]],
                       [0.0, 0.0, 1.0, -self.obs_[2]],
                       [0.0, 0.0, 0.0, 1.0]])
        return  M * T


    def get_projection_matrix(self):
        s = 1.0/math.tan(math.radians(self.fov_)/2.0)
        sx, sy = s / self.ar_, s
        zz = (self.zFar_+self.zNear_)/(self.zNear_-self.zFar_)
        zw = (2*self.zFar_*self.zNear_)/(self.zNear_-self.zFar_)
        return np.matrix([[sx,0,0,0],
                        [0,sy,0,0],
                        [0,0,zz,zw],
                        [0,0,-1,0]])