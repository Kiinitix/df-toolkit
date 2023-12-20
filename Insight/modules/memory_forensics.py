import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, QTextBrowser, QLineEdit


class MemoryForensicsApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Memory Forensics')
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout(main_widget)

        label = QLabel('Memory Forensics', self)
        layout.addWidget(label)

        process_label = QLabel('Running Processes:', self)
        layout.addWidget(process_label)

        self.process_list = QTextBrowser(self)
        layout.addWidget(self.process_list)

        plugin_label = QLabel('Enter Volatility Plugin:', self)
        layout.addWidget(plugin_label)

        self.plugin_input = QLineEdit(self)
        layout.addWidget(self.plugin_input)

        analyze_button = QPushButton('Analyze Memory Dump', self)
        analyze_button.clicked.connect(self.analyze_memory_dump)
        layout.addWidget(analyze_button)

        back_button = QPushButton('Back', self)
        back_button.clicked.connect(self.show_running_processes)
        layout.addWidget(back_button)
        back_button.hide()

        self.back_button = back_button

    def list_running_processes(self):
        process_list = subprocess.check_output(['tasklist'], universal_newlines=True)
        return process_list

    def show_running_processes(self):
        self.process_list.setPlainText(self.list_running_processes())
        self.back_button.hide()

    def analyze_memory_dump(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        dump_file, _ = QFileDialog.getOpenFileName(self, 'Open Memory Dump', '', 'All Files (*);;Memory Dump Files (*.dmp)', options=options)

        if dump_file:
            selected_plugin = self.plugin_input.text()
            volatility_cmd = f"volatility -f {dump_file} {selected_plugin}"
            try:
                result = subprocess.check_output(volatility_cmd, shell=True, universal_newlines=True)
                self.process_list.setPlainText(result)
                self.back_button.show()
            except subprocess.CalledProcessError as e:
                self.process_list.setPlainText(f"Error: {e}")
                self.back_button.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MemoryForensicsApp()
    main_app.show()
    sys.exit(app.exec_())
