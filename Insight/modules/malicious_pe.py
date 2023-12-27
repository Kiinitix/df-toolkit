import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
import joblib 
import pefile 

class MaliciousPEDetectorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Malicious PE Header Detector')
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout(main_widget)
        layout.setAlignment(Qt.AlignTop)

        back_button = QPushButton('Back', self)
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)

        input_label = QLabel('Enter PE File Path:', self)
        layout.addWidget(input_label)

        self.file_path_input = QLineEdit(self)
        layout.addWidget(self.file_path_input)

        detect_button = QPushButton('Detect Malicious PE Header', self)
        detect_button.clicked.connect(self.detect_pe_header)
        layout.addWidget(detect_button)

        self.output_label = QLabel('Detection Result: ', self)
        layout.addWidget(self.output_label)
        self.ml_model = None  # Load your model here using joblib.load()

    def go_back(self):
        sys.exit()

    def detect_pe_header(self):
        file_path = self.file_path_input.text()

        if not file_path:
            QMessageBox.warning(self, 'Warning', 'Please enter a file path.')
            return

        try:
            if self.ml_model:
                pe = pefile.PE(file_path)

                prediction = self.ml_model.predict([pe])[0]

                if prediction == 1: 
                    result_text = 'Malicious PE Header'
                else:
                    result_text = 'Not Malicious PE Header'

                self.output_label.setText(f'Detection Result: {result_text}')
            else:
                QMessageBox.warning(self, 'Warning', 'Machine learning model not loaded.')
        except Exception as e:
            QMessageBox.warning(self, 'Warning', f'Error analyzing PE header: {str(e)}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MaliciousPEDetectorApp()
    main_app.show()
    sys.exit(app.exec_())
