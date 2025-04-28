from ..ui import headerwindow_ui
from PyQt5 import QtWidgets

class HeaderWindow(QtWidgets.QWidget):
    def __init__(self, header_data, title):
        super().__init__()
        self.ui = headerwindow_ui.Ui_HeaderWindow()
        self.ui.setupUi(self)
        self.header_data = header_data
        self.title = title
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, 800, 600)
        self.display_header()

    def display_header(self):
        header_text = "\n".join([f"{key}: {value}" for key, value in self.header_data.items()])
        self.ui.textBrowser.setPlainText(header_text)
        self.ui.textBrowser.setReadOnly(True)
        self.ui.verticalScrollBar.setVisible(True)
        self.ui.horizontalScrollBar.setVisible(True)
        self.ui.textBrowser.setVerticalScrollBar(self.ui.verticalScrollBar)
        self.ui.textBrowser.setHorizontalScrollBar(self.ui.horizontalScrollBar)
        self.ui.verticalScrollBar.setRange(0, self.ui.textBrowser.verticalScrollBar().maximum())
        self.ui.horizontalScrollBar.setRange(0, self.ui.textBrowser.horizontalScrollBar().maximum())
        self.ui.verticalScrollBar.valueChanged.connect(self.ui.textBrowser.verticalScrollBar().setValue)
        self.ui.horizontalScrollBar.valueChanged.connect(self.ui.textBrowser.horizontalScrollBar().setValue)
        self.ui.verticalScrollBar.setPageStep(10)
        self.ui.horizontalScrollBar.setPageStep(10)
        self.ui.verticalScrollBar.setSingleStep(1)
        self.ui.horizontalScrollBar.setSingleStep(1)
