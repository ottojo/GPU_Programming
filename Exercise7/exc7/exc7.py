import moderngl
from pathlib import Path
import numpy as np
import math

from gpuproglib import WindowInterface, run_interface, Camera, read_model, generate_rendering_buffers


class Exc7(WindowInterface):
    def __init__(self):
    
        self.ctx = moderngl.create_context()
        
        vs_path = Path.cwd() / 'exc7.vert'
        fs_path = Path.cwd() / 'exc7.frag'

        self.prog = self.ctx.program(
            vertex_shader=vs_path.read_text(),
            fragment_shader=fs_path.read_text()
        )
        
        self.mv = self.prog['worldViewMatrix']
        self.p = self.prog['ProjMatrix']

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
        
        vs_ao_path = Path.cwd() / 'exc7_ao.vert'
        fs_ao_path = Path.cwd() / 'exc7_ao.frag'

        self.progAO_ = self.ctx.program(
            vertex_shader=vs_ao_path.read_text(),
            fragment_shader=fs_ao_path.read_text()
        )
        
        self.tex1U = self.progAO_['posTex']
        self.tex2U = self.progAO_['normalTex']
        self.tex3U = self.progAO_['colorTex']
        
        canvas_fs_quad = np.array([0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0]).astype('f4')
        vboAO = self.ctx.buffer(canvas_fs_quad.tobytes())
        self.vaoAO_ = self.ctx.simple_vertex_array(self.progAO_, vboAO, 'inPos')
        
        self.texture1FB_ = self.ctx.texture(self.wnd.size, components=4, dtype='f4')
        self.texture2FB_ = self.ctx.texture(self.wnd.size, components=4, dtype='f4')
        self.texture3FB_ = self.ctx.texture(self.wnd.size, components=4, dtype='f4')
        self.renderBufferFB_ = self.ctx.depth_renderbuffer(self.wnd.size)
        self.fbo_ = self.ctx.framebuffer([self.texture1FB_, self.texture2FB_, self.texture3FB_], self.renderBufferFB_)
        
        
    def render(self):
    
        self.fbo_.clear(0.0, 0.0, 0.0, -1.0)
        self.fbo_.use()
        
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
        self.vao.render()
        
        self.ctx.screen.use()
        self.ctx.screen.clear(0.0, 0.0, 0.0)
        
        self.ctx.viewport = self.wnd.viewport
        
        self.texture1FB_.use(0)
        self.texture2FB_.use(1)
        self.texture3FB_.use(2)
        
        self.tex1U.value=0
        self.tex2U.value=1
        self.tex3U.value=2
        
        self.vaoAO_.render(moderngl.TRIANGLE_STRIP)


if __name__ == '__main__':
    run_interface(Exc7)
