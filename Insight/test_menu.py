import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
import importlib

class ModuleWindow(QWidget):
    def __init__(self, modules):
        super().__init__()

        self.modules = modules
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        for module in self.modules:
            button = QPushButton(module)
            func = self.createFunction(module)
            button.clicked.connect(func)
            layout.addWidget(button)

        self.setLayout(layout)
        self.setWindowTitle('Module Buttons')
        self.show()

    def createFunction(self, module):
        def buttonClicked():
            mod = importlib.import_module(module)
            print(f"{module} function triggered")
        return buttonClicked

if __name__ == '__main__':
    app = QApplication(sys.argv)
    available_modules_file = "available_modules.txt"
    with open(available_modules_file, 'r') as file:
        available_modules = [line.strip() for line in file.readlines()]

    window = ModuleWindow(available_modules)
    sys.exit(app.exec_())
