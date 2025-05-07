from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import pyplot as plt

from ..ui import histogramwindow_ui

class HistogramWindow(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.ui = histogramwindow_ui.Ui_Histogram()
        self.ui.setupUi(self)
        self.histogram_data = None
        self.title = "Histogram"
        self.setWindowTitle(self.title)
        self.setGeometry(1000, 200, 500, 400)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.ui.verticalLayout_4.addWidget(self.canvas)
        self.bin = 256
        self.main_window = main_window
        self.display_window = None
        self.scatter_plots = None
        self.hist = None
        self.ui.horizontalSlider.sliderReleased.connect(self.on_slider_release)
        self.ui.horizontalSlider.valueChanged.connect(self.on_slider_value_changed)
        self.ui.horizontalSlider_2.sliderReleased.connect(self.on_slider_release)
        self.ui.horizontalSlider_2.valueChanged.connect(self.on_slider_value_changed)
        self.ui.doubleSpinBox.editingFinished.connect(self.on_double_spin_box_finished)
        self.ui.doubleSpinBox_2.editingFinished.connect(self.on_double_spin_box_finished)

    def set_data(self, display_window=None):
        self.display_window = display_window
        self.histogram_data = display_window.image.flatten()
        self.title = display_window.title.split("/")[-1]
        self.setWindowTitle(self.title + " - Histogram")
        self.ui.label_3.setText(self.title)
        self.display_histogram()
        
    def on_double_spin_box_finished(self):
        if self.display_window:
            self.ui.horizontalSlider.setValue(int(self.ui.doubleSpinBox_2.value()*100))
            self.ui.horizontalSlider_2.setValue(int(self.ui.doubleSpinBox.value()*100))
            self.display_window.image_scene.clim = (self.ui.doubleSpinBox_2.value(), self.ui.doubleSpinBox.value())
        
    def on_slider_value_changed(self):
        self.ui.doubleSpinBox_2.setValue(self.ui.horizontalSlider.value()/100)
        self.ui.doubleSpinBox.setValue(self.ui.horizontalSlider_2.value()/100)
        self.update_markers()
        
    def on_slider_release(self):
        if self.display_window:
            self.display_window.image_scene.clim = (self.ui.horizontalSlider.value()/100, self.ui.horizontalSlider_2.value()/100)
        
    def update_markers(self):
        if self.scatter_plots is not None:
            self.scatter_plots[0].remove()
            self.scatter_plots[1].remove()
        self.scatter_plots = (self.ax.scatter(self.ui.horizontalSlider.value()/100, 0, color='red', marker='x', s=100, label='vmin'),
                             self.ax.scatter(self.ui.horizontalSlider_2.value()/100, 0, color='green', marker='x', s=100, label='vmax'))
        self.canvas.draw_idle()
            
    def display_histogram(self):
        min_val = self.histogram_data.mean() - 4 * self.histogram_data.std()
        max_val = self.histogram_data.mean() + 4 * self.histogram_data.std()
        self.ui.horizontalSlider.setRange(int(min_val*100), int(max_val*100))
        self.ui.horizontalSlider_2.setRange(int(min_val*100), int(max_val*100))
        self.ui.horizontalSlider.setValue(int(self.display_window.image_scene.clim[0]*100))
        self.ui.doubleSpinBox_2.setValue(self.display_window.image_scene.clim[0])
        self.ui.horizontalSlider_2.setValue(int(self.display_window.image_scene.clim[1]*100))
        self.ui.doubleSpinBox.setValue(self.display_window.image_scene.clim[1])
        self.scatter_plots = None
        self.ax.clear()
        self.hist = self.ax.hist(self.histogram_data, bins=self.bin, range=(min_val, max_val), color='blue', alpha=0.7)
        self.ax.set_title(self.title)
        self.ax.set_xlabel('Pixel Value')
        self.ax.set_ylabel('Frequency')
        self.update_markers()
        self.canvas.draw_idle()
        
    def closeEvent(self, event):
        self.main_window.histogram_window = None
        super().closeEvent(event)