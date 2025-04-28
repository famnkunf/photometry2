from PyQt5 import QtWidgets, QtCore

from ..ui import aperturewindow_ui

class ApertureWindow(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__(None, QtCore.Qt.WindowStaysOnTopHint)
        self.ui = aperturewindow_ui.Ui_ApertureWindow()
        self.ui.setupUi(self)
        self.main_window = main_window
    
    def close(self):
        self.main_window.aperture_window = None
        super().close()