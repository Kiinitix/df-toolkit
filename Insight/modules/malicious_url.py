import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, QMessageBox
import joblib  
import pickle

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

    def sanitization(self, web):
        web = web.lower()
        token = []
        dot_token_slash = []
        raw_slash = str(web).split('/')
        for i in raw_slash:
            raw1 = str(i).split('-')
            slash_token = []
            for j in range(0,len(raw1)):
                raw2 = str(raw1[j]).split('.')
                slash_token = slash_token + raw2
            dot_token_slash = dot_token_slash + raw1 + slash_token
        token = list(set(dot_token_slash)) 
        if 'com' in token:
            token.remove('com')
        return token

    def detect_url(self):
        urls = []
        url = self.url_input.text()

        urls.append(url)

        whitelist = ['hackthebox.eu','root-me.org','gmail.com']
        s_url = [i for i in urls if i not in whitelist]

        file = "Classifier/pickel_model.pkl"
        with open(file, 'rb') as f1:  
            lgr = pickle.load(f1)
        f1.close()
        
        file = "Classifier/pickel_vector.pkl"
        with open(file, 'rb') as f2:  
            vectorizer = pickle.load(f2)
        f2.close()

        x = vectorizer.transform(s_url)
        y_predict = lgr.predict(x)

        for site in whitelist:
            s_url.append(site)

        predict = list(y_predict)
        for j in range(0,len(whitelist)):
            predict.append('good')

        if not url:
            QMessageBox.warning(self, 'Warning', 'Please enter a URL.')
            return

        if self.ml_model:
            result_text = predict[0]
            self.output_label.setText(f'Detection Result: {result_text}')
        else:
            QMessageBox.warning(self, 'Warning', 'Machine learning model not loaded.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MaliciousURLDetectorApp()
    main_app.show()
    sys.exit(app.exec_())
