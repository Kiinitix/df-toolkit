import sys
from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtGui import QColor, QFont
from PySide2.QtWidgets import *

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QScrollArea, QStackedWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import random
import subprocess
import importlib

from ui_splash_screen import Ui_SplashScreen
from cli_menu import update

counter = 0

class Dashboard(QWidget):
    def __init__(self, modules):
        super().__init__()

        self.modules = modules
        self.initUI()

    def initUI(self):
        update()
        main_layout = QHBoxLayout()

        left_panel = QVBoxLayout()
        left_panel.setAlignment(Qt.AlignTop)
        tabs = ["Home", "Download", "Info", "Exit"]
        self.tab_buttons = []

        for tab in tabs:
            button = QPushButton(tab)
            button.setObjectName("tabButton")
            button.clicked.connect(lambda _, tab=tab: self.switch_tab(tab))
            left_panel.addWidget(button)
            self.tab_buttons.append(button)

        dashboard_content = QStackedWidget()
        home_tab = QWidget()
        
        home_layout = QVBoxLayout()

        buttons_layout = QHBoxLayout()

        button0 = QPushButton('Manage Modules')
        button0.setObjectName("homeButton")
        button0.setFont(QFont("Arial", 14, QFont.Bold))
        button0.clicked.connect(lambda _, button_id=0: self.home_button_clicked(button_id))
        home_layout.addWidget(button0)
        
        button1 = QPushButton('Carving')
        button1.setObjectName("homeButton")
        button1.setFont(QFont("Arial", 14, QFont.Bold))
        button1.clicked.connect(lambda _, button_id=1: self.home_button_clicked(button_id))
        buttons_layout.addWidget(button1)

        button2 = QPushButton('Hex Reader')
        button2.setObjectName("homeButton")
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
        for module in self.modules:
            button = QPushButton(module)
            button.setFont(QFont("Arial", 14, QFont.Bold))
            func = self.createFunction(module)
            button.clicked.connect(func)
            home_layout.addWidget(button)
        '''
        home_scroll_area = QScrollArea()
        home_scroll_area.setWidgetResizable(True)
        home_scroll_area.setWidget(QWidget())
        home_scroll_area.widget().setLayout(home_layout)

        dashboard_content.addWidget(home_scroll_area)

        download_tab = QWidget()
        download_layout = QVBoxLayout()

        conf = QPushButton('AWS')
        conf.setObjectName("downloadButton")
        conf.setFont(QFont("Arial", 14, QFont.Bold))
        conf.clicked.connect(lambda _, button_id=11: self.download_button_clicked(button_id))
        download_layout.addWidget(conf)

        download = QPushButton('Azure')
        download.setObjectName("downloadButton")
        download.setFont(QFont("Arial", 14, QFont.Bold))
        download.clicked.connect(lambda _, button_id=12: self.download_button_clicked(button_id))
        download_layout.addWidget(download)

        upload = QPushButton('OCI')
        upload.setObjectName("downloadButton")
        upload.setFont(QFont("Arial", 14, QFont.Bold))
        upload.clicked.connect(lambda _, button_id=13: self.download_button_clicked(button_id))
        download_layout.addWidget(upload)

        download_tab.setLayout(download_layout)
        dashboard_content.addWidget(download_tab)

        info_tab = QWidget()
        info_layout = QVBoxLayout()
        for _ in range(5):
            label = QLabel(random.choice(self.get_random_sentences()))
            label.setObjectName("infoLabel")
            info_layout.addWidget(label)
        info_tab.setLayout(info_layout)
        dashboard_content.addWidget(info_tab)

        main_layout.addLayout(left_panel)
        main_layout.addWidget(dashboard_content)

        self.setLayout(main_layout)

        self.setWindowTitle('Insight')
        self.setGeometry(100, 100, 800, 500)

        self.setStyleSheet("""
            #tabButton {
                background-color: #2c3e50;
                color: white;
                font-size: 14px;
                padding: 10px;
                border: none;
                border-radius: 5px;
                margin-bottom: 5px;
            }

            #homeButton, #downloadButton {
                background-color: #3498db;
                color: white;
                font-size: 16px;
                padding: 15px;
                border: none;
                border-radius: 10px;
                margin-bottom: 10px;
            }

            #infoLabel {
                font-size: 14px;
                margin-bottom: 5px;
            }
        """)

    def switch_tab(self, tab_name):
        index = ["Home", "Download", "Info", "Exit"].index(tab_name)
        self.tab_buttons[index].setChecked(True)
        self.findChild(QStackedWidget).setCurrentIndex(index)

    def home_button_clicked(self, button_id):
        if(button_id == 0):
            subprocess.Popen(["python3", "cli_menu.py"])
        if(button_id == 1):
            subprocess.Popen(["python3", "modules/carving.py"])
        if(button_id == 2):
            subprocess.Popen(["python", "modules/hex_main.py"])
        if(button_id == 3):
            subprocess.Popen(["python", "modules/file_explorer.py"])
        if(button_id == 4):
            subprocess.Popen(["python", "modules/magic_cipher.py"])
        if(button_id == 5):
            subprocess.Popen(["python", "modules/disk_analyzer.py"])
        if(button_id == 6):
            subprocess.Popen(["python", "modules/memory_forensics.py"])
        if(button_id == 7):
            subprocess.Popen(["python", "modules/timeline_analysis.py"])
        if(button_id == 8):
            subprocess.Popen(["python", "modules/malicious_url.py"])
        if(button_id == 9):
            subprocess.Popen(["python", "modules/malicious_pe.py"])


    def download_button_clicked(self, button_id):
        if(button_id == 11):
            subprocess.Popen(["python", "modules/aws/conf.py"])
        if(button_id == 12):
            subprocess.Popen(["python", "modules/aws/download.py"])
        if(button_id == 13):
            subprocess.Popen(["python", "modules/aws/upload.py"])

    def get_random_sentences(self):
        sentences = [
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
            "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
            "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        ]
        return sentences

    def createFunction(self, module):
        def buttonClicked():
            mod = importlib.import_module(module)
            print(f"{module} function triggered")
        return buttonClicked

class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(35)
        self.ui.label_description.setText("Digital Forensics Toolkit")
        QtCore.QTimer.singleShot(3000, lambda: self.ui.label_description.setText("<strong>LOADING</strong> USER INTERFACE"))
        self.show()

    def progress(self):
        available_modules_file = "available_modules.txt"
        with open(available_modules_file, 'r') as file:
            available_modules = [line.strip() for line in file.readlines()]

        global counter
        self.ui.progressBar.setValue(counter)
        if counter > 100:
            self.timer.stop()
            self.main = Dashboard(available_modules)
            self.main.show()
            self.close()
        counter += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec_())
