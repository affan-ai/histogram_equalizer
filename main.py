import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy, QScrollArea
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ImageProcessorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Image Processor')
        self.setGeometry(100, 100, 1000, 800)  # Ukuran jendela awal

        # Tambahkan QScrollArea
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        # Widget utama untuk scroll area
        main_widget = QWidget()
        scroll.setWidget(main_widget)

        # Layout utama
        main_layout = QVBoxLayout(main_widget)

        # Judul
        self.title_label = QLabel('Image Processing Application', self)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333333; padding: 10px;")
        self.title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_label)

        # Tombol Upload
        self.upload_button = QPushButton('Upload Image', self)
        self.upload_button.setFixedSize(120, 40)
        self.upload_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px;")
        self.upload_button.clicked.connect(self.upload_image)
        main_layout.addWidget(self.upload_button, alignment=Qt.AlignLeft)

        # Layout untuk gambar yang di-upload dan histogram original
        top_layout = QHBoxLayout()

        # Widget untuk menampilkan gambar yang di-upload dan histogram
        image_histogram_widget = QWidget()
        image_histogram_layout = QHBoxLayout(image_histogram_widget)

        # Label untuk menampilkan gambar yang di-upload
        self.image_label = QLabel('Uploaded Image', self)
        self.image_label.setStyleSheet("border: 2px solid #cccccc; background-color: #ffffff;")
        image_histogram_layout.addWidget(self.image_label)

        # Canvas untuk histogram original
        self.canvas_original = FigureCanvas(Figure())
        image_histogram_layout.addWidget(self.canvas_original)

        top_layout.addWidget(image_histogram_widget)

        main_layout.addLayout(top_layout)

        # Spacer untuk memberikan jarak antara gambar lama dan gambar baru
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer)

        # Layout untuk gambar yang di-equalized dan histogram equalization
        bottom_layout = QHBoxLayout()

        # Widget untuk menampilkan gambar hasil equalization dan histogram
        equalized_histogram_widget = QWidget()
        equalized_histogram_layout = QHBoxLayout(equalized_histogram_widget)

        # Label untuk menampilkan gambar hasil equalization
        self.equalized_image_label = QLabel('Equalized Image', self)
        self.equalized_image_label.setStyleSheet("border: 2px solid #cccccc; background-color: #ffffff;")
        equalized_histogram_layout.addWidget(self.equalized_image_label)

        # Canvas untuk histogram equalization
        self.canvas_equalization = FigureCanvas(Figure())
        equalized_histogram_layout.addWidget(self.canvas_equalization)

        bottom_layout.addWidget(equalized_histogram_widget)

        main_layout.addLayout(bottom_layout)

        # Set scroll area sebagai central widget
        self.setCentralWidget(scroll)

    def upload_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp)", options=options)
        if file_name:
            self.display_image(file_name)
            self.process_image(file_name)

    def display_image(self, file_name):
        pixmap = QPixmap(file_name)
        # Menggunakan Qt.KeepAspectRatio agar gambar tidak terpotong dan menyesuaikan dengan frame
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.image_label.setAlignment(Qt.AlignCenter)

    def process_image(self, file_name):
        # Baca gambar
        image = cv2.imread(file_name)
        
        if image is None:
            print("Gambar tidak terbaca dengan benar!")
            return

        # Convert gambar ke RGB untuk menampilkan dengan Matplotlib
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Tampilkan histogram original
        self.show_histogram(image_rgb, 'Histogram Original', self.canvas_original)

        # Equalization
        image_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
        image_yuv[:, :, 0] = cv2.equalizeHist(image_yuv[:, :, 0])
        equalized_image = cv2.cvtColor(image_yuv, cv2.COLOR_YUV2BGR)

        # Tampilkan histogram equalization
        equalized_image_rgb = cv2.cvtColor(equalized_image, cv2.COLOR_BGR2RGB)
        self.show_histogram(equalized_image_rgb, 'Histogram Equalization', self.canvas_equalization)

        # Tampilkan gambar hasil equalization
        self.display_equalized_image(equalized_image)

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

    def display_equalized_image(self, equalized_image):
        q_image = QImage(equalized_image.data, equalized_image.shape[1], equalized_image.shape[0], equalized_image.strides[0], QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(q_image)
        # Menggunakan Qt.KeepAspectRatio agar gambar tidak terpotong dan menyesuaikan dengan frame
        self.equalized_image_label.setPixmap(pixmap.scaled(self.equalized_image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.equalized_image_label.setAlignment(Qt.AlignCenter)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageProcessorApp()
    ex.show()
    sys.exit(app.exec_())
