from .mainwindow import MainWindow
from PyQt5.QtWidgets import QApplication

def loop():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
    
if __name__ == "__main__":
    loop()