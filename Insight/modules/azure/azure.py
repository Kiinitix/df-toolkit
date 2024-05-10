import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLineEdit
from azure.storage.blob import BlobServiceClient

class AzureFileManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Azure File Manager")
        self.init_ui()

    def init_ui(self):
        self.access_key_label = QLabel("Access Key:")
        self.access_key_input = QLineEdit()
        self.label = QLabel("No file selected")
        self.upload_button = QPushButton("Upload File")
        self.upload_button.clicked.connect(self.upload_file)
        self.download_button = QPushButton("Download File")
        self.download_button.clicked.connect(self.download_file)

        layout = QVBoxLayout()
        layout.addWidget(self.access_key_label)
        layout.addWidget(self.access_key_input)
        layout.addWidget(self.label)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.download_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Upload")
        if file_path:
            connection_string = f"DefaultEndpointsProtocol=https;AccountName=<account_name>;AccountKey={self.access_key_input.text()};EndpointSuffix=core.windows.net"
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            blob_client = blob_service_client.get_blob_client(container="<container_name>", blob=file_path)
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data)
            self.label.setText(f"Uploaded file: {file_path}")

    def download_file(self):
        download_path, _ = QFileDialog.getSaveFileName(self, "Save File")
        if download_path:
            connection_string = f"DefaultEndpointsProtocol=https;AccountName=<account_name>;AccountKey={self.access_key_input.text()};EndpointSuffix=core.windows.net"
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            blob_client = blob_service_client.get_blob_client(container="<container_name>", blob=download_path)
            with open(download_path, "wb") as data:
                data.write(blob_client.download_blob().readall())
            self.label.setText(f"Downloaded file: {download_path}")

def main():
    app = QApplication(sys.argv)
    window = AzureFileManager()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
