from PyQt5 import QtWidgets, QtGui, QtCore
import matplotlib as mpl
from astropy.visualization import ImageNormalize, LinearStretch
from vispy import app, scene
import numpy as np

from ..ui import displaywindow_ui
from .headerwindow import HeaderWindow

mpl.use('QtAgg')
class DisplayWindow(QtWidgets.QWidget):
    def __init__(self, image, title, header_data=None, main_window=None):
        super().__init__()
        self.ui = displaywindow_ui.Ui_DisplayWindow()
        self.ui.setupUi(self)
        self.image = image
        self.title = title
        self.header_data = header_data
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, 800, 600)
        self.canvas = scene.SceneCanvas(keys='interactive')
        self.view = self.canvas.central_widget.add_view(bgcolor='gray')
        self.image_scene = scene.Image(self.image,cmap='gray', parent=self.view.scene)
        self.view.camera = scene.PanZoomCamera(rect=(0, 0, self.image.shape[1], self.image.shape[0]), aspect=1)
        self.image_scene.clim = (self.image.mean() - 0. * self.image.std(), self.image.mean() + 0.5 * self.image.std())
        self.ui.verticalLayout_2.addWidget(self.canvas.native)
        self.ui.OpenHeader.clicked.connect(self.open_header)
        self.canvas.events.mouse_move.connect(self.on_mouse_move)
        self.canvas.events.mouse_wheel.connect(self.on_zoom)
        self.canvas.events.mouse_press.connect(self.on_mouse_click)
        self.canvas.events.mouse_double_click.connect(self.on_mouse_double_click)
        self.ui.home.clicked.connect(self.view.camera.reset)
        self.plot_image()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.main_window = main_window
        
    def focusInEvent(self, event: QtGui.QFocusEvent):
        if self.main_window.histogram_window:
            self.main_window.histogram_window.set_data(self)
        return super().focusInEvent(event)

    def on_zoom(self, event):
        pass
    
    def enterEvent(self, a0):
        if self.main_window.aperture_window:
            self.main_window.aperture_window.init_aperture(self, None, None)
        return super().enterEvent(a0)
    
    def leaveEvent(self, a0):
        if self.main_window.aperture_window:
            self.main_window.aperture_window.aperture.parent = None
            self.canvas.update()
        return super().leaveEvent(a0)
    
    def on_mouse_double_click(self, event):
        if self.main_window.aperture_window:
            transform = self.image_scene.get_transform(map_to='canvas')
            x, y, _, _= transform.imap(event.pos)
            self.main_window.aperture_window.add_new_object(self, x, y)
            self.main_window.aperture_window.aperture.visible = False
    
    def on_mouse_click(self, event):
        if self.main_window.aperture_window:
            if event.is_dragging:
                pass
            else:
                transform = self.image_scene.get_transform(map_to='canvas')
                x, y, _, _= transform.imap(event.pos)
                self.main_window.aperture_window.toggle_drawing(self, x, y)
            
    def on_mouse_move(self, event):
        transform = self.image_scene.get_transform(map_to='canvas')
        if event.pos is not None:
            x, y, _, _= transform.imap(event.pos)
            if self.main_window.aperture_window:
                self.main_window.aperture_window.draw_aperture(self, x, y)
    
    def plot_image(self):
        pass
            
    def open_header(self):
        if self.header_data is not None:
            self.header_window = HeaderWindow(self.header_data, self.title + " - Header")
            self.header_window.show()
        else:
            warning = QtWidgets.QMessageBox()
            warning.setIcon(QtWidgets.QMessageBox.Warning)
            warning.setText("No header data available.")
            warning.setWindowTitle("Error")
            warning.setStandardButtons(QtWidgets.QMessageBox.Ok)
            warning.exec_()
        self.ui.OpenHeader.setEnabled(False)
        
    def closeEvent(self, event):
        return super().closeEvent(event)
        