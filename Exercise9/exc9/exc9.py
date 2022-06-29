import moderngl
from pathlib import Path
import numpy as np
import math
from PIL import Image
import os

from gpuproglib import WindowInterface, run_interface, Camera

def local(*path):
    return os.path.join(os.path.dirname(__file__), *path)

def create_plane():

    rendVerts = []
    
    rendVerts.append(-1.0)
    rendVerts.append(0.0)
    rendVerts.append(0.0)
    rendVerts.append(1.0)
    
    rendVerts.append(0.0)
    rendVerts.append(0.0)
    rendVerts.append(1.0)
    rendVerts.append(1.0)
    
    rendVerts.append(0.0)
    rendVerts.append(1.0)
    rendVerts.append(0.0)
    rendVerts.append(1.0)
    
    rendVerts.append(0.0)
    rendVerts.append(0.0)
    rendVerts.append(1.0)
    rendVerts.append(1.0)
    
    rendVerts.append(1.0)
    rendVerts.append(0.0)
    rendVerts.append(0.0)
    rendVerts.append(1.0)
    
    rendVerts.append(0.0)
    rendVerts.append(1.0)
    rendVerts.append(0.0)
    rendVerts.append(1.0)
    
    rendVerts.append(1.0)
    rendVerts.append(0.0)
    rendVerts.append(0.0)
    rendVerts.append(1.0)
    
    rendVerts.append(0.0)
    rendVerts.append(0.0)
    rendVerts.append(-1.0)
    rendVerts.append(1.0)
    
    rendVerts.append(0.0)
    rendVerts.append(1.0)
    rendVerts.append(0.0)
    rendVerts.append(1.0)
    
    rendVerts.append(0.0)
    rendVerts.append(0.0)
    rendVerts.append(-1.0)
    rendVerts.append(1.0)
    
    rendVerts.append(-1.0)
    rendVerts.append(0.0)
    rendVerts.append(0.0)
    rendVerts.append(1.0)
    
    rendVerts.append(0.0)
    rendVerts.append(1.0)
    rendVerts.append(0.0)
    rendVerts.append(1.0)
    
    renderIndexs = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    
    coordMin = np.array([-1.0, 0.0, -1.0])
    coordMax = np.array([1.0, 1.0, 1.0])
    
    return np.array(rendVerts), np.array(renderIndexs), coordMin, coordMax


class Exc9(WindowInterface):
    def __init__(self):
        self.ctx = moderngl.create_context()
        vs_path = Path.cwd() / 'exc9.vert'
        geo_path = Path.cwd() / 'exc9.geom'
        fs_path = Path.cwd() / 'exc9.frag'

        self.prog = self.ctx.program(
            vertex_shader=vs_path.read_text(),
            geometry_shader=geo_path.read_text(),
            fragment_shader=fs_path.read_text()
        )
        
        self.mvp = self.prog['worldViewProjMatrix']
        self.lightDir = self.prog['lightDirection']
        self.inObjColor = self.prog['inObjColor']
        self.inLightColor = self.prog['inLightColor']
        self.camPos = self.prog['camPos']
        
        rendVert, rendFaces, coordMin, coordMax = create_plane()

        self.vbo = self.ctx.buffer(rendVert.astype('f4').tobytes())
        self.ibo = self.ctx.buffer(rendFaces.astype('i4').tobytes())
        self.vao = self.ctx.vertex_array(self.prog, [(self.vbo, '4f', 'sPos')], self.ibo)
        
        aabbSize = math.sqrt(np.sum((coordMax-coordMin) ** 2))
        self.camera = Camera(
                [0.0, 0.5, 0.0], 
                [0.0, 0.0, aabbSize*1.5], 
                [0.0, 1.0, 0.0],
                float(self.WINDOW_SIZE[0])/float(self.WINDOW_SIZE[1]),
                45.0, 0.1, aabbSize*5.0)
        self.viewMat = self.camera.get_view_natrix()
        self.projMat = self.camera.get_projection_matrix()
        self.worldViewProjMat = self.projMat * self.viewMat
        
        self.lastRotated_ = False
        self.mouse = (0.0, 0.0)
        
        self.lightDir_ = np.array([1.0, 0.0, 0.5])
        self.objColor_ = np.array([1.0, 0.0, 0.0, 1.0])
        self.lightColor_ = np.array([1.0, 1.0, 1.0, 1.0])
        
        
    def render(self):
        self.ctx.viewport = self.wnd.viewport
        if self.wnd.mouse_pressed and self.lastRotated:
            self.camera.rotate_x((self.wnd.mouse[1]-self.mouse[1])/500.0)
            self.camera.rotate_y((self.wnd.mouse[0]-self.mouse[0])/500.0)
            self.viewMat = self.camera.get_view_natrix()
            self.worldViewProjMat = self.projMat * self.viewMat
        self.mouse = self.wnd.mouse
        self.lastRotated = self.wnd.mouse_pressed
        
        if self.wnd.keys[0x25] == True:
            self.lightDir_[0] += 0.01
        if self.wnd.keys[0x27] == True:
            self.lightDir_[0] -= 0.01
        
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.ctx.clear(1.0, 1.0, 1.0)
        self.mvp.write(self.worldViewProjMat.transpose().astype('f4').tobytes())
        
        self.lightDir.write(self.lightDir_.astype('f4').tobytes())
        self.camPos.write(self.camera.obs_.astype('f4').tobytes())
        self.inObjColor.write(self.objColor_.astype('f4').tobytes())
        self.inLightColor.write(self.lightColor_.astype('f4').tobytes())
        
        self.vao.render()


if __name__ == '__main__':
    run_interface(Exc9)
