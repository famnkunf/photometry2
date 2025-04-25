from astropy.io import fits
from PyQt5.QtWidgets import QFileDialog, QHBoxLayout, QPushButton, QWidget, QVBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photometry 2.0")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.hbox = QHBoxLayout()
        main_layout.addLayout(self.hbox)
        main_layout.addStretch(1)

        self.open_fits_file_button = QPushButton("Open FITS File", self)
        self.open_fits_file_button.setToolTip("Click to open a FITS file")
        self.open_fits_file_button.clicked.connect(self.open_fits_file)
        self.hbox.addWidget(self.open_fits_file_button)
        self.hbox.addStretch(1)
        

    def open_fits_file(self):
        options = QFileDialog.Options()
        filenames, _ = QFileDialog.getOpenFileNames(self, "Open FITS File", "", "FITS Files (*.fits *.fit);;All Files (*)", options=options)
        if filenames:
            for filename in filenames:
                self.load_fits_file(filename)

    def load_fits_file(self, file_name):
        with fits.open(file_name) as hdul:
            pass