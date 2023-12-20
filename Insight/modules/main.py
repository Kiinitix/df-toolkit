import sys
import pefile
import binascii
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTextEdit, QVBoxLayout, QWidget, QPushButton

class StaticMalwareAnalyzerApp(QMainWindow):
    def __init__(self):
        super(StaticMalwareAnalyzerApp, self).__init__()

        self.setWindowTitle("Static Malware Analyzer")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.txt_file_content = QTextEdit(self.central_widget)
        self.layout.addWidget(self.txt_file_content)

        self.btn_analyze = QPushButton("Analyze File", self.central_widget)
        self.btn_analyze.clicked.connect(self.analyze_file)
        self.layout.addWidget(self.btn_analyze)

        self.txt_report = QTextEdit(self.central_widget)
        self.layout.addWidget(self.txt_report)

    def analyze_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select a file", "", "Executable Files (*.exe);;All Files (*)")
        if file_path:
            self.clear_results()
            self.display_file_content(file_path)
            self.analyze_pe_header(file_path)
            self.analyze_strings(file_path)

    def clear_results(self):
        self.txt_file_content.clear()
        self.txt_report.clear()

    def display_file_content(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                content_hex = binascii.hexlify(file.read()).decode('utf-8')
                self.txt_file_content.setPlainText(content_hex)
        except Exception as e:
            self.txt_report.append(f"Error reading file: {str(e)}")

    def analyze_pe_header(self, file_path):
        try:
            pe = pefile.PE(file_path)
            self.txt_report.append(f"\nPE Header Analysis:\n")
            self.txt_report.append(f"Image Base: 0x{pe.OPTIONAL_HEADER.ImageBase:08X}")
            self.txt_report.append(f"Entry Point: 0x{pe.OPTIONAL_HEADER.AddressOfEntryPoint:08X}")
            self.txt_report.append(f"Sections:")
            #for section in pe.sections:
                #self.txt_report.append(f"  - {section.Name.decode(errors='ignore').rstrip('\\x00')}")

        except pefile.PEFormatError as e:
            self.txt_report.append(f"\nError analyzing PE header: {str(e)}")

    def analyze_strings(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                content = file.read().decode(errors='ignore')
                strings = [s for s in content.split('\x00') if s]
                self.txt_report.append(f"\nString Analysis:\n")
                for string in strings:
                    self.txt_report.append(f"  - {string}")

        except Exception as e:
            self.txt_report.append(f"\nError analyzing strings: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = StaticMalwareAnalyzerApp()
    mainWindow.show()
    sys.exit(app.exec_())
