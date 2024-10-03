import sys
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QVBoxLayout, QWidget, QApplication, QLabel, QComboBox
from PyQt5.QtCore import Qt
from edgeDetection import EdgeDetectionFeatureWindow
from histogram import HistogramFeatureWindow
from faceRecognition import FaceDetectionFeatureWindow
from imageSegmentation import ColorSegmentationApp  # Import the segmentation feature
from imageCropper import ImageCropperWindow

class MainMenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Main Menu')
        self.setGeometry(0, 0, 400, 300)  # Adjust window size as needed
        cwa = self.frameGeometry()
        cwc = QDesktopWidget().availableGeometry().center()
        cwa.moveCenter(cwc)
        self.move(cwa.topLeft())

        # Main layout for the menu
        layout = QVBoxLayout()

        # Title label
        self.title_label = QLabel('Select a Feature', self)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333333; padding: 5px;")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        # Combo box
        self.feature_combo = QComboBox(self)
        self.feature_combo.addItem("Histogram Equalization")
        self.feature_combo.addItem("Face & Blur Detection")
        self.feature_combo.addItem("Edge Detection")
        self.feature_combo.addItem("Image Segmentation")  # Add Image Segmentation option
        self.feature_combo.addItem("Image Cropper")
        self.feature_combo.activated[str].connect(self.open_feature)
        layout.addWidget(self.feature_combo, alignment=Qt.AlignCenter)

        # Set main layout to the central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_feature(self, feature_name):
        if feature_name == "Histogram Equalization":
            self.histogram_window = HistogramFeatureWindow()
            self.histogram_window.show()
        elif feature_name == "Face & Blur Detection":
            self.face_detection_window = FaceDetectionFeatureWindow()
            self.face_detection_window.show()
        elif feature_name == "Edge Detection":
            self.edge_detection_window = EdgeDetectionFeatureWindow()
            self.edge_detection_window.show()
        elif feature_name == "Image Segmentation":  # Handle segmentation feature
            self.segmentation_window = ColorSegmentationApp()
            self.segmentation_window.show()
        elif feature_name == "Image Cropper": 
            self.image_cropper = ImageCropperWindow()
            self.image_cropper.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainMenuWindow()
    main_window.show()
    sys.exit(app.exec_())
