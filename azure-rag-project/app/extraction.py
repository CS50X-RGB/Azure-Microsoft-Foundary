from io import BytesIO
from pypdf import PdfReader
from azure.storage.blob import ContainerClient

def extract_docs(container_client : ContainerClient):
    extract_doc = []
    
    blobs = container_client.list_blobs(
        name_starts_with="raw/"
    )

    for blob in blobs:
        blob_client = container_client.get_blob_client(
            blob=blob.name
        )
        
        file_bytes = blob_client.download_blob().readall()
        text = ""
        if blob.name.endswith(".pdf"):
            text = extract_pdf(file_bytes=file_bytes)
        

        extract_doc.append({
            "soruce" : blob.name,
            "text" : text       
        })
    return extract_doc

def extract_pdf(file_bytes : bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    
    text = ""
    
    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"
    
    return text