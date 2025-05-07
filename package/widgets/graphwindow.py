from PyQt5 import QtWidgets, QtCore, QtGui

from ..ui.graphwindow_ui import Ui_GraphWindow

class GraphWindow(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.ui = Ui_GraphWindow()
        self.ui.setupUi(self)
        self.main_window = main_window
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setWindowTitle("Graph Window")
        self.graph_data = None 
        
    def closeEvent(self, a0):
        self.main_window.graph_window = None
        return super().closeEvent(a0)