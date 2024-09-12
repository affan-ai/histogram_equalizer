# main_menu.py

import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QApplication, QLabel
from PyQt5.QtCore import Qt
from edgeDetection import EdgeDetectionFeatureWindow
from histogram import HistogramFeatureWindow
from faceRecognition import FaceDetectionFeatureWindow

class MainMenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Main Menu')
        self.setGeometry(100, 100, 400, 300)  # Adjust window size as needed

        # Main layout for the menu
        layout = QVBoxLayout()

        # Title label
        self.title_label = QLabel('Select a Feature', self)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333333; padding: 10px;")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        # Buttons for different features
        self.histogram_button = QPushButton('Histogram', self)
        self.histogram_button.setFixedSize(150, 40)
        self.histogram_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px;")
        self.histogram_button.clicked.connect(self.open_histogram_feature)
        layout.addWidget(self.histogram_button, alignment=Qt.AlignCenter)

        self.face_detection_button = QPushButton('Face Detection', self)
        self.face_detection_button.setFixedSize(150, 40)
        self.face_detection_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px;")
        self.face_detection_button.clicked.connect(self.open_face_detection_feature)
        layout.addWidget(self.face_detection_button, alignment=Qt.AlignCenter)

        self.edge_detection_button = QPushButton('Edge Detection', self)
        self.edge_detection_button.setFixedSize(150, 40)
        self.edge_detection_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px;")
        self.edge_detection_button.clicked.connect(self.open_edge_detection_feature)
        layout.addWidget(self.edge_detection_button, alignment=Qt.AlignCenter)

        # Set main layout to the central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_histogram_feature(self):
        self.histogram_window = HistogramFeatureWindow()
        self.histogram_window.show()

    def open_face_detection_feature(self):
        self.face_detection_window = FaceDetectionFeatureWindow()
        self.face_detection_window.show()

    def open_edge_detection_feature(self):
        self.edge_detection_window = EdgeDetectionFeatureWindow()
        self.edge_detection_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainMenuWindow()
    main_window.show()
    sys.exit(app.exec_())
