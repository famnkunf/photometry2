from PyQt5 import QtWidgets, QtCore
from vispy import scene
import numpy as np

from ..ui.objectswindow_ui import Ui_ObjectsWindow

class ObjectsWindow(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.ui = Ui_ObjectsWindow()
        self.ui.setupUi(self)
        self.main_window = main_window
        self.setWindowTitle("Objects")
        self.setGeometry(1000, 200, 500, 400)
        self.objects = []
        self.selected_object = None
        self.selected_object_marker = None
        self.ui.export_button.clicked.connect(self.export_objects)
        self.ui.objects_table.cellChanged.connect(self.update_object)
        self.ui.objects_table.itemSelectionChanged.connect(self.update_selected_object)
        
    def add_new_object(self, display_window, x, y, major_axis, minor_axis, angle, gap, background, intensity, snr):
        aperture = scene.Node(parent=display_window.view.scene)
        scene.Ellipse(center=(x, y), radius=(major_axis, minor_axis), border_color='yellow', color=(0, 0, 0, 0), parent=aperture)
        gap_aperture = scene.Ellipse(center=(x, y), radius=(major_axis + 2*gap, minor_axis + 2*gap), border_color='yellow', color=(0, 0, 0, 0), parent=aperture)
        outer_aperture = scene.Ellipse(center=(x, y), radius=(major_axis + 2 * gap + 2*background, minor_axis + 2 * gap + 2*background), border_color='yellow', color=(0, 0, 0, 0), parent=aperture)
        gap_aperture.border._connect = "segments"
        outer_aperture.border._connect = "segments"
        transform = scene.MatrixTransform()
        transform.translate((-x, -y, -1))
        transform.rotate(angle, (0, 0, 1))
        transform.translate((x, y, 0))
        aperture.transform = transform
        new_object = {
            'id': len(self.objects),
            'x': round(x, 2),
            'y': round(y, 2),
            'intensity': round(intensity, 2),
            'snr': round(snr, 2),
            'name': '',
            'notes': '',
            'major_axis': major_axis,
            'minor_axis': minor_axis,
            'angle': angle,
            'gap': gap,
            'background': background,
            'aperture': aperture,
            'display_window': display_window,
            'file_name': display_window.title.split("/")[-1],
        }
        self.objects.append(new_object)
        self.update_table()
    
    def update_selected_object(self):
        if len(self.ui.objects_table.selectedItems()) > 0:
            if self.selected_object_marker is not None:
                self.selected_object_marker.parent = None
            self.selected_object_marker = scene.Markers()
            self.selected_object_marker.transform = scene.STTransform(translate=(0, 0, -1), scale=(1, 1, 1))
            row = self.ui.objects_table.selectedItems()[0].row()
            if row >= len(self.objects):
                return
            self.selected_object: dict = self.objects[row]
            x, y = self.selected_object['x'], self.selected_object['y']
            display_window = self.selected_object['display_window']
            if not display_window.isVisible():
                return
            self.selected_object_marker.parent = display_window.view.scene
            self.selected_object_marker.set_data(pos=np.array([[x, y]]), face_color='red', size=10)
            self.selected_object['display_window'].raise_()
        else:
            self.selected_object = {}
            if self.selected_object_marker is not None:
                self.selected_object_marker.parent = None

    def keyPressEvent(self, a0):
        if a0.key() == QtCore.Qt.Key_Delete:
            if self.selected_object is not None:
                self.selected_object['aperture'].parent = None
                self.objects.remove(self.selected_object)
                self.ui.objects_table.removeRow(self.ui.objects_table.selectedItems()[0].row())
                self.selected_object = None
                self.update_table()
        return super().keyPressEvent(a0)
        
    def update_object(self, row, column):
        if row >= len(self.objects):
            return
        if column == 0:
            return
        if column == 1:
            self.objects[row]['x'] = float(self.ui.objects_table.item(row, column).text())
        elif column == 2:
            self.objects[row]['y'] = float(self.ui.objects_table.item(row, column).text())
        elif column == 3:
            self.objects[row]['intensity'] = float(self.ui.objects_table.item(row, column).text())
        elif column == 4:
            self.objects[row]['snr'] = float(self.ui.objects_table.item(row, column).text())
        elif column == 5:
            self.objects[row]['name'] = self.ui.objects_table.item(row, column).text()
        elif column == 6:
            self.objects[row]['notes'] = self.ui.objects_table.item(row, column).text()
    
    def update_table(self):
        if len(self.objects) == 0:
            return
        self.ui.objects_table.setColumnCount(len(self.objects[0].keys()))
        self.ui.objects_table.setRowCount(len(self.objects))
        for i, k in enumerate(self.objects[0].keys()):
            self.ui.objects_table.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(k))
        for i, obj in enumerate(self.objects):
            for j, k in enumerate(obj.keys()):
                item = QtWidgets.QTableWidgetItem(str(obj[k]))
                self.ui.objects_table.setItem(i, j, item)
        for i in range(7, 15):
            self.ui.objects_table.hideColumn(i)
        self.ui.objects_table.resizeColumnsToContents()
        self.ui.objects_table.resizeRowsToContents()
        self.ui.objects_table.setSortingEnabled(True)
        self.ui.objects_table.sortByColumn(0, QtCore.Qt.AscendingOrder)
        
    def export_objects(self):
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Objects", "", "CSV files (*.csv);;All files (*)")
        if file_name:
            with open(file_name, 'w') as f:
                f.write("ID,X,Y,Intensity,SNR,Name,Notes\n")
                for obj in self.objects:
                    f.write(f"{obj['id']},{obj['x']},{obj['y']},{obj['intensity']},{obj['snr']},{obj['name']},{obj['notes']+'-'+obj['file_name']}\n")
        
    def closeEvent(self, a0):
        self.main_window.objects_window = None
        return super().closeEvent(a0)

        