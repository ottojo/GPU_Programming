import moderngl
from pathlib import Path
import numpy as np
import math
from PIL import Image
import os

import time
current_milli_time = lambda: time.time() * 1000.0

from gpuproglib import WindowInterface, run_interface, Camera

def local(*path):
    return os.path.join(os.path.dirname(__file__), *path)

def create_plane():
  
    # Top Face
    # Vert1
    rendVert = []
    for i in range(250):
        for j in range(250):
            rendVert.append(-2.0*(float(i)/250.0)+1.0)
            rendVert.append(0.0)
            rendVert.append(2.0*(float(j)/250.0)-1.0)
            rendVert.append(1.0)
            rendVert.append((1.0/249.0)*float(j)*5.0)
            rendVert.append((1.0/249.0)*float(i)*5.0)
    rendVert = np.array(rendVert)
    
    coordMin = np.array([-1.0, 0.0, -1.0])
    coordMax = np.array([1.0, 0.0, 1.0])
    
    rendFaces = []
    for i in range(249):
        for j in range(249):
            rendFaces.append(i*250 + j)
            rendFaces.append((i+1)*250 + 1 + j)
            rendFaces.append((i+1)*250 + j)
            rendFaces.append(i*250 + j)
            rendFaces.append(i*250 + 1 + j)
            rendFaces.append((i+1)*250 + 1 + j)      
    rendFaces = np.array(rendFaces)
    
    return rendVert, rendFaces, coordMin, coordMax

def create_rnd_grass():

    num_pts = 1500
    rendVert = []
    for i in range(num_pts):
        position = np.random.uniform(-1.0 + 0.1, 1.0 - 0.1, (2,))
        height = np.random.uniform(0.1, 0.3)
        length = np.random.uniform(0.05, 0.15)
        direction = np.random.uniform(-1., 1., (2,))
        direction = direction / np.linalg.norm(direction)

        rendVert.append(position[0] - direction[0]*length)
        rendVert.append(0.0)
        rendVert.append(position[1] - direction[1]*length)
        rendVert.append(1.0)
        rendVert.append(0.0)
        rendVert.append(0.0)

        rendVert.append(position[0] - direction[0]*length)
        rendVert.append(height)
        rendVert.append(position[1] - direction[1]*length)
        rendVert.append(1.0)
        rendVert.append(0.0)
        rendVert.append(1.0)

        rendVert.append(position[0] + direction[0]*length)
        rendVert.append(height)
        rendVert.append(position[1] + direction[1]*length)
        rendVert.append(1.0)
        rendVert.append(1.0)
        rendVert.append(1.0)

        rendVert.append(position[0] + direction[0]*length)
        rendVert.append(0.0)
        rendVert.append(position[1] + direction[1]*length)
        rendVert.append(1.0)
        rendVert.append(1.0)
        rendVert.append(0.0)

    rendVert = np.array(rendVert)
    
    coordMin = np.array([-1.0, 0.0, -1.0])
    coordMax = np.array([1.0, 0.0, 1.0])
    
    rendFaces = []
    for i in range(num_pts):
        rendFaces.append(i*4)
        rendFaces.append(i*4+1)
        rendFaces.append(i*4+2)
        rendFaces.append(i*4)
        rendFaces.append(i*4+2)
        rendFaces.append(i*4+3)
    rendFaces = np.array(rendFaces)
    
    return rendVert, rendFaces, coordMin, coordMax



