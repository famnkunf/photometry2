from PyQt5 import QtWidgets, QtGui, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import matplotlib as mpl
from matplotlib import pyplot as plt
from astropy.visualization import ImageNormalize, LinearStretch

from ..ui import displaywindow_ui
from .headerwindow import HeaderWindow

mpl.use('Qt5Agg')
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
        self.figure, self.ax = plt.subplots()
        self.ax.axis('off')
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.hide()
        self.norm = ImageNormalize(self.image, stretch=LinearStretch())
        self.norm.vmin = self.image.mean() - 0 * self.image.std()
        self.norm.vmax = self.image.mean() + 0.5 * self.image.std()
        self.ui.verticalLayout_2.addWidget(self.canvas)
        self.ui.OpenHeader.clicked.connect(self.open_header)
        self.ui.pan_and_zoom.clicked.connect(self.pan_and_zoom)
        self.ui.home.clicked.connect(self.toolbar.home)
        self.plot_image()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.main_window = main_window
        
    def pan_and_zoom(self):
        self.toolbar.pan()
        
    def focusInEvent(self, event: QtGui.QFocusEvent):
        if self.main_window.histogram_window:
            self.main_window.histogram_window.set_data(self)
        return super().focusInEvent(event)
    
    def plot_image(self):
        self.ax.imshow(self.image, cmap='gray', norm=self.norm, interpolation='bicubic', interpolation_stage='data')
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
        
        