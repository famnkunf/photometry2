from PyQt5 import QtWidgets, QtCore, QtGui
from vispy import scene, util

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
        self.ui.export_button.clicked.connect(self.export_objects)
        self.ui.objects_table.cellChanged.connect(self.update_object)
        
    def add_new_object(self, display_window, x, y, major_axis, minor_axis, angle, gap, background, intensity):
        aperture = scene.Node(parent=display_window.view.scene)
        inner_aperture = scene.Ellipse(center=(x, y), radius=(major_axis, minor_axis), border_color='yellow', color=(0, 0, 0, 0), parent=aperture)
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
            'x': x,
            'y': y,
            'major_axis': major_axis,
            'minor_axis': minor_axis,
            'angle': angle,
            'gap': gap,
            'background': background,
            'aperture': aperture,
            'intensity': intensity,
            'aperture': aperture,
            'name': '',
            'notes': '',
        }
        self.objects.append(new_object)
        self.update_table()
        
    def update_object(self, row, column):
        if row >= len(self.objects):
            return
        if column == 0:
            return
        if column == 2:
            self.objects[row]['x'] = float(self.ui.objects_table.item(row, column).text())
        elif column == 3:
            self.objects[row]['y'] = float(self.ui.objects_table.item(row, column).text())
        elif column == 9:
            self.objects[row]['intensity'] = float(self.ui.objects_table.item(row, column).text())
        elif column == 10:
            self.objects[row]['name'] = self.ui.objects_table.item(row, column).text()
        elif column == 11:
            self.objects[row]['notes'] = self.ui.objects_table.item(row, column).text()
        print(row, column)
    
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
        for i in range(3, 9):
            self.ui.objects_table.hideColumn(i)
        self.ui.objects_table.resizeColumnsToContents()
        self.ui.objects_table.resizeRowsToContents()
        self.ui.objects_table.setSortingEnabled(True)
        self.ui.objects_table.sortByColumn(0, QtCore.Qt.AscendingOrder)
        
    def export_objects(self):
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Objects", "", "CSV files (*.csv);;All files (*)")
        if file_name:
            with open(file_name, 'w') as f:
                f.write("ID,X,Y,Intensity,Name,Notes\n")
                for obj in self.objects:
                    f.write(f"{obj['id']},{obj['x']},{obj['y']},{obj['intensity']},{obj['name']},{obj['notes']}\n")
        
    def closeEvent(self, a0):
        return super().closeEvent(a0)

        