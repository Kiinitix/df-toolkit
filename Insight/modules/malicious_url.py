import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, QMessageBox
import joblib  

class MaliciousURLDetectorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Malicious URL Detector')
        self.setGeometry(100, 100, 600, 400)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout(main_widget)
        #layout.setAlignment(Qt.AlignTop)

        back_button = QPushButton('Back', self)
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)

        input_label = QLabel('Enter URL:', self)
        layout.addWidget(input_label)

        self.url_input = QLineEdit(self)
        layout.addWidget(self.url_input)

        detect_button = QPushButton('Detect Malicious URL', self)
        detect_button.clicked.connect(self.detect_url)
        layout.addWidget(detect_button)

        self.output_label = QLabel('Detection Result: ', self)
        layout.addWidget(self.output_label)

        self.ml_model = None  # Load your model here using joblib.load()

    def go_back(self):
        sys.exit()

    def detect_url(self):
        url = self.url_input.text()

        if not url:
            QMessageBox.warning(self, 'Warning', 'Please enter a URL.')
            return

        if self.ml_model:
            prediction = self.ml_model.predict([url])[0]

            if prediction == 1:
                result_text = 'Malicious URL'
            else:
                result_text = 'Not Malicious URL'

            self.output_label.setText(f'Detection Result: {result_text}')
        else:
            QMessageBox.warning(self, 'Warning', 'Machine learning model not loaded.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MaliciousURLDetectorApp()
    main_app.show()
    sys.exit(app.exec_())
