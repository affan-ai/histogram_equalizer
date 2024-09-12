import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QScrollArea, QComboBox, QFrame
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ImageProcessorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set title and window size
        self.setWindowTitle('Image Processor')
        self.setGeometry(100, 100, 1200, 1000)  # Enlarged window size

        # Add scroll area to handle large content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        # Main widget for scrollable content
        main_widget = QWidget()
        scroll.setWidget(main_widget)

        # Main layout for the app
        main_layout = QVBoxLayout(main_widget)

        # Title label
        self.title_label = QLabel('Image Processing Application', self)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333333; padding: 10px;")
        self.title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_label)

        # Upload button for the image to process
        self.upload_button = QPushButton('Upload Image', self)
        self.upload_button.setFixedSize(120, 40)
        self.upload_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px;")
        self.upload_button.clicked.connect(self.upload_image)
        main_layout.addWidget(self.upload_button, alignment=Qt.AlignLeft)

        # Layout for the original image and histogram
        original_layout = QHBoxLayout()

        # Widget to hold the original image and histogram
        original_image_histogram_widget = QWidget()
        original_image_histogram_layout = QHBoxLayout(original_image_histogram_widget)

        # Label to display the original image
        self.image_label = QLabel('Original Image', self)
        self.image_label.setStyleSheet("border: 2px solid #cccccc; background-color: #ffffff;")
        self.image_label.setFixedWidth(400)
        self.image_label.setFixedHeight(400)
        original_image_histogram_layout.addWidget(self.image_label)

        # Canvas to show the original histogram
        self.canvas_original = FigureCanvas(Figure())
        self.canvas_original.setFixedWidth(600)
        self.canvas_original.setFixedHeight(400)
        original_image_histogram_layout.addWidget(self.canvas_original)

        original_layout.addWidget(original_image_histogram_widget)
        main_layout.addLayout(original_layout)

        # Layout for the equalized image and histogram
        equalized_layout = QHBoxLayout()

        # Widget to hold the equalized image and histogram
        equalized_image_histogram_widget = QWidget()
        equalized_image_histogram_layout = QHBoxLayout(equalized_image_histogram_widget)

        # Label to display the equalized image
        self.equalized_image_label = QLabel('Equalized Image', self)
        self.equalized_image_label.setStyleSheet("border: 2px solid #cccccc; background-color: #ffffff;")
        self.equalized_image_label.setFixedWidth(400)
        self.equalized_image_label.setFixedHeight(400)
        equalized_image_histogram_layout.addWidget(self.equalized_image_label)

        # Canvas to show the equalized histogram
        self.canvas_equalization = FigureCanvas(Figure())
        self.canvas_equalization.setFixedWidth(600)
        self.canvas_equalization.setFixedHeight(400)
        equalized_image_histogram_layout.addWidget(self.canvas_equalization)

        equalized_layout.addWidget(equalized_image_histogram_widget)
        main_layout.addLayout(equalized_layout)

        # Add a frame separator between the histogram and face detection sections
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setStyleSheet("color: #000000; padding: 10px;")
        main_layout.addWidget(self.separator)

        # Title for face detection section
        self.face_detection_label = QLabel('Face Detection & Blurring', self)
        self.face_detection_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333333; padding: 10px;")
        self.face_detection_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.face_detection_label)

        # Upload button for face detection image
        self.face_upload_button = QPushButton('Upload Face Image', self)
        self.face_upload_button.setFixedSize(150, 40)
        self.face_upload_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px;")
        self.face_upload_button.clicked.connect(self.upload_face_image)
        main_layout.addWidget(self.face_upload_button, alignment=Qt.AlignLeft)

        # Face detection image label
        self.face_image_label = QLabel('Face Detection Image', self)
        self.face_image_label.setStyleSheet("border: 2px solid #cccccc; background-color: #ffffff;")
        self.face_image_label.setFixedHeight(400)
        self.face_image_label.setFixedWidth(600)
        main_layout.addWidget(self.face_image_label)

        # Drop-down to select blur level
        self.blur_level = QComboBox(self)
        self.blur_level.addItems(["Dikit", "Sedang", "Banyak"])
        self.blur_level.setStyleSheet("padding: 5px; border: 2px solid #cccccc; border-radius: 5px; background-color: #ffffff;")
        main_layout.addWidget(self.blur_level, alignment=Qt.AlignLeft)

        # Apply blur button
        self.apply_blur_button = QPushButton('Apply Blur', self)
        self.apply_blur_button.setFixedSize(100, 40)
        self.apply_blur_button.setStyleSheet("background-color: #2196F3; color: white; border-radius: 5px;")
        self.apply_blur_button.clicked.connect(self.face_blurring)
        main_layout.addWidget(self.apply_blur_button, alignment=Qt.AlignLeft)

        # Set the scroll area as the central widget
        self.setCentralWidget(scroll)

    # Function to upload the image for histogram and equalization
    def upload_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp)", options=options)
        if file_name:
            self.display_image(file_name, self.image_label)
            self.process_image(file_name)

    # Function to display the image in the QLabel
    def display_image(self, file_name, label):
        pixmap = QPixmap(file_name)
        label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        label.setAlignment(Qt.AlignCenter)

    # Function to process and equalize the image, displaying histogram
    def process_image(self, file_name):
        image = cv2.imread(file_name)

        if image is None:
            print("Gambar tidak terbaca dengan benar!")
            return

        # Convert image to RGB for matplotlib
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Show the original histogram
        self.show_histogram(image_rgb, 'Histogram Original', self.canvas_original)

        # Equalization process
        image_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
        image_yuv[:, :, 0] = cv2.equalizeHist(image_yuv[:, :, 0])
        equalized_image = cv2.cvtColor(image_yuv, cv2.COLOR_YUV2BGR)

        # Display equalized image and histogram
        equalized_image_rgb = cv2.cvtColor(equalized_image, cv2.COLOR_BGR2RGB)
        self.show_histogram(equalized_image_rgb, 'Histogram Equalization', self.canvas_equalization)
        self.display_image_cv(equalized_image, self.equalized_image_label)

    # Show histogram for the image
    def show_histogram(self, image, title, canvas):
        canvas.figure.clear()
        ax = canvas.figure.add_subplot(111)
        color = ('r', 'g', 'b')
        for i, col in enumerate(color):
            hist = cv2.calcHist([image], [i], None, [256], [0, 256])
            ax.plot(hist, color=col)
        ax.set_xlim([0, 256])
        ax.set_title(title)
        canvas.draw()

    # Function to upload a different image for face detection
    def upload_face_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp)", options=options)
        if file_name:
            self.image_face = cv2.imread(file_name)
            self.detect_faces()

    # Detect faces automatically upon uploading an image
    def detect_faces(self):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(self.image_face, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(self.image_face, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Display face detection image
        self.display_image_cv(self.image_face, self.face_image_label)

    # Display image using OpenCV format
    def display_image_cv(self, image, label):
        q_image = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(q_image)
        label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        label.setAlignment(Qt.AlignCenter)



    # Function to apply face blurring based on user selection
    def face_blurring(self):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        image = self.image_face.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Set blur level based on user selection
        blur_level = self.blur_level.currentText()
        if blur_level == "Dikit":
            ksize = (21, 21)  # Small blur
        elif blur_level == "Sedang":
            ksize = (41, 41)  # Medium blur
        elif blur_level == "Banyak":
            ksize = (81, 81)  # Large blur

        # Ensure ksize is odd and greater than zero
        ksize = (ksize[0] | 1, ksize[1] | 1)

        for (x, y, w, h) in faces:
            face_region = image[y:y + h, x:x + w]
            if face_region.shape[0] > 0 and face_region.shape[1] > 0:
                blurred_face = cv2.GaussianBlur(face_region, ksize, 0)
                image[y:y + h, x:x + w] = blurred_face

        # Display the image with faces blurred
        self.display_image_cv(image, self.face_image_label)

# Start the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageProcessorApp()
    window.show()
    sys.exit(app.exec_())

