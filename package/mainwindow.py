from PyQt5 import QtWidgets, QtGui, QtCore
from astropy.io import fits
import numpy as np

from .ui import mainwindow_ui
from .widgets.displaywindow import DisplayWindow
from .widgets.histogramwindow import HistogramWindow
from .widgets.aperturewindow import ApertureWindow
from .widgets.objectswindow import ObjectsWindow
from .widgets.graphwindow import GraphWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = mainwindow_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Photometry v2.0")
        self.setMinimumSize(600, 500)
        self.resize(600, 500)
        self.ui.action_Open.triggered.connect(self.action_Open)
        self.ui.actionCloseAll.triggered.connect(self.action_CloseAll)
        self.ui.actionHistogram.triggered.connect(self.action_Histogram)
        self.ui.actionAperture.triggered.connect(self.action_Aperture)
        self.ui.actionObjects.triggered.connect(self.action_Objects)
        self.ui.actionGraph.triggered.connect(self.action_Graph)
        self.ui.actionTiled.triggered.connect(self.action_Tiled)
        # self.ui.mdiArea.setViewMode(QtWidgets.QMdiArea.TabbedView)
        self.ui.mdiArea.setViewMode(QtWidgets.QMdiArea.SubWindowView)
        self.ui.mdiArea.tileSubWindows()
        self.display_windows: list[DisplayWindow] = []
        self.limit = ()
        self.current_display_window = None
        self.histogram_window = None
        self.aperture_window = None
        self.objects_window = None
        self.graph_window = None
        self.ui.actionObjects.trigger()
        self.ui.actionAperture.trigger()
        self.ui.actionHistogram.trigger()
        self.ui.actionGraph.trigger()
        
    def action_CloseAll(self):
        for display_window in self.display_windows:
            display_window.close()
        self.display_windows.clear()
        
    def action_Open(self):
        file_names, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Open FITS file", "", "FITS files (*.fits *.fit);;All files (*)")
        if file_names:
            for file_name in file_names:
                try:
                    with fits.open(file_name) as hdul:
                        image_data = hdul[0].data
                        if image_data is not None:
                            display_window = DisplayWindow(image_data, file_name, header_data=hdul[0].header, main_window=self)
                            display_window.show()
                            self.display_windows.append(display_window)
                        else:
                            print("No image data found in the FITS file.")
                except Exception as e:
                    print(f"Error opening FITS file: {e}")
                    
    def action_Graph(self):
        if self.graph_window is None:
            self.graph_window = GraphWindow(self)
            self.ui.mdiArea.addSubWindow(self.graph_window)
            self.graph_window.show()
        else:
            self.graph_window.raise_()
                    
    def action_Objects(self):
        if self.objects_window is None:
            self.objects_window = ObjectsWindow(self)
            self.ui.mdiArea.addSubWindow(self.objects_window)
            self.objects_window.show()
        else:
            self.objects_window.raise_()
                    
    def action_Histogram(self):
        if self.histogram_window is None:
            self.histogram_window = HistogramWindow(self)
            self.ui.mdiArea.addSubWindow(self.histogram_window)
            self.histogram_window.show()
        else:
            self.histogram_window.raise_()

    def action_Aperture(self):
        if self.aperture_window is None:
            self.aperture_window = ApertureWindow(self)
            self.ui.mdiArea.addSubWindow(self.aperture_window)
            self.aperture_window.show()
        else:
            self.aperture_window.raise_()
                
    def action_Tiled(self):
        if self.ui.mdiArea.subWindowList():
            self.ui.mdiArea.tileSubWindows()
                
    def closeEvent(self, event):
        question_box = QtWidgets.QMessageBox(self)
        question_box.setWindowFlags(question_box.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        question_box.setWindowTitle("Exit")
        question_box.setText("Are you sure you want to exit?")
        question_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        question_box.setDefaultButton(QtWidgets.QMessageBox.No)
        result = question_box.exec_()
        if result == QtWidgets.QMessageBox.Yes:
            event.accept()
            if self.histogram_window:
                self.histogram_window.close()
            for display_window in self.display_windows:
                display_window.close()
            if self.aperture_window:
                self.aperture_window.close()
            if self.objects_window:
                self.objects_window.close()
            if self.graph_window:
                self.graph_window.close()
            super().closeEvent(event)
        else:
            event.ignore()
        