import sys
import psutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QComboBox, QPushButton, QTextBrowser


class DiskAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Disk Analyzer')
        self.setGeometry(100, 100, 600, 400)

        # Create the main widget and set it as the central widget
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Create layout
        layout = QVBoxLayout(main_widget)

        # Create widgets
        label = QLabel('Disk Analyzer', self)
        layout.addWidget(label)

        # Partition selection dropdown
        self.partition_combo = QComboBox(self)
        self.partition_combo.currentIndexChanged.connect(self.refresh_disk_info)
        layout.addWidget(self.partition_combo)

        # Display disk information
        self.disk_info = QTextBrowser(self)
        layout.addWidget(self.disk_info)

        # Refresh button
        refresh_button = QPushButton('Refresh', self)
        refresh_button.clicked.connect(self.refresh_disk_info)
        layout.addWidget(refresh_button)

        # Populate partition dropdown and display initial information
        self.populate_partitions()
        self.refresh_disk_info()

    def populate_partitions(self):
        # Populate the partition dropdown with available partitions
        partitions = [partition.device for partition in psutil.disk_partitions()]
        self.partition_combo.addItems(partitions)

    def refresh_disk_info(self):
        # Display detailed disk information for the selected partition
        selected_partition = self.partition_combo.currentText()
        disk_info_text = self.get_partition_info(selected_partition)
        self.disk_info.setPlainText(disk_info_text)

    def get_partition_info(self, partition):
        disk_info = f"Partition Information for {partition}:\n\n"
        try:
            usage = psutil.disk_usage(partition)

            disk_info += f"Total Size: {self.convert_bytes(usage.total)}\n"
            disk_info += f"Used Space: {self.convert_bytes(usage.used)}\n"
            disk_info += f"Free Space: {self.convert_bytes(usage.free)}\n\n"

            # Display file and directory information
            disk_info += "File and Directory Information:\n\n"
            for item in psutil.disk_partitions():
                if item.device == partition:
                    for entry in psutil.os.scandir(item.mountpoint):
                        disk_info += f"{entry.name}\n"
            return disk_info
        except Exception as e:
            return f"Error retrieving information: {str(e)}"

    @staticmethod
    def convert_bytes(bytes_val):
        # Convert bytes to human-readable format
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_val < 1024.0:
                break
            bytes_val /= 1024.0
        return f"{bytes_val:.2f} {unit}"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = DiskAnalyzerApp()
    main_app.show()
    sys.exit(app.exec_())
