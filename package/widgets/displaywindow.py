from PyQt5 import QtWidgets, QtGui, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from astropy.visualization import ImageNormalize, LinearStretch

from ..ui import displaywindow_ui
from .headerwindow import HeaderWindow

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
        self.canvas = FigureCanvas(Figure(figsize=(self.image.shape[1] / 100, self.image.shape[0] / 100), dpi=100))
        self.canvas.mpl_connect("motion_notify_event", self.on_mouse_move)
        self.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.canvas.mpl_connect('button_press_event', self.start_pan)
        self.canvas.mpl_connect('button_release_event', self.stop_pan)
        self.canvas.mpl_connect('motion_notify_event', self.on_pan)
        self.norm = ImageNormalize(self.image, stretch=LinearStretch())
        self.norm.vmin = self.image.mean() - 0 * self.image.std()
        self.norm.vmax = self.image.mean() + 0.5 * self.image.std()
        self.ui.verticalLayout_2.addWidget(self.canvas)
        self.ui.OpenHeader.clicked.connect(self.open_header)
        self.plot_image()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.main_window = main_window
        
    def on_mouse_move(self, event):
        if self.main_window.aperture_window:
            pass
    
    def on_scroll(self, event):
        pass
    
    def start_pan(self, event):
        pass

    def stop_pan(self, event):
        pass
    
    def on_pan(self, event):
        pass
    
    def focusInEvent(self, event: QtGui.QFocusEvent):
        if self.main_window.histogram_window:
            self.main_window.histogram_window.set_data(self)
        return super().focusInEvent(event)
    
    def plot_image(self):
        ax = self.canvas.figure.add_subplot(111)
        ax.imshow(self.image, cmap='gray', origin='lower', norm=self.norm)
        ax.axis('off')
        self.canvas.draw()
        
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
        
        