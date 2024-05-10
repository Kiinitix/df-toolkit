import oci
import boto3

class OCIObjectStorageClient:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.client = self.create_client()

    def create_client(self):
        config = oci.config.from_file(self.config_file_path)
        return oci.object_storage.ObjectStorageClient(config)

    def upload_file(self, bucket_name, object_name, file_path):
        try:
            with open(file_path, "rb") as f:
                self.client.put_object(bucket_name, object_name, f)
            print(f"File '{object_name}' uploaded successfully to bucket '{bucket_name}'")
        except Exception as e:
            print(f"Error uploading file: {e}")

    def download_file(self, bucket_name, object_name, download_path):
        try:
            response = self.client.get_object(bucket_name, object_name)
            with open(download_path, 'wb') as f:
                for chunk in response.data.raw.stream(1024 * 1024, decode_content=False):
                    f.write(chunk)
            print(f"File '{object_name}' downloaded successfully to '{download_path}'")
        except Exception as e:
            print(f"Error downloading file: {e}")

def main():
    config_file_path = input('/path/to/config_file' ) # Path to your OCI config file
    bucket_name = input('your_bucket_name')
    object_name = input('your_object_name')
    file_path = input('/path/to/local_file')
    download_path = input('/path/to/downloaded_file')

    oci_object_storage_client = OCIObjectStorageClient(config_file_path)
    oci_object_storage_client.upload_file(bucket_name, object_name, file_path)
    oci_object_storage_client.download_file(bucket_name, object_name, download_path)

if __name__ == "__main__":
    main()
