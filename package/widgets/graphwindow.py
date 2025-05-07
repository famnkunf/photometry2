from PyQt5 import QtWidgets, QtCore
from vispy import scene
from vispy.geometry import Rect

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
        self.canvas = scene.SceneCanvas(keys='interactive', show=True, parent=self.ui.graph)
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = scene.PanZoomCamera(rect=Rect(0, 0, 1, 1), aspect=1)
        self.ui.comboBox.currentIndexChanged.connect(self.update_graph_type)
        self.drawing = False
        
    def update_graph_type(self):
        graph_type = self.ui.comboBox.currentText()
        if graph_type == "Line":
            self.plot_line_graph()
        elif graph_type == "Horizontal Box":
            self.plot_box_graph()
        elif graph_type == "Area":
            self.plot_area_graph()
        elif graph_type == "None":
            self.drawing = False

    def plot_line_graph(self):
        print("Plotting line graph")
        self.drawing = True
        pass
    
    def plot_box_graph(self):
        print("Plotting box graph")
        self.drawing = True
        pass
    
    def plot_area_graph(self):
        print("Plotting area graph")
        self.drawing = True
        pass
        
    def closeEvent(self, a0):
        self.main_window.graph_window = None
        return super().closeEvent(a0)