class Exc3(WindowInterface):
    def __init__(self):
        self.ctx = moderngl.create_context()
        vs_path = Path.cwd() / 'exc3_ground.vert'
        fs_path = Path.cwd() / 'exc3_ground.frag'
        self.prog_ground = self.ctx.program(
            vertex_shader=vs_path.read_text(),
            fragment_shader=fs_path.read_text()
        )

        vs_path = Path.cwd() / 'exc3_grass.vert'
        fs_path = Path.cwd() / 'exc3_grass.frag'
        self.prog_grass = self.ctx.program(
            vertex_shader=vs_path.read_text(),
            fragment_shader=fs_path.read_text()
        )
        
        self.mvp = self.prog_ground['worldViewProjMatrix']
        self.diffTexLoc = self.prog_ground['diffTexture']

        self.mvp_grass = self.prog_grass['worldViewProjMatrix']
        if 'time' in self.prog_grass:
            self.time_grass = self.prog_grass['time']
        else:
            self.time_grass = None
        self.diffTexLoc_grass = self.prog_grass['diffTexture']

        rendVert, rendFaces, coordMin, coordMax = create_plane()
        self.vbo = self.ctx.buffer(rendVert.astype('f4').tobytes())
        self.ibo = self.ctx.buffer(rendFaces.astype('i4').tobytes())
        self.vao_ground = self.ctx.vertex_array(self.prog_ground, [(self.vbo, '4f 2f', 'sPos', 'sTexCoords')], self.ibo)

        rendVert, rendFaces, _, _ = create_rnd_grass()
        self.vbo = self.ctx.buffer(rendVert.astype('f4').tobytes())
        self.ibo = self.ctx.buffer(rendFaces.astype('i4').tobytes())
        self.vao_grass = self.ctx.vertex_array(self.prog_grass, [(self.vbo, '4f 2f', 'sPos', 'sTexCoords')], self.ibo)
        
        
        self.aabbSize = math.sqrt(np.sum((coordMax-coordMin) ** 2))
        self.camera = Camera(
                [0.0, 0.0, 0.0], 
                [0.0, 0.0, self.aabbSize*1.5], 
                [0.0, 1.0, 0.0],
                float(self.WINDOW_SIZE[0])/float(self.WINDOW_SIZE[1]),
                45.0, 0.1, self.aabbSize*5.0)
        self.viewMat = self.camera.get_view_natrix()
        self.projMat = self.camera.get_projection_matrix()
        self.worldViewProjMat = self.projMat * self.viewMat
        
        self.lastRotated_ = False
        self.mouse = (0.0, 0.0)
        
        diffImg = Image.open(local('textures', 'ground.jpg')).convert('RGB').transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        diffImg_grass = Image.open(local('textures', 'grass_small.png')).convert('RGBA').transpose(Image.Transpose.FLIP_TOP_BOTTOM)

        self.diffTexture = self.ctx.texture(diffImg.size, 3, diffImg.tobytes())
        self.diffTexture_grass = self.ctx.texture(diffImg_grass.size, 4, diffImg_grass.tobytes())
        
        self.diffTexture.use(0)      
        self.diffTexture_grass.use(1)        
      
        self.diffTexLoc.value = 0
        self.diffTexLoc_grass.value = 1

        self.prevTime = current_milli_time()
        
        
    def render(self):
        self.ctx.viewport = self.wnd.viewport
        if self.wnd.mouse_pressed and self.lastRotated:
            self.camera.rotate_x((self.wnd.mouse[1]-self.mouse[1])/500.0)
            self.camera.rotate_y((self.wnd.mouse[0]-self.mouse[0])/500.0)
            self.viewMat = self.camera.get_view_natrix()
            self.worldViewProjMat = self.projMat * self.viewMat
        if (self.wnd.wheel != 0.0): 
            viewDir = self.camera.vrp_ - self.camera.obs_
            dist = math.sqrt(np.sum(viewDir ** 2))
            viewDir = viewDir/dist
            newPos = self.camera.obs_ + viewDir*self.wnd.wheel*0.01
            newViewDir = self.camera.vrp_ - newPos
            newDist = math.sqrt(np.sum(newViewDir ** 2))
            if newDist < self.aabbSize*1.5 and newDist > 1.5:
                self.camera.obs_ = newPos
                self.viewMat = self.camera.get_view_natrix()
                self.worldViewProjMat = self.projMat * self.viewMat

        self.mouse = self.wnd.mouse
        self.lastRotated = self.wnd.mouse_pressed
        
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.ctx.disable(moderngl.CULL_FACE)
        self.ctx.clear(1.0, 1.0, 1.0)

        self.mvp.write(self.worldViewProjMat.transpose().astype('f4').tobytes())
        self.mvp_grass.write(self.worldViewProjMat.transpose().astype('f4').tobytes())
        if not(self.time_grass is None):
            self.time_grass.value = (((current_milli_time() - self.prevTime)*0.0025))
        
        self.vao_ground.render()
        self.vao_grass.render()


if __name__ == '__main__':
    run_interface(Exc3)
