from PyQt5 import QtWidgets, QtCore, QtGui
import numpy as np
from vispy import scene
from photutils.centroids import centroid_2dg

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
        self.aperture = scene.Node(parent=None)
        self.aperture.transform = transform
        self.inner_aperture = scene.Ellipse(center=(0, 0), radius=(0, 0), border_color='red', color=(0, 0, 0, 0), parent=self.aperture)
        self.gap_aperture = scene.Ellipse(center=(0, 0), radius=(0, 0), border_color='yellow', color=(0, 0, 0, 0), parent=self.aperture)
        self.outer_aperture = scene.Ellipse(center=(0, 0), radius=(0, 0), border_color='blue', color=(0, 0, 0, 0), parent=self.aperture)
        self.current_display_window = None
        self.current_x = None
        self.current_y = None
        self.objects = []
        self.drawing = True
        
    def update_value(self):
        self.draw_aperture(self.current_display_window, self.current_x, self.current_y)
            
    def draw_aperture(self, display_window, x, y):
        if self.drawing:
            if x is not None and y is not None:
                self.current_x, self.current_y = x, y
                self.inner_aperture.center = (x, y)
                self.gap_aperture.center = (x, y)
                self.outer_aperture.center = (x, y)
                self.inner_aperture.radius = (self.ui.major_axis.value(), self.ui.minor_axis.value())
                self.gap_aperture.radius = (self.ui.major_axis.value() + 2*self.ui.gap.value(), self.ui.minor_axis.value() + 2*self.ui.gap.value())
                self.outer_aperture.radius = (self.ui.major_axis.value() + 2 * self.ui.gap.value() + 2*self.ui.background.value(), self.ui.minor_axis.value() + 2 * self.ui.gap.value() + 2*self.ui.background.value())
                if self.inner_aperture.parent != display_window.view.scene:
                    self.current_display_window = display_window
                    display_window.view.add(self.aperture)
                    
    def toggle_drawing(self, display_window, x, y):
        if self.drawing:
            centroid_x, centroid_y = self.get_centroid(display_window, x, y)
            self.inner_aperture.center = (centroid_x, centroid_y)
            self.gap_aperture.center = (centroid_x, centroid_y)
            self.outer_aperture.center = (centroid_x, centroid_y)
        self.drawing = not self.drawing
        
        
    def get_centroid(self, display_window, x, y):
        a = self.ui.major_axis.value()
        b = self.ui.minor_axis.value()
        angle = np.deg2rad(self.ui.angle.value())
        if a >= b:
            temp = a
        else:
            temp = b
        inner_pixels = display_window.image[int(y - temp):int(y + temp), int(x - temp):int(x + temp)]
        centroid_x, centroid_y = centroid_2dg(inner_pixels)
        if centroid_x < 0 or centroid_x >= inner_pixels.shape[1] or centroid_y < 0 or centroid_y >= inner_pixels.shape[0]:
            return x, y
        return (centroid_x + x - temp, centroid_y + y - temp)                
    def closeEvent(self, event):
        self.main_window.aperture_window = None
        self.aperture.visible = False
        super().closeEvent(event)