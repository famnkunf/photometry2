from PyQt5 import QtWidgets, QtGui, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import matplotlib as mpl
from matplotlib import pyplot as plt
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
        self.plot_image()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.main_window = main_window
        
    def focusInEvent(self, event: QtGui.QFocusEvent):
        if self.main_window.histogram_window:
            self.main_window.histogram_window.set_data(self)
        return super().focusInEvent(event)

    def on_zoom(self, event):
        pass
            
    def on_mouse_move(self, event):
        transform = self.image_scene.get_transform(map_to='canvas')
        if event.pos is not None:
            x, y, _, _= transform.imap(event.pos)
            if self.main_window.aperture_window:
                self.main_window.aperture_window.draw_aperture(self, x, y)
            self.canvas.update()
    
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
        
        