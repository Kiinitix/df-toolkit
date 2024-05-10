from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class Configure(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Second Window")
        self.label = QLabel("This is the second window.")
        self.setGeometry(100, 100, 800, 600)
        #self.setFixedSize(300, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
