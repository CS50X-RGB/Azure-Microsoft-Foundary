from io import BytesIO
from pypdf import PdfReader
from azure.storage.blob import ContainerClient
from pathlib import Path

def debug_pdf(file_bytes: bytes):
    Path("debug.pdf").write_bytes(file_bytes)

    reader = PdfReader(BytesIO(file_bytes))

    for i, page in enumerate(reader.pages):
        print("Page:", i + 1)
        print("Images:", len(page.images))
        print("Resources:", page.get("/Resources"))


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
            # debug_pdf(file_bytes=file_bytes)
            text = extract_pdf(file_bytes=file_bytes)
        

        extract_doc.append({
            "source" : blob.name,
            "text" : text       
        })
    return extract_doc

def extract_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))

    text = ""

    for i, page in enumerate(reader.pages):
        page_text = page.extract_text()
        text += (page_text or "") + "\n"

    return text