'''
        button1 = QPushButton('Carving')
        button1.setObjectName("homeButton")
        button1.setFont(QFont("Arial", 14, QFont.Bold))
        button1.clicked.connect(lambda _, button_id=1: self.home_button_clicked(button_id))
        buttons_layout.addWidget(button1)

        button2 = QPushButton('Hex Reader')
        button2.setObjectName("homeButton")
        buttimport sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel

class NavigationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Navigable Window")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.page_index = 0
        self.pages = []

        self.create_page1()
        self.create_page2()
        self.create_page3()

        self.show_page(self.page_index)

    def create_page1(self):
        page1_layout = QVBoxLayout()
        label = QLabel("Page 1")
        page1_layout.addWidget(label)

        button_next = QPushButton("Next")
        button_next.clicked.connect(self.next_page)
        page1_layout.addWidget(button_next)

        self.pages.append(page1_layout)

    def create_page2(self):
        page2_layout = QVBoxLayout()
        label = QLabel("Page 2")
        page2_layout.addWidget(label)

        button_prev = QPushButton("Previous")
        button_prev.clicked.connect(self.prev_page)
        page2_layout.addWidget(button_prev)

        button_next = QPushButton("Next")
        button_next.clicked.connect(self.next_page)
        page2_layout.addWidget(button_next)

        self.pages.append(page2_layout)

    def create_page3(self):
        page3_layout = QVBoxLayout()
        label = QLabel("Page 3")
        page3_layout.addWidget(label)

        button_prev = QPushButton("Previous")
        button_prev.clicked.connect(self.prev_page)
        page3_layout.addWidget(button_prev)

        self.pages.append(page3_layout)

    def show_page(self, index):
        self.layout = self.pages[index]
        self.central_widget.setLayout(self.layout)

    def next_page(self):
        if self.page_index < len(self.pages) - 1:
            self.page_index += 1
            self.show_page(self.page_index)

    def prev_page(self):
        if self.page_index > 0:
            self.page_index -= 1
            self.show_page(self.page_index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NavigationWindow()
    window.show()
    sys.exit(app.exec_())
on2.setFont(QFont("Arial", 14, QFont.Bold))
        button2.clicked.connect(lambda _, button_id=2: self.home_button_clicked(button_id))
        buttons_layout.addWidget(button2)

        #home_layout.addLayout(buttons_layout)

        button3 = QPushButton('File Explorer')
        button3.setObjectName("homeButton")
        button3.setFont(QFont("Arial", 14, QFont.Bold))
        button3.clicked.connect(lambda _, button_id=3: self.home_button_clicked(button_id))
        home_layout.addWidget(button3)

        button4 = QPushButton('Magic Cipher')
        button4.setObjectName("homeButton")
        button4.setFont(QFont("Arial", 14, QFont.Bold))
        button4.clicked.connect(lambda _, button_id=4: self.home_button_clicked(button_id))
        home_layout.addWidget(button4)

        #home_layout.addLayout(buttons_layout)

        button5 = QPushButton('Disk Analyser')
        button5.setObjectName("homeButton")
        button5.setFont(QFont("Arial", 14, QFont.Bold))
        button5.clicked.connect(lambda _, button_id=5: self.home_button_clicked(button_id))
        home_layout.addWidget(button5)

        button6 = QPushButton('Memory Forensics')
        button6.setObjectName("homeButton")
        button6.setFont(QFont("Arial", 14, QFont.Bold))
        button6.clicked.connect(lambda _, button_id=6: self.home_button_clicked(button_id))
        home_layout.addWidget(button6)

        button7 = QPushButton('Timeline Analysis')
        button7.setObjectName("homeButton")
        button7.setFont(QFont("Arial", 14, QFont.Bold))
        button7.clicked.connect(lambda _, button_id=7: self.home_button_clicked(button_id))
        home_layout.addWidget(button7)

        button8 = QPushButton('Malicious URL Detector')
        button8.setObjectName("homeButton")
        button8.setFont(QFont("Arial", 14, QFont.Bold))
        button8.clicked.connect(lambda _, button_id=8: self.home_button_clicked(button_id))
        home_layout.addWidget(button8)

        button9 = QPushButton('Malicious PE Header File Detector')
        button9.setObjectName("homeButton")
        button9.setFont(QFont("Arial", 14, QFont.Bold))
        button9.clicked.connect(lambda _, button_id=9: self.home_button_clicked(button_id))
        home_layout.addWidget(button9)
'''
        #home_layout.addLayout(buttons_layout)