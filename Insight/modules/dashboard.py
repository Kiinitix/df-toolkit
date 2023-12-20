import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QScrollArea, QStackedWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import random
import subprocess


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()

        left_panel = QVBoxLayout()
        left_panel.setAlignment(Qt.AlignTop)
        tabs = ["Home", "Download", "Info"]
        self.tab_buttons = []

        for tab in tabs:
            button = QPushButton(tab)
            button.setObjectName("tabButton")
            button.clicked.connect(lambda _, tab=tab: self.switch_tab(tab))
            left_panel.addWidget(button)
            self.tab_buttons.append(button)

        dashboard_content = QStackedWidget()

        # Home Tab
        home_tab = QWidget()
        home_layout = QVBoxLayout()

# Adding six big buttons to the Home tab, two in each row
        buttons_layout = QHBoxLayout()

# Button 1
        button1 = QPushButton('Carving')
        button1.setObjectName("homeButton")
        button1.setFont(QFont("Arial", 14, QFont.Bold))
        button1.clicked.connect(lambda _, button_id=1: self.home_button_clicked(button_id))
        buttons_layout.addWidget(button1)

# Button 2
        button2 = QPushButton('Hex Reader')
        button2.setObjectName("homeButton")
        button2.setFont(QFont("Arial", 14, QFont.Bold))
        button2.clicked.connect(lambda _, button_id=2: self.home_button_clicked(button_id))
        buttons_layout.addWidget(button2)

# Add the buttons_layout to home_layout
        home_layout.addLayout(buttons_layout)

# Button 3
        button3 = QPushButton('File Explorer')
        button3.setObjectName("homeButton")
        button3.setFont(QFont("Arial", 14, QFont.Bold))
        button3.clicked.connect(lambda _, button_id=3: self.home_button_clicked(button_id))
        home_layout.addWidget(button3)

# Button 4
        button4 = QPushButton('Button 4')
        button4.setObjectName("homeButton")
        button4.setFont(QFont("Arial", 14, QFont.Bold))
        button4.clicked.connect(lambda _, button_id=4: self.home_button_clicked(button_id))
        home_layout.addWidget(button4)

# Button 5
        button5 = QPushButton('Button 5')
        button5.setObjectName("homeButton")
        button5.setFont(QFont("Arial", 14, QFont.Bold))
        button5.clicked.connect(lambda _, button_id=5: self.home_button_clicked(button_id))
        home_layout.addWidget(button5)

# Button 6
        button6 = QPushButton('Button 6')
        button6.setObjectName("homeButton")
        button6.setFont(QFont("Arial", 14, QFont.Bold))
        button6.clicked.connect(lambda _, button_id=6: self.home_button_clicked(button_id))
        home_layout.addWidget(button6)

# Scroll Area for Home Tab
        home_scroll_area = QScrollArea()
        home_scroll_area.setWidgetResizable(True)
        home_scroll_area.setWidget(QWidget())
        home_scroll_area.widget().setLayout(home_layout)

        dashboard_content.addWidget(home_scroll_area)

        # Download Tab
        download_tab = QWidget()
        download_layout = QVBoxLayout()
        for i in range(3):
            button = QPushButton(f'Download Button {i+1}')
            button.setObjectName("downloadButton")
            button.clicked.connect(lambda _, button_id=i+1: self.download_button_clicked(button_id))
            download_layout.addWidget(button)
        download_tab.setLayout(download_layout)
        dashboard_content.addWidget(download_tab)

        # Info Tab
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

        self.setWindowTitle('Scrollable Dashboard')
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
        index = ["Home", "Download", "Info"].index(tab_name)
        self.tab_buttons[index].setChecked(True)
        self.findChild(QStackedWidget).setCurrentIndex(index)

    def home_button_clicked(self, button_id):
        print(f'Home Button {button_id} clicked')
        # Launch another application (other_app.py) using subprocess
        if(button_id == 1):
            subprocess.Popen(["python", "carving.py"])
        if(button_id == 2):
            subprocess.Popen(["python", "hex_main.py"])
        if(button_id == 3):
            subprocess.Popen(["python", "file_explorer.py"])

    def download_button_clicked(self, button_id):
        print(f'Download Button {button_id} clicked')
        # Add functionality for Download buttons

    def get_random_sentences(self):
        sentences = [
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
            "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
            "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        ]
        return sentences


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec_())
