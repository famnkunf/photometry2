from PyQt5 import QtWidgets, QtCore, QtGui
from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np

from ..ui import aperturewindow_ui

class ApertureWindow(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__(None, QtCore.Qt.WindowStaysOnTopHint)
        self.ui = aperturewindow_ui.Ui_ApertureWindow()
        self.ui.setupUi(self)
        self.main_window = main_window
        self.draft = None
        self.update_value()
        self.ui.major_axis.valueChanged.connect(self.update_value)
        self.ui.minor_axis.valueChanged.connect(self.update_value)
        self.ui.angle.valueChanged.connect(self.update_value)
        self.ui.gap.valueChanged.connect(self.update_value)
        self.ui.background.valueChanged.connect(self.update_value)
        
    def update_value(self):
        self.a = self.ui.major_axis.value()
        self.b = self.ui.minor_axis.value()
        self.angle = self.ui.angle.value()
        self.gap = self.ui.gap.value()
        self.background = self.ui.background.value()
        if self.draft is not None:
            self.draft[0].set_width(self.a)
            self.draft[0].set_height(self.b)
            self.draft[0].set_angle(self.angle)
            self.draft[1].set_width(self.a + self.gap)
            self.draft[1].set_height(self.b + self.gap)
            self.draft[1].set_angle(self.angle)
            self.draft[2].set_width(self.a + self.gap + self.background)
            self.draft[2].set_height(self.b + self.gap + self.background)
            self.draft[2].set_angle(self.angle)
        
    # def _create_ellipse_cursor(self, a, b, angle, background, gap, display_window):
    #     scale_x = display_window.image.shape[1]/np.abs(display_window.ax.get_xlim()[1] - display_window.ax.get_xlim()[0])
    #     scale_y = display_window.image.shape[0]/np.abs(display_window.ax.get_ylim()[1] - display_window.ax.get_ylim()[0])
    #     width = int((a + 2*gap + 2*background))
    #     height = int((b + 2*gap + 2*background))
    #     pixmap = QtGui.QPixmap(width, height)
    #     pixmap.fill(QtCore.Qt.transparent)
    #     pixmap.setDevicePixelRatio(display_window.canvas.devicePixelRatio())
    #     painter = QtGui.QPainter(pixmap)
    #     painter.setRenderHint(QtGui.QPainter.Antialiasing)
    #     painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
    #     print(scale_x, scale_y)
    #     painter.scale(scale_x, scale_y)
        
    #     pen = QtGui.QPen(QtCore.Qt.red, 1)
    #     pen.setStyle(QtCore.Qt.SolidLine)
    #     painter.setPen(pen)
    #     painter.drawEllipse(int(width//2-a//2), int(height//2-b//2), int(a), int(b))

    #     pen.setStyle(QtCore.Qt.DashLine)
    #     pen.setBrush(QtCore.Qt.blue)
    #     painter.setPen(pen)
    #     painter.drawEllipse(int(width//2-a//2-gap), int(height//2-b//2-gap), int(a + 2*gap), int(b + 2*gap))

    #     pen.setStyle(QtCore.Qt.DashLine)
    #     pen.setBrush(QtCore.Qt.yellow)
    #     painter.setPen(pen)
    #     painter.drawEllipse(int(width//2-a//2-gap-background), int(height//2-b//2-gap-background), int(a + 2*gap + 2*background), int(b + 2*gap + 2*background))
    #     painter.rotate(angle)
        
    #     # painter.translate(int(display_window.canvas.width() / 2), int(display_window.canvas.height() / 2))
    #     painter.end()

    #     return QtGui.QCursor(pixmap)

        
    def draw_aperture(self, display_window, event):
        x, y = event.xdata, event.ydata
        if x is not None and y is not None:
            if self.draft is None:
                self.draft = (
                    Ellipse((x, y), self.a, self.b, angle=self.angle, color='red', fill=False, lw=1),
                    Ellipse((x, y), self.a + self.gap, self.b + self.gap, angle=self.angle, color='blue', fill=False, lw=1, ls='--'),
                    Ellipse((x, y), self.a + self.gap + self.background, self.b + self.gap + self.background, angle=self.angle, color='yellow', fill=False, lw=1, ls='--'),
                )
                for patch in self.draft:
                    display_window.ax.add_patch(patch)
            else:
                for patch in self.draft:
                    patch.set_center((x, y))
            display_window.canvas.draw_idle()
            display_window.canvas.flush_events()
        # cursor = self._create_ellipse_cursor(self.a, self.b, self.angle, self.background, self.gap, display_window)
        # display_window.canvas.setCursor(cursor)

    def close(self):
        self.main_window.aperture_window = None
        if self.draft:
            for patch in self.draft:
                patch.remove()
        super().close()