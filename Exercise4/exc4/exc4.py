import moderngl
from pathlib import Path
import numpy as np
import math

from gpuproglib import WindowInterface, run_interface, Camera, read_model, generate_rendering_buffers


class Exc4(WindowInterface):
    def __init__(self):
        self.ctx = moderngl.create_context()
        vs_path = Path.cwd() / 'exc4.vert'
        fs_path = Path.cwd() / 'exc4.frag'

        self.prog = self.ctx.program(
            vertex_shader=vs_path.read_text(),
            fragment_shader=fs_path.read_text()
        )
        
        self.mv = self.prog['worldViewMatrix']
        self.p = self.prog['ProjMatrix']
        self.lightPos = self.prog['lightPosition']
        self.objColor = self.prog['inObjColor']
        self.lightColor = self.prog['inLightColor']
        self.camPos = self.prog['camPos']

        vertexs, normals, faces, coordMin, coordMax = read_model("Bunny.obj")
        rendVert, rendFaces = generate_rendering_buffers(vertexs, normals, faces)

        self.vbo = self.ctx.buffer(rendVert.astype('f4').tobytes())
        self.ibo = self.ctx.buffer(rendFaces.astype('i4').tobytes())
        self.vao = self.ctx.vertex_array(self.prog, [(self.vbo, '4f 3f', 'sPos', 'sNormal')], self.ibo)
        
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
        
        
    def render(self):
        self.ctx.viewport = self.wnd.viewport
        if self.wnd.mouse_pressed and self.lastRotated:
            self.camera.rotate_x((self.wnd.mouse[1]-self.mouse[1])/500.0)
            self.camera.rotate_y((self.wnd.mouse[0]-self.mouse[0])/500.0)
            self.viewMat = self.camera.get_view_natrix()
            self.worldViewProjMat = self.projMat * self.viewMat
        self.mouse = self.wnd.mouse
        self.lastRotated = self.wnd.mouse_pressed
        
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.ctx.clear(1.0, 1.0, 1.0)
        self.mv.write(self.viewMat.transpose().astype('f4').tobytes())
        self.p.write(self.projMat.transpose().astype('f4').tobytes())
        self.lightPos.write(np.array([2.0, 4.0, 4.0]).astype('f4').tobytes())
        self.objColor.write(np.array([1.0, 0.0, 0.0, 1.0]).astype('f4').tobytes())
        self.lightColor.write(np.array([1.0, 1.0, 1.0, 1.0]).astype('f4').tobytes())
        self.camPos.write(self.camera.obs_.astype('f4').tobytes())
        self.vao.render()


if __name__ == '__main__':
    run_interface(Exc4)
