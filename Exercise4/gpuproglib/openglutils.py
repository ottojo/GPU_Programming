import math
import numpy as np

import OpenGL
from OpenGL import GL

FLOAT_SIZE = 4
SHORT_SIZE = 2

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