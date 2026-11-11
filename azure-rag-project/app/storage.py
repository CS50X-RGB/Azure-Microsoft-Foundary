import os
from app.upload import upload_directory
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from pathlib import Path

account_name = os.environ["AZURE_STORAGE_ACCOUNT"]

account_url = f"https://{account_name}.blob.core.windows.net"

cred = DefaultAzureCredential()

blob_service_client = BlobServiceClient(
    account_url=account_name,
    credential=cred
)

container_client = blob_service_client.get_container_client(
    "documents"
)

if __name__ == "__main__":
    file_path = Path('data/raw')
    
    upload_directory(file_path)
    
    cred.close()    