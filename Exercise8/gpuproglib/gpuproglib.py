import time
import sys
from abc import abstractmethod, ABC
import numpy as np
from PyQt5 import QtOpenGL, QtWidgets, QtCore, QtGui

from config import OPENGL_VERSION, WINDOW_SIZE

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
        self.factory: type(WindowInterface) = lambda: None
        self.iface: WindowInterface = None

        self.wnd = WindowInfo()
        self.wnd.viewport = (0, 0) + (size[0] * self.devicePixelRatio(), size[1] * self.devicePixelRatio())
        self.wnd.ratio = size[0] / size[1]
        self.wnd.size = size

    def keyPressEvent(self, event):
        # Quit when ESC is pressed
        if event.key() == QtCore.Qt.Key_Escape:
            QtCore.QCoreApplication.instance().quit()
        elif event.key() == QtCore.Qt.Key_R:
            self.iface.reload()
            sys.stdout.flush()

        self.wnd.keys[event.nativeVirtualKey() & 0xFF] = True

    def keyReleaseEvent(self, event):
        self.wnd.keys[event.nativeVirtualKey() & 0xFF] = False

    def mouseMoveEvent(self, event):
        self.wnd.mouse = (event.x(), event.y())

    def mousePressEvent(self, evt):
        self.wnd.mouse = (evt.x(), evt.y())
        self.wnd.mouse_pressed = True
        self.update()

    def mouseReleaseEvent(self, evt):
        self.wnd.mouse_pressed = False
        self.update()

    def wheelEvent(self, event):
        self.wnd.wheel += event.angleDelta().y()

    def paintGL(self):
        if self.iface is None:
            self.iface = self.factory()
        self.wnd.time = time.monotonic() - self.start_time
        self.setWindowTitle(f'{self.title} - time {self.wnd.time:4.2f}')
        self.iface.render()
        self.wnd.old_keys = np.copy(self.wnd.keys)
        self.wnd.wheel = 0

        self.update()


class WindowInterface(ABC):
    WINDOW_SIZE = WINDOW_SIZE
    wnd: WindowInfo = None

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def reload(self):
        pass


def run_interface(interface: type(WindowInterface)):
    app = QtWidgets.QApplication([])
    window = Window(interface.WINDOW_SIZE, getattr(interface, 'WINDOW_TITLE', interface.__name__))
    interface.wnd = window.wnd
    window.factory = interface
    window.show()
    app.exec_()
    del app


