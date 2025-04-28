from PyQt5 import QtWidgets, QtCore

from ..ui import aperturewindow_ui

class ApertureWindow(QtWidgets.QWidget):
    def __init__(self, display_window):
        super().__init__(None, QtCore.Qt.WindowStaysOnTopHint)
        self.ui = aperturewindow_ui.Ui_ApertureWindow()
        self.ui.setupUi(self)
        self.display_window = display_window
    
    def close(self):
        self.display_window.aperture_window = None
        super().close()