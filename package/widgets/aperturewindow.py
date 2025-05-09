from PyQt5 import QtWidgets
import numpy as np
from vispy import scene
from photutils.centroids import centroid_2dg

from ..ui import aperturewindow_ui
from .objectswindow import ObjectsWindow

class ApertureWindow(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.ui = aperturewindow_ui.Ui_ApertureWindow()
        self.ui.setupUi(self)
        self.main_window = main_window
        self.ui.major_axis.valueChanged.connect(self.update_value)
        self.ui.minor_axis.valueChanged.connect(self.update_value)
        self.ui.angle.valueChanged.connect(self.update_value)
        self.ui.gap.valueChanged.connect(self.update_value)
        self.ui.background.valueChanged.connect(self.update_value)
        self.aperture = None
        self.inner_aperture = None
        self.gap_aperture = None
        self.outer_aperture = None
        self.init_aperture()
        self.current_display_window = None
        self.current_x = None
        self.current_y = None
        self.drawing = True
        
    def update_value(self):
        self.draw_aperture(self.current_display_window, self.current_x, self.current_y)
            
    def draw_aperture(self, display_window, x, y):
        if x is None or y is None:
            return
        if self.drawing:
            self.current_x, self.current_y = x, y
        else:
            x, y = self.current_x, self.current_y
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
        if self.aperture.parent is None and display_window is not None:
            self.aperture.parent = display_window.view.scene
            
    def init_aperture(self):
        self.drawing = True
        self.aperture = scene.Node()
        self.inner_aperture = scene.Ellipse(center=(0, 0), radius=(0, 0), border_color='red', color=(0, 0, 0, 0), parent=self.aperture)
        self.gap_aperture = scene.Ellipse(center=(0, 0), radius=(0, 0), border_color='yellow', color=(0, 0, 0, 0), parent=self.aperture)
        self.outer_aperture = scene.Ellipse(center=(0, 0), radius=(0, 0), border_color='blue', color=(0, 0, 0, 0), parent=self.aperture)
            
    def toggle_drawing(self, display_window, x, y):
        if self.drawing:
            centroid_x, centroid_y = self.get_centroid(display_window, x, y)
            self.current_x, self.current_y = centroid_x, centroid_y
            self.inner_aperture.center = (centroid_x, centroid_y)
            self.gap_aperture.center = (centroid_x, centroid_y)
            self.outer_aperture.center = (centroid_x, centroid_y)
        else:
            self.aperture.visible = True
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
        angle_c = np.cos(angle)
        angle_s = np.sin(angle)
        for i in range(int(y-temp), int(y + temp)):
            for j in range(int(x-temp), int(x + temp)):
                i_2 = i-y
                j_2 = j-x
                i_3 = i_2*angle_c - j_2*angle_s
                j_3 = i_2*angle_s + j_2*angle_c
                if (i_3/a)**2 + (j_3/b)**2 <= 1:
                    mask[int(i-y+temp), int(j-x+temp)] = True
        centroid_x, centroid_y = centroid_2dg(inner_pixels, mask=mask)
        if centroid_x < 0 or centroid_x >= inner_pixels.shape[1] or centroid_y < 0 or centroid_y >= inner_pixels.shape[0]:
            return x, y
        return centroid_x + x - temp, centroid_y + y - temp
    
    def add_new_object(self, display_window, x, y):
        centroid_x, centroid_y = self.get_centroid(display_window, x, y)
        major_axis = self.ui.major_axis.value()
        minor_axis = self.ui.minor_axis.value()
        angle = self.ui.angle.value()
        gap = self.ui.gap.value()
        background = self.ui.background.value()
        intensity, snr = self.get_intensity(display_window, centroid_x, centroid_y, major_axis, minor_axis, angle, gap, background)
        if self.main_window.objects_window:
            self.main_window.objects_window.add_new_object(
                display_window,
                centroid_x,
                centroid_y,
                major_axis,
                minor_axis,
                angle,
                gap,
                background,
                intensity,
                snr)
            self.main_window.objects_window.raise_()
        else:
            self.main_window.objects_window = ObjectsWindow(self.main_window)
            self.main_window.objects_window.add_new_object(
                display_window,
                centroid_x,
                centroid_y,
                major_axis,
                minor_axis,
                angle,
                gap,
                background,
                intensity, 
                snr)
            self.main_window.objects_window.show()

    @staticmethod
    def get_intensity(display_window, x, y, major_axis, minor_axis, angle, gap, background):
        if major_axis >= minor_axis:
            temp = major_axis
            a = major_axis/2
            b = minor_axis/2
        else:
            temp = minor_axis
            a = minor_axis/2
            b = major_axis/2
        inner_mask = np.zeros(display_window.image.shape, dtype=bool)
        background_mask = np.zeros(display_window.image.shape, dtype=bool)
        gap_mask = np.zeros(display_window.image.shape, dtype=bool)
        display_window.ui.progressBar.setValue(0)
        total_pixels = (temp+gap+background)**2
        count = 0
        for i in range(int(y - temp - gap - background), int(y + temp + gap + background)):
            for j in range(int(x - temp - gap - background), int(x + temp + gap + background)):
                i_2 = i-y
                j_2 = j-x
                i_3 = i_2*np.cos(angle) - j_2*np.sin(angle)
                j_3 = i_2*np.sin(angle) + j_2*np.cos(angle)
                if (i_3/a)**2 + (j_3/b)**2 <= 1:
                    inner_mask[int(i), int(j)] = True
                if (i_3/(a + gap + background))**2 + (j_3/(b + gap + background))**2 <= 1:
                    background_mask[int(i), int(j)] = True
                if (i_3/(a + gap))**2 + (j_3/(b + gap))**2 <= 1:
                    gap_mask[int(i), int(j)] = True
                count += 1
            display_window.ui.progressBar.setValue(int(count/total_pixels*100))
            display_window.canvas.update()
        inner_pixels = display_window.image[inner_mask]
        background_pixels = display_window.image[background_mask & ~gap_mask]
        intensity = np.sum(inner_pixels - np.mean(background_pixels))
        snr = intensity / (np.std(background_pixels)*np.sqrt(len(inner_pixels)))
        return intensity, snr

    def closeEvent(self, event):
        self.main_window.aperture_window = None
        self.aperture.visible = False
        super().closeEvent(event)