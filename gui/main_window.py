from astropy.io import fits
from PyQt5.QtWidgets import QFileDialog, QHBoxLayout, QPushButton, QWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photometry 2.0")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        self.setLayout(QHBoxLayout())
        self.open_fits_file_button = QPushButton("Open FITS File", self)
        self.open_fits_file_button.setToolTip("Click to open a FITS file")
        self.open_fits_file_button.clicked.connect(self.open_fits_file)
        self.layout().addWidget(self.open_fits_file_button)

    def open_fits_file(self):
        options = QFileDialog.Options()
        filenames, _ = QFileDialog.getOpenFileNames(self, "Open FITS File", "", "FITS Files (*.fits *.fit);;All Files (*)", options=options)
        if filenames:
            for filename in filenames:
                self.load_fits_file(filename)

    def load_fits_file(self, file_name):
        with fits.open(file_name) as hdul:
            pass