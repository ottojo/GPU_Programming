import sys
import math
import argparse
import os
import numpy as np
import time

import OpenGL
OpenGL.ERROR_CHECKING = False
OpenGL.ERROR_LOGGING = False
from OpenGL import GL

import pygame as pg

from OpenGLUtils import ShaderLoader, MeshRenderer, Camera

current_milli_time = lambda: time.time() * 1000.0

FLOAT_SIZE = 4
INT_SIZE = 4

class GLScene:
    
    def __init__(self, width, height, ptMin, ptMax, vertexs, faces, 
                lightDir = [1.0, 1.0, 0.0], objColor = [0.0, 1.0, 0.0, 1.0]):

        # Configure OpenGL state.
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glCullFace(GL.GL_BACK)
        GL.glFrontFace(GL.GL_CCW)

        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glDepthMask(GL.GL_TRUE)
        GL.glDepthFunc(GL.GL_LEQUAL)

        # Create the camera.
        aabbSize = math.sqrt(np.sum((ptMax-ptMin) ** 2))
        self.camera_ = Camera(
                [0.0, 0.0, 0.0], 
                [0.0, aabbSize*0.5, aabbSize*1.5], 
                [0.0, 1.0, 0.0],
                float(width)/float(height),
                45.0, 0.1, aabbSize*5.0)
        self.viewMat_ = self.camera_.get_view_natrix()
        self.projMat_ = self.camera_.get_projection_matrix()
        self.worldViewProjMat_ = self.projMat_ * self.viewMat_

        # Load the shaders.
        self.shaderLoader_ = ShaderLoader()
        self.shaderMesh_ = self.shaderLoader_.load_shader(
            ["vertexShader.glsl", "pixelShader.glsl"],
            [GL.GL_VERTEX_SHADER, GL.GL_FRAGMENT_SHADER])
        self.worldViewProjMatrixUnif_ = GL.glGetUniformLocation(self.shaderMesh_, "worldViewProjMatrix")
        self.lightDirUnif_ = GL.glGetUniformLocation(self.shaderMesh_, "lightDirection")
        self.objColorUnif_ = GL.glGetUniformLocation(self.shaderMesh_, "inColor")
        self.timeLoc_ = GL.glGetUniformLocation(self.shaderMesh_, "time")
        self.posLoc_ = GL.glGetAttribLocation(self.shaderMesh_, "sPos")
        self.normalLoc_ = GL.glGetAttribLocation(self.shaderMesh_, "sNormal")

        # Load the mesh.
        self.mesh_ = MeshRenderer(vertexs, faces, [4,3], [self.posLoc_, self.normalLoc_])

        # Resize viewport.
        self.width_ = width
        self.height_ = height
        GL.glViewport(0, 0, width, height)

        # Initialize mouse variables.
        self.lastRotated_ = False
        self.mouseX_ = 0.0
        self.mouseY_ = 0.0
        
        # Save light direction.
        self.lightDir_ = lightDir
        
        # Save the object color.
        self.objColor_ = objColor
        
        
    def update(self, rotate, mouseX, mouseY):
        if rotate and self.lastRotated_:
            self.camera_.rotate_x((mouseY-self.mouseY_)/500.0)
            self.camera_.rotate_y((mouseX-self.mouseX_)/500.0)
            self.viewMat_ = self.camera_.get_view_natrix()
            self.worldViewProjMat_ = self.projMat_ * self.viewMat_
        self.mouseX_ = mouseX
        self.mouseY_ = mouseY
        self.lastRotated_ = rotate


    def display(self, time):
        GL.glClearColor(1,1,1,1)
         
        #Render Mesh
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)     
        GL.glUseProgram(self.shaderMesh_)
        GL.glBindFragDataLocation(self.shaderMesh_, 0, "outColor")
        GL.glUniformMatrix4fv(self.worldViewProjMatrixUnif_, 1, GL.GL_TRUE, np.ascontiguousarray(self.worldViewProjMat_, dtype=np.float32))
        GL.glUniform3f(self.lightDirUnif_, self.lightDir_[0], self.lightDir_[1], self.lightDir_[2])            
        GL.glUniform4f(self.objColorUnif_, self.objColor_[0], self.objColor_[1], self.objColor_[2], self.objColor_[3])
        GL.glUniform1f(self.timeLoc_, time)
        self.mesh_.render_mesh()
        GL.glUseProgram(0)
        

##################################################################### MAIN


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Script to visualize a deformation plane')
    args = parser.parse_args()    

    # Create the model
    rendVert = []
    for i in range(50):
        for j in range(50):
            rendVert.append(2.0*(float(i)/50.0)-1.0)
            rendVert.append(0.0)
            rendVert.append(2.0*(float(j)/50.0)-1.0)
            rendVert.append(1.0)
            rendVert.append(0.0)
            rendVert.append(1.0)
            rendVert.append(0.0)
    rendVert = np.array(rendVert)
    
    coordMin = np.array([-1.0, 0.0, -1.0])
    coordMax = np.array([1.0, 0.0, 1.0])
    
    rendFaces = []
    for i in range(49):
        for j in range(49):
            rendFaces.append(i*50 + j)
            rendFaces.append((i+1)*50 + 1 + j)
            rendFaces.append((i+1)*50 + j)
            rendFaces.append(i*50 + j)
            rendFaces.append(i*50 + 1 + j)
            rendFaces.append((i+1)*50 + 1 + j)      
    rendFaces = np.array(rendFaces)
    
    print("Vertexs: "+str(len(rendVert)/7))
    print("faces: "+str(len(rendFaces)/3))
    
    #Render
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    SCREEN = pg.display.set_mode((512, 512),  pg.OPENGL | pg.DOUBLEBUF)
    MyClock = pg.time.Clock()

    MyGL = GLScene(512, 512, coordMin, coordMax, rendVert, rendFaces)

    mouseDown = False
    prevTime = current_milli_time()
    while 1:
        for event in pg.event.get():
            if event.type==pg.QUIT or (event.type==pg.KEYDOWN and event.key==pg.K_ESCAPE):
                pg.quit();sys.exit()
            elif (event.type==pg.KEYDOWN and event.key==pg.K_s):
                pg.image.save(SCREEN,"screenshot.jpg")
            elif event.type == pg.KEYDOWN:
                pass
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseDown = True
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    mouseDown = False
        
        mouseX, mouseY = pg.mouse.get_pos()
        MyGL.update(mouseDown, mouseX, mouseY)

        currTime = ((current_milli_time() - prevTime)*0.01)

        MyGL.display(currTime)

        pg.display.flip()