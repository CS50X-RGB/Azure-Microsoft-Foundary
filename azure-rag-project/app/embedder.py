from app.llm import get_embedding_model
from dotenv import load_dotenv
import os
import base64
load_dotenv()

client = get_embedding_model()

def generate_id(source: str, chunk_index: int) -> str:
    raw_id = f"{source}_{chunk_index}"
  
    return base64.urlsafe_b64encode(
          raw_id.encode("utf-8")
      ).decode("utf-8").rstrip("=")


def generate_embedding(chunks):
    embedded_chunks = []
    batch_size = 100

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]

        response = client.embeddings.create(
            model=os.getenv("AZURE_EMBEDDING_MODEL_NAME"),
            input=[chunk["text"] for chunk in batch]
        )

        for j, (chunk, embedding_data) in enumerate(
            zip(batch, response.data)
        ):
            embedded_chunks.append({
                "id": generate_id(chunk["source"], i + j),
                "source": chunk["source"],
                "text": chunk["text"],
                "embedding": embedding_data.embedding
            })

    return embedded_chunks


def embed_query(query : str):
    response = client.embeddings.create(
        model=os.getenv("AZURE_EMBEDDING_MODEL_NAME"),
        input=query
    )
    
    return response.data[0].embedding