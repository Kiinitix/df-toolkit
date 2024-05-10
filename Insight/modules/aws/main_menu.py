import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, QTextEdit, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import subprocess
import boto3
from botocore.exceptions import NoCredentialsError

class AWSCLIConfigApp(QMainWindow):
    def __init__(self, main_menu):
        super().__init__()

        self.setWindowTitle('AWS CLI Configuration')
        self.setGeometry(100, 100, 600, 400)
        self.main_menu = main_menu

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
            QTextEdit {
                font-size: 14px;
                padding: 8px;
                margin-top: 10px;
            }
        """)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout(main_widget)

        back_button = QPushButton("Back to Main Menu")
        back_button.clicked.connect(self.back_to_main_menu)
        layout.addWidget(back_button)

        layout.setAlignment(Qt.AlignCenter)

        label = QLabel('AWS CLI Configuration', self)
        label.setFont(QFont('Arial', 20))
        layout.addWidget(label)

        access_key_label = QLabel('Enter AWS Access Key ID:', self)
        layout.addWidget(access_key_label)

        self.access_key_input = QLineEdit(self)
        layout.addWidget(self.access_key_input)

        secret_key_label = QLabel('Enter AWS Secret Access Key:', self)
        layout.addWidget(secret_key_label)

        self.secret_key_input = QLineEdit(self)
        layout.addWidget(self.secret_key_input)

        region_label = QLabel('Enter AWS Default Region:', self)
        layout.addWidget(region_label)

        self.region_input = QLineEdit(self)
        layout.addWidget(self.region_input)

        save_button = QPushButton('Save Configuration', self)
        save_button.clicked.connect(self.save_configuration)
        layout.addWidget(save_button)

        check_button = QPushButton('Check Existing Configuration', self)
        check_button.clicked.connect(self.check_configuration)
        layout.addWidget(check_button)

        output_label = QLabel('Existing Configuration:', self)
        layout.addWidget(output_label)

        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)
        layout.addWidget(self.output_area)

    def back_to_main_menu(self):
        self.main_menu.show()
        self.close()

    def save_configuration(self):
        access_key = self.access_key_input.text()
        secret_key = self.secret_key_input.text()
        region = self.region_input.text()

        if not access_key or not secret_key or not region:
            QMessageBox.warning(self, 'Warning', 'Please enter all required fields.')
            return

        try:
            subprocess.run(['aws', 'configure', 'set', 'aws_access_key_id', access_key])
            subprocess.run(['aws', 'configure', 'set', 'aws_secret_access_key', secret_key])
            subprocess.run(['aws', 'configure', 'set', 'region', region])

            QMessageBox.information(self, 'Success', 'AWS CLI configured successfully.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error configuring AWS CLI: {str(e)}')

    def check_configuration(self):
        try:
            result = subprocess.run(['aws', 'configure', 'list'], capture_output=True, text=True)
            existing_config = result.stdout.strip()

            if existing_config:
                self.output_area.setPlainText(existing_config)
            else:
                self.output_area.setPlainText('No existing AWS CLI configuration found.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error checking AWS CLI configuration: {str(e)}')

class S3FileDownloadApp(QMainWindow):
    def __init__(self, main_menu):
        super().__init__()

        self.setWindowTitle('AWS S3 File Download')
        self.setGeometry(100, 100, 800, 600)
        self.main_menu = main_menu

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

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout(main_widget)

        back_button = QPushButton("Back to Main Menu")
        back_button.clicked.connect(self.back_to_main_menu)
        layout.addWidget(back_button)

        layout.setAlignment(Qt.AlignCenter)

        label = QLabel('AWS S3 File Download', self)
        label.setFont(QFont('Arial', 20))
        layout.addWidget(label)

        bucket_label = QLabel('Enter S3 Bucket Name:', self)
        layout.addWidget(bucket_label)

        self.bucket_input = QLineEdit(self)
        layout.addWidget(self.bucket_input)

        key_label = QLabel('Enter S3 Object Key (File Path):', self)
        layout.addWidget(key_label)

        self.key_input = QLineEdit(self)
        layout.addWidget(self.key_input)

        download_button = QPushButton('Download File', self)
        download_button.clicked.connect(self.download_file)
        layout.addWidget(download_button)


    def back_to_main_menu(self):
        self.main_menu.show()
        self.close()

    def download_file(self):
        bucket_name = self.bucket_input.text()
        object_key = self.key_input.text()

        if not bucket_name or not object_key:
            return

        save_path, _ = QFileDialog.getSaveFileName(self, 'Save File As', '', 'All Files (*);;Text Files (*.txt)')

        if not save_path:
            return

        try:
            s3 = boto3.client('s3')

            s3.download_file(bucket_name, object_key, save_path)

            print(f"File downloaded successfully to: {save_path}")
        except NoCredentialsError:
            print("Credentials not available. Please configure AWS credentials.")
        except Exception as e:
            print(f"Error: {str(e)}")

class S3FileUploadApp(QMainWindow):
    def __init__(self, main_menu):
        super().__init__()

        self.setWindowTitle('AWS S3 File Upload')
        self.setGeometry(100, 100, 800, 600)
        self.main_menu = main_menu

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

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout(main_widget)

        back_button = QPushButton("Back to Main Menu")
        back_button.clicked.connect(self.back_to_main_menu)
        layout.addWidget(back_button)

        layout.setAlignment(Qt.AlignCenter)

        label = QLabel('AWS S3 File Upload', self)
        label.setFont(QFont('Arial', 20))
        layout.addWidget(label)

        bucket_label = QLabel('Enter S3 Bucket Name:', self)
        layout.addWidget(bucket_label)

        self.bucket_input = QLineEdit(self)
        layout.addWidget(self.bucket_input)

        key_label = QLabel('Enter S3 Object Key (File Path):', self)
        layout.addWidget(key_label)

        self.key_input = QLineEdit(self)
        layout.addWidget(self.key_input)

        file_button = QPushButton('Select File for Upload', self)
        file_button.clicked.connect(self.upload_file)
        layout.addWidget(file_button)

    def back_to_main_menu(self):
        self.main_menu.show()
        self.close()

    def upload_file(self):
        bucket_name = self.bucket_input.text()
        object_key = self.key_input.text()

        if not bucket_name or not object_key:
            return

        file_path, _ = QFileDialog.getOpenFileName(self, 'Select File for Upload', '', 'All Files (*);;Text Files (*.txt)')

        if not file_path:
            return

        try:
            s3 = boto3.client('s3')
            s3.upload_file(file_path, bucket_name, object_key)

            print(f"File uploaded successfully to S3: s3://{bucket_name}/{object_key}")
        except NoCredentialsError:
            print("Credentials not available. Please configure AWS credentials.")
        except Exception as e:
            print(f"Error: {str(e)}")

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        button1 = QPushButton("Configure AWS")
        button1.clicked.connect(self.open_window1)
        layout.addWidget(button1)

        button2 = QPushButton("Upload File")
        button2.clicked.connect(self.open_window2)
        layout.addWidget(button2)

        button3 = QPushButton("Download File")
        button3.clicked.connect(self.open_window3)
        layout.addWidget(button3)

        button4 = QPushButton("Exit")
        button4.clicked.connect(self.exit)
        layout.addWidget(button4)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def exit(self):
        sys.exit()

    def open_window1(self):
        
        self.window1 = AWSCLIConfigApp(self)
        self.window1.show()
        self.hide()

    def open_window2(self):
        self.window2 = S3FileUploadApp(self)
        self.window2.show()
        self.hide()

    def open_window3(self):
        self.window3 = S3FileDownloadApp(self)
        self.window3.show()
        self.hide()

class Window1(QMainWindow):
    def __init__(self, main_menu):
        super().__init__()
        self.setWindowTitle("Window 1")
        self.setGeometry(100, 100, 400, 300)
        self.main_menu = main_menu

        layout = QVBoxLayout()
        back_button = QPushButton("Back to Main Menu")
        back_button.clicked.connect(self.back_to_main_menu)
        layout.addWidget(back_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def back_to_main_menu(self):
        self.main_menu.show()
        self.close()

class Window2(QMainWindow):
    def __init__(self, main_menu):
        super().__init__()
        self.setWindowTitle("Window 2")
        self.setGeometry(100, 100, 400, 300)
        self.main_menu = main_menu

        layout = QVBoxLayout()
        back_button = QPushButton("Back to Main Menu")
        back_button.clicked.connect(self.back_to_main_menu)
        layout.addWidget(back_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def back_to_main_menu(self):
        self.main_menu.show()
        self.close()

class Window3(QMainWindow):
    def __init__(self, main_menu):
        super().__init__()
        self.setWindowTitle("Window 3")
        self.setGeometry(100, 100, 400, 300)
        self.main_menu = main_menu

        layout = QVBoxLayout()
        back_button = QPushButton("Back to Main Menu")
        back_button.clicked.connect(self.back_to_main_menu)
        layout.addWidget(back_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def back_to_main_menu(self):
        self.main_menu.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec_())