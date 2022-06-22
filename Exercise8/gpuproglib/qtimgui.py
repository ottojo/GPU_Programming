from imgui.integrations.opengl import ProgrammablePipelineRenderer
import imgui
import moderngl
from PyQt5 import QtOpenGL, QtWidgets, QtCore, QtGui
from config import OPENGL_VERSION, WINDOW_SIZE
import time
import sys
import numpy as np

class WindowInfo:
    def __init__(self):
        self.size = (0, 0)
        self.mouse_pressed = False
        self.mouse = (0, 0)
        self.wheel = 0
        self.time: float = 0.0
        self.ratio = 1.0
        self.viewport = (0, 0, 0, 0)
        self.keys = np.full(256, False)
        self.old_keys = np.copy(self.keys)

    def key_down(self, key):
        return self.keys[key]

    def key_pressed(self, key):
        return self.keys[key] and not self.old_keys[key]

    def key_released(self, key):
        return not self.keys[key] and self.old_keys[key]


class Window(QtOpenGL.QGLWidget):
    def __init__(self, size, title):
        fmt = QtOpenGL.QGLFormat()
        fmt.setVersion(*OPENGL_VERSION)
        fmt.setProfile(QtOpenGL.QGLFormat.CoreProfile)
        fmt.setSwapInterval(1)
        fmt.setSampleBuffers(True)
        fmt.setDepthBufferSize(24)
        super().__init__(fmt, None)

        self.setFixedSize(size[0], size[1])
        self.move(QtWidgets.QDesktopWidget().rect().center() - self.rect().center())
        self.setWindowTitle(title)
        self.title = title
        self.start_time = time.monotonic()
        self.size = size
        self.viewport = (0, 0) + (size[0] * self.devicePixelRatio(), size[1] * self.devicePixelRatio())
        self.aspectRatio = size[0] / size[1]
        self.screen: moderngl.Framebuffer = None
        self.wnd = WindowInfo()

    def initializeGL(self):
        super().initializeGL()
        self.screen = self.ctx.detect_framebuffer()

    def keyReleaseEvent(self, event: QtGui.QKeyEvent):
        self.wnd.keys[event.nativeVirtualKey() & 0xFF] = False

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        self.wnd.mouse = (event.x(), event.y())

    def mousePressEvent(self, evt: QtGui.QMouseEvent):
        self.wnd.mouse = (evt.x(), evt.y())
        self.wnd.mouse_pressed = True
        self.update()

    def mouseReleaseEvent(self, evt: QtGui.QMouseEvent):
        btn: QtCore.Qt = evt.button()
        self.wnd.mouse_pressed = False
        self.update()

    def wheelEvent(self, event: QtGui.QWheelEvent):
        # http://doc.qt.io/qt-5/qwheelevent.html#angleDelta
        self.wnd.wheel += event.angleDelta().y()
        event.accept()
        self.update()

    def resizeGL(self, width, height):
        print(f'resize {width}, {height}')
        side = min(width, height)
        if side < 0:
            return
        self.viewport = ((width - side) // 2, (height - side) // 2, side, side)
        self.ctx.viewport = self.viewport

    def paintGL(self):
        if self.iface is None:
            self.iface = self.factory()
        self.wnd.time = time.monotonic() - self.start_time
        self.setWindowTitle(f'{self.title} - time {self.wnd.time:4.2f}')
        self.iface.render()
        self.wnd.old_keys = np.copy(self.wnd.keys)
        self.wnd.wheel = 0

        self.update()


class QModernGLWidget(QtOpenGL.QGLWidget):
    def __init__(self):
        fmt = QtOpenGL.QGLFormat()
        fmt.setVersion(4, 3)
        fmt.setProfile(QtOpenGL.QGLFormat.CoreProfile)
        fmt.setSampleBuffers(True)
        self.timer = QtCore.QElapsedTimer()
        self.viewport = (0, 0, 0, 0)
        self.ctx: moderngl.Context = None
        self.screen: moderngl.Framebuffer = None
        super(QModernGLWidget, self).__init__(fmt, None)

    def initializeGL(self):
        print(f'initGL')
        self.ctx = moderngl.create_context()
        self.screen: moderngl.Framebuffer = self.ctx.detect_framebuffer()
        self.init()

    def paintGL(self):
        self.render()
        self.paintGL = self.render

    def init(self):
        pass

    def render(self):
        pass

    def resizeGL(self, width, height):
        print(f'resize {width}, {height}')
        side = min(width, height)
        if side < 0:
            return
        self.viewport = ((width - side) // 2, (height - side) // 2, side, side)
        self.ctx.viewport = self.viewport


class QtRenderer(ProgrammablePipelineRenderer):
    def __init__(self, window: Window, attach_callbacks=True):
        super().__init__()

        self.window = window

        if attach_callbacks:
            window.keyPressEvent = self.keyPressEvent
            window.keyReleaseEvent = self.keyReleaseEvent
            window.mouseMoveEvent = self.mouseMoveEvent
            window.mousePressEvent = self.mousePressEvent
            window.mouseReleaseEvent = self.mouseReleaseEvent
            window.wheelEvent = self.wheelEvent
            window.resizeGL = self.resizeGL
            window.set_scroll_callback(self.scroll_callback)

        self.io.display_size = window.size

        self._map_keys()
        self._gui_time = None

    def _map_keys(self):
        key_map = self.io.key_map

        key_map[imgui.KEY_TAB] = QtCore.Qt.Key_Tab
        key_map[imgui.KEY_LEFT_ARROW] = QtCore.Qt.Key_Left
        key_map[imgui.KEY_RIGHT_ARROW] = QtCore.Qt.Key_Right
        key_map[imgui.KEY_UP_ARROW] = QtCore.Qt.Key_Up
        key_map[imgui.KEY_DOWN_ARROW] = QtCore.Qt.Key_Down
        key_map[imgui.KEY_PAGE_UP] = QtCore.Qt.Key_PageUp
        key_map[imgui.KEY_PAGE_DOWN] = QtCore.Qt.Key_PageDown
        key_map[imgui.KEY_HOME] = QtCore.Qt.Key_Home
        key_map[imgui.KEY_END] = QtCore.Qt.Key_End
        key_map[imgui.KEY_DELETE] = QtCore.Qt.Key_Delete
        key_map[imgui.KEY_BACKSPACE] = QtCore.Qt.Key_Backspace
        key_map[imgui.KEY_ENTER] = QtCore.Qt.Key_Enter
        key_map[imgui.KEY_ESCAPE] = QtCore.Qt.Key_Escape
        key_map[imgui.KEY_A] = QtCore.Qt.Key_A
        key_map[imgui.KEY_C] = QtCore.Qt.Key_C
        key_map[imgui.KEY_V] = QtCore.Qt.Key_V
        key_map[imgui.KEY_X] = QtCore.Qt.Key_X
        key_map[imgui.KEY_Y] = QtCore.Qt.Key_Y
        key_map[imgui.KEY_Z] = QtCore.Qt.Key_Z


    def set_key_modifiers(self):
        io = self.io
        io.key_ctrl = io.keys_down[QtCore.Qt.Key_Control]
        io.key_alt = io.keys_down[QtCore.Qt.Key_Alt]
        io.key_shift = io.keys_down[QtCore.Qt.Key_Shift]
        io.key_super = (
            io.keys_down[QtCore.Qt.Key_Super_L] or
            io.keys_down[QtCore.Qt.Key_Super_R]
        )

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        key = event.key()
        io = self.io
        io.keys_down[key] = True
        self.set_key_modifiers()
        for character in event.text():
            self.consume_char(character)

        if event.key() == QtCore.Qt.Key_Escape:
            # Quit when ESC is pressed
            QtCore.QCoreApplication.instance().quit()
        elif event.key() == QtCore.Qt.Key_R:
            # reload when R-key is pressed.
            self.iface.reload()
            sys.stdout.flush()

        # self.wnd.keys[event.nativeVirtualKey() & 0xFF] = True

    def keyReleaseEvent(self, event: QtGui.QKeyEvent):
        key = event.key()
        io = self.io
        io.keys_down[key] = False
        self.set_key_modifiers()

        # self.wnd.keys[event.nativeVirtualKey() & 0xFF] = False

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        self.mouse = (event.x(), event.y())
        # if glfw.get_window_attrib(self.window, glfw.FOCUSED):
        self.io.mouse_pos = self.mouse
        # else imgui.get_io().mouse_pos = (-1,-1)

    def mousePressEvent(self, evt: QtGui.QMouseEvent):
        self.window.mouse = (evt.x(), evt.y())
        self.window.mouse_pressed = True
        io = imgui.get_io()
        btn = evt.button()
        if btn == QtCore.Qt.LeftButton:
            io.mouse_down[0] = True
        if btn == QtCore.Qt.RightButton:
            io.mouse_down[1] = True
        if btn == QtCore.Qt.MidButton:
            io.mouse_down[2] = True
        self.window.update()

    def mouseReleaseEvent(self, evt: QtGui.QMouseEvent):
        btn: QtCore.Qt = evt.button()
        self.window.mouse_pressed = False
        self.window.update()

    def wheelEvent(self, event: QtGui.QWheelEvent):
        # http://doc.qt.io/qt-5/qwheelevent.html#angleDelta
        self.window.wheel += event.angleDelta().y()

        self.io.mouse_wheel = event.y()
        event.accept()
        self.window.update()

    def consume_char(self, char):
        if 0 < char < 0x10000:
            self.io.add_input_character(char)

    def resizeGL(self, width, height):
        self.io.display_size = width, height
        print(f'resize {width}, {height}')
        side = min(width, height)
        if side < 0:
            return
        self.window.viewport = ((width - side) // 2, (height - side) // 2, side, side)
        self.window.ctx.viewport = self.window.viewport

    # def resize_callback(self, window, width, height):
    #     self.io.display_size = width, height
    #
    # def mouse_callback(self, *args, **kwargs):
    #     pass

    # def scroll_callback(self, window, x_offset, y_offset):
    #     self.io.mouse_wheel = y_offset

    def process_inputs(self):
        # todo: consider moving to init
        io = imgui.get_io()

        w, h = self.window.size
        dw, dh = self.window.screen.size

        io.display_size = w, h
        if w != 0 and h != 0:
            io.display_fb_scale = dw/w, dh/h # else?

        io.delta_time = 1.0/60

        # if glfw.get_window_attrib(self.window, glfw.FOCUSED):
        #     io.mouse_pos = glfw.get_cursor_pos(self.window)
        # else:
        #     io.mouse_pos = -1, -1

        # io.mouse_down[0] = glfw.get_mouse_button(self.window, 0)
        # io.mouse_down[1] = glfw.get_mouse_button(self.window, 1)
        # io.mouse_down[2] = glfw.get_mouse_button(self.window, 2)

        current_time = time.monotonic()

        if self._gui_time:
            self.io.delta_time = current_time - self._gui_time
        else:
            self.io.delta_time = 1. / 60.

        self._gui_time = current_time
