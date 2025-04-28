from PyQt5 import QtWidgets, QtGui, QtCore
from astropy.io import fits
import numpy as np

from .ui import mainwindow_ui
from .widgets.displaywindow import DisplayWindow
from .widgets.histogramwindow import HistogramWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = mainwindow_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("../assets/splash.ico"))
        self.setWindowTitle("Photometry v2.0")
        self.ui.action_Open.triggered.connect(self.action_Open)
        self.ui.actionSave_All.triggered.connect(self.action_SaveAll)
        self.ui.actionHistogram.triggered.connect(self.action_Histogram)
        self.display_windows: list[DisplayWindow] = []
        self.limit = ()
        self.current_display_window = None
        self.histogram_window = None
        self.aperture_window = None
    def action_SaveAll(self):
        print("Save All")
        
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
                    
    def action_Histogram(self):
        self.histogram_window = HistogramWindow(self)
        self.histogram_window.show()
                
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
            super().closeEvent(event)
        else:
            event.ignore()
        