import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from configure import Configure

class ThreeButtonWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Three Button Window")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        self.button1 = QPushButton("Configure OCI")
        self.button2 = QPushButton("Upload")
        self.button3 = QPushButton("Download")

        layout = QVBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)

        self.setLayout(layout)

        self.button1.clicked.connect(self.open_configure_window)

    def open_configure_window(self):
        self.conf = Configure()
        self.conf.show()

def main():
    app = QApplication(sys.argv)
    window = ThreeButtonWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
