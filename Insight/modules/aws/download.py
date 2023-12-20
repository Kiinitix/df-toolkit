import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, QFileDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import boto3
from botocore.exceptions import NoCredentialsError


class S3FileDownloadApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('AWS S3 File Download')
        self.setGeometry(100, 100, 800, 600)

        # Set application-wide style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 16px;
                margin-bottom: 10px;
            }
            QLineEdit {
                font-size: 14px;
                padding: 8px;
                margin-bottom: 20px;
            }
            QPushButton {
                font-size: 16px;
                padding: 10px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        # Create the main widget and set it as the central widget
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Create layout
        layout = QVBoxLayout(main_widget)
        layout.setAlignment(Qt.AlignCenter)

        # Create widgets
        label = QLabel('AWS S3 File Download', self)
        label.setFont(QFont('Arial', 20))
        layout.addWidget(label)

        # S3 Bucket and Key input
        bucket_label = QLabel('Enter S3 Bucket Name:', self)
        layout.addWidget(bucket_label)

        self.bucket_input = QLineEdit(self)
        layout.addWidget(self.bucket_input)

        key_label = QLabel('Enter S3 Object Key (File Path):', self)
        layout.addWidget(key_label)

        self.key_input = QLineEdit(self)
        layout.addWidget(self.key_input)

        # Download button
        download_button = QPushButton('Download File', self)
        download_button.clicked.connect(self.download_file)
        layout.addWidget(download_button)

    def download_file(self):
        bucket_name = self.bucket_input.text()
        object_key = self.key_input.text()

        if not bucket_name or not object_key:
            return

        save_path, _ = QFileDialog.getSaveFileName(self, 'Save File As', '', 'All Files (*);;Text Files (*.txt)')

        if not save_path:
            return

        try:
            # Initialize an S3 client
            s3 = boto3.client('s3')

            # Download the file from S3 and save it locally
            s3.download_file(bucket_name, object_key, save_path)

            print(f"File downloaded successfully to: {save_path}")
        except NoCredentialsError:
            print("Credentials not available. Please configure AWS credentials.")
        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = S3FileDownloadApp()
    main_app.show()
    sys.exit(app.exec_())
