from PyQt5 import QtWidgets, QtCore, QtGui
import numpy as np
from vispy import scene, util
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
                transform = scene.MatrixTransform()
                transform.translate((-x, -y, -1))
                transform.rotate(self.ui.angle.value(), (0, 0, 1))
                transform.translate((x, y, 0))
                self.aperture.transform = transform
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
        major_axis = self.ui.major_axis.value()
        minor_axis = self.ui.minor_axis.value()
        angle = np.deg2rad(self.ui.angle.value())
        if major_axis >= minor_axis:
            temp = major_axis
            a = major_axis/2
            b = minor_axis/2
        else:
            temp = minor_axis
            a = minor_axis/2
            b = major_axis/2
        inner_pixels = display_window.image[int(y - temp):int(y + temp), int(x - temp):int(x + temp)]
        mask = np.zeros(inner_pixels.shape, dtype=bool)
        for i in range(int(y-temp), int(y + temp)):
            for j in range(int(x-temp), int(x + temp)):
                i_2 = i-y
                j_2 = j-x
                i_3 = i_2*np.cos(angle) - j_2*np.sin(angle)
                j_3 = i_2*np.sin(angle) + j_2*np.cos(angle)
                if (i_3/a)**2 + (j_3/b)**2 <= 1:
                    mask[int(i-y+temp), int(j-x+temp)] = True
        centroid_x, centroid_y = centroid_2dg(inner_pixels, mask=mask)
        if centroid_x < 0 or centroid_x >= inner_pixels.shape[1] or centroid_y < 0 or centroid_y >= inner_pixels.shape[0]:
            return x, y
        return (centroid_x + x - temp, centroid_y + y - temp)                
    def closeEvent(self, event):
        self.main_window.aperture_window = None
        self.aperture.visible = False
        super().closeEvent(event)