from app.storage import container_client
from pathlib import Path

def upload_file(file_path : Path):
    blob_name = f"raw/{file_path.name}"
    
    with file_path.open("rb") as file:
        container_client.upload_blob(
            name=blob_name,
            data=file,
            overwrite=True
        )
        
    print(f"Uploaded: {blob_name}")
    
def upload_directory(dir : str):
    
    dir_path = Path(dir)
    
    for file_path in dir_path.rglob("*"):
        if not file_path.is_file():
            continue
        
        rel_path = file_path.relative_to(dir_path)
        blob_name = f"raw/{rel_path.as_posix()}"
        
        
        with file_path.open("rb") as file:
            container_client.upload_blob(
                name=blob_name,
                data=file,
                overwrite=True
            )
        
        
        print(f"Uploaded  : {blob_name}")