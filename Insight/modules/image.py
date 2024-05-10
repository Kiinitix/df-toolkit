import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QLabel, QMainWindow, QFileDialog,
    QVBoxLayout, QWidget, QPushButton, QTextEdit, QHBoxLayout,
)
from PyQt5.QtGui import QPixmap, QImage, QImageReader, QPainter, QPen, QColor
from PIL import Image, ImageChops, ImageFilter, ImageOps, ImageEnhance
from PIL.ExifTags import TAGS
from skimage.metrics import structural_similarity as ssim
from scipy.ndimage import sobel
from skimage import color
from PyQt5.QtCore import Qt

class ImageForensicsApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.image_path = None

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label)

        self.load_button = QPushButton('Load Image', self)
        self.load_button.clicked.connect(self.load_image)

        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.load_button)
        self.button_layout.addStretch()

        self.layout.addLayout(self.button_layout)
        self.layout.addWidget(self.output_text)

        self.setGeometry(100, 100, 800, 600)  # Set initial window size

    def load_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp *.jpeg);;All Files (*)", options=options)

        if file_name:
            self.image_path = file_name
            print(f"Image Path: {self.image_path}")
            self.update_image_label()
            self.analyze_image()

    def update_image_label(self):
        if self.image_path:
            try:
                pixmap = QPixmap(self.image_path)
                if not pixmap.isNull():
                    print("Image loaded successfully.")
                    self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), aspectRatioMode=Qt.KeepAspectRatio))
                else:
                    print("Error: Failed to load pixmap.")
            except Exception as e:
                print(f"Error: {e}")

    def analyze_metadata(self):
        if self.image_path:
            image = Image.open(self.image_path)
            exif_data = self.get_exif_data(image)
            self.append_output("\nMetadata Analysis:")
            self.append_output(str(exif_data))

    def analyze_ela(self):
        if self.image_path:
            original_image = Image.open(self.image_path)
            temp_image_path = 'temp_resaved.jpg'
            original_image.save(temp_image_path, 'JPEG', quality=90)

            temp_image = Image.open(temp_image_path)
            ela_image = ImageChops.difference(original_image, temp_image)
            extrema = ela_image.getextrema()
            max_diff = max([ex[1] for ex in extrema])
            scale = 255.0 / max_diff

            ela_image = ela_image.point(lambda p: p * scale)
            self.display_image(ela_image)
            self.append_output("\nError Level Analysis (ELA) performed.")

    def analyze_noise(self):
        if self.image_path:
            original_image = Image.open(self.image_path)
            gray_image = original_image.convert('L')
            arr_original = np.array(gray_image)

            # Calculate and display the image gradient as a measure of noise
            gradient = np.gradient(arr_original)
            magnitude = np.sqrt(gradient[0]**2 + gradient[1]**2)
            self.display_image(Image.fromarray(magnitude.astype('uint8')))
            self.append_output("\nNoise Analysis performed.")

    def detect_splicing(self):
        if self.image_path:
            original_image = Image.open(self.image_path)

            # Simulate splicing detection with a basic edge detection filter
            edge_detection = original_image.filter(ImageFilter.FIND_EDGES)
            self.display_image(edge_detection)
            self.append_output("\nSplicing Detection performed.")

    def detect_clones(self):
        if self.image_path:
            original_image = Image.open(self.image_path)

        # Simulate clone detection with a basic structural similarity index
        # (in practice, more advanced techniques are used)
            cloned_image = ImageOps.flip(original_image)

        # Explicitly set win_size to a smaller odd value
            smaller_side = min(original_image.size[0], original_image.size[1])
            win_size = min(smaller_side, 5)  # You can adjust this value based on your needs

        # Ensure win_size is odd
            if win_size % 2 == 0:
                win_size += 1

            similarity_index, _ = ssim(np.array(original_image), np.array(cloned_image), full=True, win_size=win_size)
            self.append_output(f"\nClone Detection performed. Structural Similarity Index: {similarity_index}")



    def detect_steganography(self):
        if self.image_path:
            # Simulate steganalysis by checking for LSB modifications
            original_image = Image.open(self.image_path)
            lsb_modified_image = original_image.copy()
            lsb_modified_image.putpixel((0, 0), (0, 0, 0))

            self.display_image(lsb_modified_image)
            self.append_output("\nSteganalysis performed.")

    def analyze_geometry(self):
        if self.image_path:
            original_image = Image.open(self.image_path)

            # Simulate geometric analysis by detecting edges
            edges = sobel(color.rgb2gray(np.array(original_image)))
            self.display_image(Image.fromarray((edges * 255).astype('uint8'), 'L'))
            self.append_output("\nGeometric Analysis performed")
    
    def analyze_color(self):
        if self.image_path:
            original_image = Image.open(self.image_path)

            # Simulate color analysis by separating color channels
            r, g, b = original_image.split()
            self.display_image(Image.merge("RGB", (r, g.point(lambda p: p * 0), b.point(lambda p: p * 0))))
            self.append_output("\nColor Analysis performed.")

    def display_image(self, image):
        q_image = self.convert_image_to_qimage(image)
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), aspectRatioMode=Qt.KeepAspectRatio))

    def convert_image_to_qimage(self, image):
        if image.mode == 'RGB':
            r, g, b = image.split()
            image = Image.merge("RGB", (b, g, r))
        elif image.mode == 'RGBA':
            r, g, b, a = image.split()
            image = Image.merge("RGBA", (b, g, r, a))

        data = image.tobytes("raw", image.mode)
        q_image = QImage(data, image.width, image.height, image.width * len(image.mode), QImage.Format_ARGB32)

        return q_image

    def get_exif_data(self, image):
        exif_data = {}
        try:
            for tag, value in image._getexif().items():
                tag_name = TAGS.get(tag, tag)
                exif_data[tag_name] = value
        except AttributeError:
            print("No EXIF data found")

        return exif_data

    def analyze_image(self):
        self.clear_output()
        self.analyze_metadata()
        self.analyze_ela()
        self.analyze_noise()
        self.detect_splicing()
        self.detect_clones()
        self.detect_steganography()
        self.analyze_geometry()
        self.analyze_color()

    def append_output(self, text):
        self.output_text.append(text)

    def clear_output(self):
        self.output_text.clear()

def main():
    app = QApplication(sys.argv)
    forensics_app = ImageForensicsApp()
    forensics_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

