from PyQt5 import QtWidgets, QtCore, QtGui
import numpy as np
from vispy import scene

from ..ui import aperturewindow_ui

class ApertureWindow(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__(None, QtCore.Qt.WindowStaysOnTopHint)
        self.ui = aperturewindow_ui.Ui_ApertureWindow()
        self.ui.setupUi(self)
        self.main_window = main_window
        self.ui.major_axis.valueChanged.connect(self.update_value)
        self.ui.minor_axis.valueChanged.connect(self.update_value)
        self.ui.angle.valueChanged.connect(self.update_value)
        self.ui.gap.valueChanged.connect(self.update_value)
        self.ui.background.valueChanged.connect(self.update_value)
        transform = scene.STTransform(translate=(0, 0, -1), scale=(1, 1, 1))
        self.inner_aperture = scene.Ellipse(center=(0, 0), radius=(0, 0), border_color='red', color=(0, 0, 0, 0))
        self.gap_aperture = scene.Ellipse(center=(0, 0), radius=(0, 0), border_color='yellow', color=(0, 0, 0, 0))
        self.outer_aperture = scene.Ellipse(center=(0, 0), radius=(0, 0), border_color='blue', color=(0, 0, 0, 0))
        self.inner_aperture.transform = transform
        self.gap_aperture.transform = transform
        self.outer_aperture.transform = transform
        
    def update_value(self):
        pass
        
    def draw_aperture(self, display_window, x, y):
        if x is not None and y is not None:
            self.inner_aperture.center = (x, y)
            self.gap_aperture.center = (x, y)
            self.outer_aperture.center = (x, y)
            self.inner_aperture.radius = (self.ui.major_axis.value(), self.ui.minor_axis.value())
            self.gap_aperture.radius = (self.ui.major_axis.value() + 2*self.ui.gap.value(), self.ui.minor_axis.value() + 2*self.ui.gap.value())
            self.outer_aperture.radius = (self.ui.major_axis.value() + 2 * self.ui.gap.value() + 2*self.ui.background.value(), self.ui.minor_axis.value() + 2 * self.ui.gap.value() + 2*self.ui.background.value())
            if self.inner_aperture.parent != display_window.view.scene:
                display_window.view.add(self.inner_aperture)
                display_window.view.add(self.gap_aperture)
                display_window.view.add(self.outer_aperture)
                
    def close(self):
        self.main_window.aperture_window = None
        super().close()