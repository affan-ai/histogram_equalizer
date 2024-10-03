import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget, QMessageBox, QApplication
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class NegativeFilterWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Negative Filter Feature')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.upload_button = QPushButton('Upload Image', self)
        self.upload_button.setFixedSize(150, 40)
        self.upload_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px;")
        self.upload_button.clicked.connect(self.upload_image)
        layout.addWidget(self.upload_button, alignment=Qt.AlignLeft)

        self.negative_button = QPushButton('Apply Negative Filter', self)
        self.negative_button.setFixedSize(150, 40)
        self.negative_button.setStyleSheet("background-color: #2196F3; color: white; border-radius: 5px;")
        self.negative_button.clicked.connect(self.apply_negative_filter)
        layout.addWidget(self.negative_button, alignment=Qt.AlignLeft)

        self.image_label = QLabel('Image will be displayed here', self)
        self.image_label.setStyleSheet("border: 2px solid #cccccc; background-color: #ffffff;")
        self.image_label.setFixedHeight(400)
        layout.addWidget(self.image_label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.image = None

    def upload_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp)", options=options)
        if file_name:
            self.image = cv2.imread(file_name)
            self.display_image(self.image)

    def apply_negative_filter(self):
        if self.image is not None:
            # Apply negative filter
            negative_image = 255 - self.image
            self.display_image(negative_image)
        else:
            QMessageBox.warning(self, 'Warning', 'No image uploaded!')

    def display_image(self, image):
        height, width, channel = image.shape
        bytes_per_line = channel * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.image_label.setAlignment(Qt.AlignCenter)
