import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, QFileDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import boto3
from botocore.exceptions import NoCredentialsError


class S3FileUploadApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('AWS S3 File Upload')
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
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # Create the main widget and set it as the central widget
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Create layout
        layout = QVBoxLayout(main_widget)
        layout.setAlignment(Qt.AlignCenter)

        # Create widgets
        label = QLabel('AWS S3 File Upload', self)
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

        # File selection button
        file_button = QPushButton('Select File for Upload', self)
        file_button.clicked.connect(self.upload_file)
        layout.addWidget(file_button)

    def upload_file(self):
        bucket_name = self.bucket_input.text()
        object_key = self.key_input.text()

        if not bucket_name or not object_key:
            return

        file_path, _ = QFileDialog.getOpenFileName(self, 'Select File for Upload', '', 'All Files (*);;Text Files (*.txt)')

        if not file_path:
            return

        try:
            # Initialize an S3 client
            s3 = boto3.client('s3')

            # Upload the file to S3
            s3.upload_file(file_path, bucket_name, object_key)

            print(f"File uploaded successfully to S3: s3://{bucket_name}/{object_key}")
        except NoCredentialsError:
            print("Credentials not available. Please configure AWS credentials.")
        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = S3FileUploadApp()
    main_app.show()
    sys.exit(app.exec_())
