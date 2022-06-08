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

    # Create the model
    rendVert = []
    rendFaces = []
  
    # Top Face
    # Vert1
    rendVert.append(-1.0)
    rendVert.append(0.0)
    rendVert.append(-1.0)
    rendVert.append(1.0)
    
    rendVert.append(0.0)
    rendVert.append(1.0)
    rendVert.append(0.0)
    
    rendVert.append(1.0)
    rendVert.append(0.0)
    rendVert.append(0.0)
    
    rendVert.append(0.0)
    rendVert.append(0.0)
    rendVert.append(1.0)
    
    rendVert.append(0.0)
    rendVert.append(0.0)
    
    # Vert2
    rendVert.append(-1.0)
    rendVert.append(0.0)
    rendVert.append(1.0)
    rendVert.append(1.0)
    
    rendVert.append(0.0)
    rendVert.append(1.0)
    rendVert.append(0.0)
    
    rendVert.append(1.0)
    rendVert.append(0.0)
    rendVert.append(0.0)
    
    rendVert.append(0.0)
    rendVert.append(0.0)
    rendVert.append(1.0)
    
    rendVert.append(0.0)
    rendVert.append(1.0)
    
    # Vert3
    rendVert.append(1.0)
    rendVert.append(0.0)
    rendVert.append(1.0)
    rendVert.append(1.0)
    
    rendVert.append(0.0)
    rendVert.append(1.0)
    rendVert.append(0.0)
    
    rendVert.append(1.0)
    rendVert.append(0.0)
    rendVert.append(0.0)
    
    rendVert.append(0.0)
    rendVert.append(0.0)
    rendVert.append(1.0)
    
    rendVert.append(1.0)
    rendVert.append(1.0)
    
    # Vert4
    rendVert.append(1.0)
    rendVert.append(0.0)
    rendVert.append(-1.0)
    rendVert.append(1.0)
    
    rendVert.append(0.0)
    rendVert.append(1.0)
    rendVert.append(0.0)
    
    rendVert.append(1.0)
    rendVert.append(0.0)
    rendVert.append(0.0)
    
    rendVert.append(0.0)
    rendVert.append(0.0)
    rendVert.append(1.0)
    
    rendVert.append(1.0)
    rendVert.append(0.0)
    
    # Face 1 indexs
    rendFaces.append(0)
    rendFaces.append(1)
    rendFaces.append(2)
    rendFaces.append(0)
    rendFaces.append(2)
    rendFaces.append(3) 

     
    rendVert = np.array(rendVert)
    rendFaces = np.array(rendFaces)
    
    coordMin = np.array([-1.0, 0.0, -1.0])
    coordMax = np.array([1.0, 0.0, 1.0])
    
    return rendVert, rendFaces, coordMin, coordMax


class Exc6(WindowInterface):
    def __init__(self):
        self.ctx = moderngl.create_context()
        vs_path = Path.cwd() / 'exc6.vert'
        fs_path = Path.cwd() / 'exc6.frag'

        self.prog = self.ctx.program(
            vertex_shader=vs_path.read_text(),
            fragment_shader=fs_path.read_text()
        )
        
        self.mvp = self.prog['worldViewProjMatrix']
        self.lightDir = self.prog['lightDirection']
        self.camPos = self.prog['camPos']
        
        self.diffTexLoc = self.prog['diffTexture']
        self.specTexLoc = self.prog['specTexture']
        self.normTexLoc = self.prog['normalTexture']
        self.dispTexLoc = self.prog['dispTexture']

        rendVert, rendFaces, coordMin, coordMax = create_plane()

        self.vbo = self.ctx.buffer(rendVert.astype('f4').tobytes())
        self.ibo = self.ctx.buffer(rendFaces.astype('i4').tobytes())
        self.vao = self.ctx.vertex_array(self.prog, [(self.vbo, '4f 3f 3f 3f 2f', 'sPos', 'sNormal', 'sTangent', 'sBinormal', 'sTexCoords')], self.ibo)
        
        aabbSize = math.sqrt(np.sum((coordMax-coordMin) ** 2))
        self.camera = Camera(
                [0.0, 0.0, 0.0], 
                [0.0, 0.0, aabbSize*1.5], 
                [0.0, 1.0, 0.0],
                float(self.WINDOW_SIZE[0])/float(self.WINDOW_SIZE[1]),
                45.0, 0.1, aabbSize*5.0)
        self.viewMat = self.camera.get_view_natrix()
        self.projMat = self.camera.get_projection_matrix()
        self.worldViewProjMat = self.projMat * self.viewMat
        
        self.lastRotated_ = False
        self.mouse = (0.0, 0.0)
        
        diffImg = Image.open(local('textures', 'bricks_diff.jpg')).convert('RGB').transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        specImg = Image.open(local('textures', 'bricks_spec.jpg')).convert('RGB').transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        normImg = Image.open(local('textures', 'bricks_normal.jpg')).convert('RGB').transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        depthImg = Image.open(local('textures', 'bricks_depth.jpg')).convert('RGB').transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        
        self.diffTexture = self.ctx.texture(diffImg.size, 3, diffImg.tobytes())
        self.specTexture = self.ctx.texture(specImg.size, 3, specImg.tobytes())
        self.normalTexture = self.ctx.texture(normImg.size, 3, normImg.tobytes())
        self.depthTexture = self.ctx.texture(depthImg.size, 3, depthImg.tobytes())
        
        self.diffTexture.use(0)
        self.specTexture.use(1)
        self.normalTexture.use(2)
        self.depthTexture.use(3)
        
        self.diffTexLoc.value = 0
        self.specTexLoc.value = 1
        self.normTexLoc.value = 2
        self.dispTexLoc.value = 3
        
        self.lightDir_ = np.array([1.0, 1.0, 0.0])
        
        
    def render(self):
        self.ctx.viewport = self.wnd.viewport
        if self.wnd.mouse_pressed and self.lastRotated:
            self.camera.rotate_x((self.wnd.mouse[1]-self.mouse[1])/500.0)
            self.camera.rotate_y((self.wnd.mouse[0]-self.mouse[0])/500.0)
            self.viewMat = self.camera.get_view_natrix()
            self.worldViewProjMat = self.projMat * self.viewMat
        self.mouse = self.wnd.mouse
        self.lastRotated = self.wnd.mouse_pressed

        if self.wnd.keys[106] == True:
            self.lightDir_[0] += 0.01
        if self.wnd.keys[117] == True:
            self.lightDir_[0] -= 0.01

        self.ctx.enable(moderngl.DEPTH_TEST)
        self.ctx.clear(1.0, 1.0, 1.0)
        self.mvp.write(self.worldViewProjMat.transpose().astype('f4').tobytes())
        
        self.lightDir.write(self.lightDir_.astype('f4').tobytes())
        self.camPos.write(self.camera.obs_.astype('f4').tobytes())
        
        
        self.vao.render()


if __name__ == '__main__':
    run_interface(Exc6)
