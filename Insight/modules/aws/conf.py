import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, QTextEdit, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import subprocess


class AWSCLIConfigApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('AWS CLI Configuration')
        self.setGeometry(100, 100, 600, 400)

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
            QTextEdit {
                font-size: 14px;
                padding: 8px;
                margin-top: 10px;
            }
        """)

        # Create the main widget and set it as the central widget
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Create layout
        layout = QVBoxLayout(main_widget)
        layout.setAlignment(Qt.AlignCenter)

        # Create widgets
        label = QLabel('AWS CLI Configuration', self)
        label.setFont(QFont('Arial', 20))
        layout.addWidget(label)

        # AWS Access Key ID input
        access_key_label = QLabel('Enter AWS Access Key ID:', self)
        layout.addWidget(access_key_label)

        self.access_key_input = QLineEdit(self)
        layout.addWidget(self.access_key_input)

        # AWS Secret Access Key input
        secret_key_label = QLabel('Enter AWS Secret Access Key:', self)
        layout.addWidget(secret_key_label)

        self.secret_key_input = QLineEdit(self)
        layout.addWidget(self.secret_key_input)

        # AWS Default Region input
        region_label = QLabel('Enter AWS Default Region:', self)
        layout.addWidget(region_label)

        self.region_input = QLineEdit(self)
        layout.addWidget(self.region_input)

        # Save Configuration button
        save_button = QPushButton('Save Configuration', self)
        save_button.clicked.connect(self.save_configuration)
        layout.addWidget(save_button)

        # Check Existing Configuration button
        check_button = QPushButton('Check Existing Configuration', self)
        check_button.clicked.connect(self.check_configuration)
        layout.addWidget(check_button)

        # Output area for displaying existing configuration
        output_label = QLabel('Existing Configuration:', self)
        layout.addWidget(output_label)

        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)
        layout.addWidget(self.output_area)

    def save_configuration(self):
        access_key = self.access_key_input.text()
        secret_key = self.secret_key_input.text()
        region = self.region_input.text()

        if not access_key or not secret_key or not region:
            QMessageBox.warning(self, 'Warning', 'Please enter all required fields.')
            return

        try:
            # Run AWS CLI commands to configure
            subprocess.run(['aws', 'configure', 'set', 'aws_access_key_id', access_key])
            subprocess.run(['aws', 'configure', 'set', 'aws_secret_access_key', secret_key])
            subprocess.run(['aws', 'configure', 'set', 'region', region])

            QMessageBox.information(self, 'Success', 'AWS CLI configured successfully.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error configuring AWS CLI: {str(e)}')

    def check_configuration(self):
        try:
            # Run AWS CLI command to get the current configuration
            result = subprocess.run(['aws', 'configure', 'list'], capture_output=True, text=True)
            existing_config = result.stdout.strip()

            if existing_config:
                self.output_area.setPlainText(existing_config)
            else:
                self.output_area.setPlainText('No existing AWS CLI configuration found.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error checking AWS CLI configuration: {str(e)}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = AWSCLIConfigApp()
    main_app.show()
    sys.exit(app.exec_())
