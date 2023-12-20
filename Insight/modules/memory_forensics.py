import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, QTextBrowser, QLineEdit


class MemoryForensicsApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Memory Forensics')
        self.setGeometry(100, 100, 800, 600)

        # Create the main widget and set it as the central widget
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Create layout
        layout = QVBoxLayout(main_widget)

        # Create widgets
        label = QLabel('Memory Forensics', self)
        layout.addWidget(label)

        # Process list
        process_label = QLabel('Running Processes:', self)
        layout.addWidget(process_label)

        self.process_list = QTextBrowser(self)
        layout.addWidget(self.process_list)

        # Plugin input
        plugin_label = QLabel('Enter Volatility Plugin:', self)
        layout.addWidget(plugin_label)

        self.plugin_input = QLineEdit(self)
        layout.addWidget(self.plugin_input)

        # Analyze memory dump button
        analyze_button = QPushButton('Analyze Memory Dump', self)
        analyze_button.clicked.connect(self.analyze_memory_dump)
        layout.addWidget(analyze_button)

        # Back button
        back_button = QPushButton('Back', self)
        back_button.clicked.connect(self.show_running_processes)
        layout.addWidget(back_button)
        back_button.hide()

        self.back_button = back_button

    def list_running_processes(self):
        # Get the list of running processes
        process_list = subprocess.check_output(['tasklist'], universal_newlines=True)
        return process_list

    def show_running_processes(self):
        # Display the running processes when the back button is clicked
        self.process_list.setPlainText(self.list_running_processes())
        self.back_button.hide()

    def analyze_memory_dump(self):
        # Open file dialog to select a memory dump
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        dump_file, _ = QFileDialog.getOpenFileName(self, 'Open Memory Dump', '', 'All Files (*);;Memory Dump Files (*.dmp)', options=options)

        if dump_file:
            # Use Volatility to analyze the memory dump with the specified plugin
            selected_plugin = self.plugin_input.text()
            volatility_cmd = f"volatility -f {dump_file} {selected_plugin}"
            try:
                result = subprocess.check_output(volatility_cmd, shell=True, universal_newlines=True)
                # Display the result in the QTextBrowser
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
