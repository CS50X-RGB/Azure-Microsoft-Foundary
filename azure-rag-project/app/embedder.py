from app.llm import get_embedding_model
from dotenv import load_dotenv
import os

load_dotenv()

client = get_embedding_model()

def generate_embedding(chunks : list[dict]):
    text = [chunk['text'] for chunk in chunks]
    
    response  = client.embeddings.create(
        model=os.getenv("AZURE_EMBEDDING_MODEL_NAME"),
        inputs=text
    )
    
    for chunk,item in zip(chunks,response.data):
        chunk['embedding'] = item.embedding
    
    return chunks