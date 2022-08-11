from typing import List, Callable, Tuple, Union

import moderngl
import numpy as np
from PIL import Image
import sys
from pathlib import Path
from datetime import datetime
from PyQt5.QtCore import Qt
from config import OPENGL_VERSION

from gpuproglib import WindowInterface, run_interface


number_keys = (
Qt.Key_1,
Qt.Key_2,
Qt.Key_3,
Qt.Key_4,
Qt.Key_5,
Qt.Key_6,
Qt.Key_7,
Qt.Key_8,
Qt.Key_9,
)

class ShaderToy(WindowInterface):
    def reload(self):
        print('reload')
        self.reload_prog()
        self.reload_uniforms()
        self.reload_vertex_array()

    def reload_prog(self):
        try:
            version = ''.join([str(x) for x in OPENGL_VERSION])
            version = f'#version {version}0\n'
            header_path = Path(__file__).parent / 'includes' / 'image' / 'header.glsl'
            footer_path = Path(__file__).parent / 'includes' / 'image' / 'footer.glsl'
            header = header_path.read_text()
            footer = footer_path.read_text()
            shadertoy = self.fs_path.read_text()
            newprog = self.ctx.program(
                vertex_shader=self.vs_path.read_text(),
                fragment_shader=version+header+shadertoy+footer
            )
            if self.prog:
                self.prog.release()
            self.prog = newprog
            print(f'[R]: reload')
            for idx, sub in enumerate(self.subroutines()):
                print(f'[{idx+1}]: {sub.name}')


        except moderngl.Error as e:
            print(e)

    def reload_vertex_array(self):
        vao_inputs = ('in_vert',)

        if not self.prog:
            return

        if self.vao:
            self.vao.release()

        if not all([name in self.prog for name in vao_inputs]):
            print(f'missing attribute names in shader, cannot init vertex array object')
            self.vao = None
            return

        self.vao = self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'in_vert')

    def open_and_create_texture(self, name: str, convert: str = 'RGB', transpose: int = Image.FLIP_TOP_BOTTOM):
        path = Path(__file__).parent / 'textures' / name
        image = Image.open(path).convert(convert).transpose(transpose)
        return self.ctx.texture(image.size, 3, image.tobytes())

    def __init__(self):
        self.light_dir = np.array([1.0, 1.0, 0.0])

        self.ctx = moderngl.create_context()
        self.fs_path = Path.cwd() / 'fsq.frag'
        if len(sys.argv) == 1:
            print('must provide a shadertoy as argument')
            raise SystemExit()

        if len(sys.argv) > 1:
            self.fs_path = Path(sys.argv[1]).absolute()
            print(f'using fragment shader: {self.fs_path}')

        self.vs_path = Path(__file__).parent / 'fsq.vert'

        self.prog: moderngl.Program = None
        self.reload_prog()

        self.active_uniforms: List[moderngl.Uniform] = []

        vertices = np.array([-1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0])

        self.vbo = self.ctx.buffer(vertices.astype('f4').tobytes())
        self.vao: moderngl.VertexArray = None
        self.reload_vertex_array()

        self.lastRotated = False
        self.mouse = (0.0, 0.0)

        self.reload_uniforms()

    def subroutines(self) -> List[moderngl.Subroutine]:
        if self.prog is None:
            return []
        for name in self.prog:
            if type(self.prog[name]) is moderngl.Subroutine:
                yield self.prog[name]

    def uniforms(self) -> List[moderngl.Uniform]:
        if self.prog is None:
            return []
        for name in self.prog:
            if type(self.prog[name]) is moderngl.Uniform:
                yield self.prog[name]

    def render(self):
        self.ctx.viewport = self.wnd.viewport
        if self.wnd.mouse_pressed and self.lastRotated:
            dxy = np.array(self.mouse) - np.array(self.wnd.mouse)
            dxy = dxy / np.array(self.WINDOW_SIZE)
        self.mouse = self.wnd.mouse
        self.lastRotated = self.wnd.mouse_pressed

        for key, sub in zip(number_keys,self.subroutines()):
            if self.wnd.key_pressed(key):

                print(f'selected subroutine: {sub.name}')
                self.vao.subroutines = [self.prog[sub.name].index]

        self.ctx.clear(1.0, 1.0, 1.0)
        for uniform in self.active_uniforms:
            uniform.extra()
        if self.vao:
            self.vao.render(moderngl.TRIANGLE_STRIP)

    def iTime(self):
        return np.array([self.wnd.time])

    def iResolution(self):
        x, y = self.wnd.size
        return x, y, 0

    def iMouse(self)->Tuple:
        x, y = self.wnd.mouse
        y = self.wnd.size[1] - y
        if self.wnd.mouse_pressed:
            return x, y, x, y
        return x, y, 0., 0.

    def iDate(self):
        d = datetime.now()
        secs = d.hour*3600 + d.minute * 60 + d.second
        secs += d.microsecond / (1000*1000)
        return d.year, d.month, d.day, secs

    def reload_uniforms(self):
        if not self.prog:
            return
        self.active_uniforms.clear()

        for uniform in self.uniforms():
            name = uniform.name
            if name not in self.supported_uniforms:
                print(f'WARNING! Uniform: "{name}" is not supported by this program')
                continue

            if 'iTime' == name:
                uniform.extra = set_np_array(uniform, self.iTime)
            elif 'iResolution' == name:
                uniform.extra = set_tuple(uniform, self.iResolution)
            elif 'iMouse' == name:
                uniform.extra = set_tuple(uniform, self.iMouse)
            elif 'iDate' == name:
                uniform.extra = set_tuple(uniform, self.iDate)
            self.active_uniforms.append(uniform)

    supported_uniforms = (
        'iTime',
        'iResolution',
        'iMouse',
        'iDate',
    )


def set_single(uniform: moderngl.Uniform, data: Union[int, float]):
    def inner():
        uniform.value = data

    return inner


def set_tuple(uniform: moderngl.Uniform, getter: Callable[[], Tuple]):
    def inner():
        uniform.value = getter()

    return inner


def set_np_array(uniform, getter):
    def inner():
        uniform.write(getter().astype('f4').tobytes())

    return inner


if __name__ == '__main__':
    run_interface(ShaderToy)
