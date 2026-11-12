import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from app.llm import get_embedding_model
load_dotenv()

search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name=os.getenv("AZURE_SEARCH_INDEX"),
    credential=AzureKeyCredential(
        os.getenv("AZURE_SEARCH_API_KEY")
    )
)

embedding_client = get_embedding_model()

def retrieve_documents(query : str,k : int = 3):
    response = embedding_client.embeddings.create(
        model=os.getenv("AZURE_EMBEDDING_MODEL_NAME")
    )
    
    query_vector = response.data[0].embedding
    
    results = search_client.search(
        search_text=None,
        vector_queries=[
            {
                "kind" : "vector",
                "vector" : query_vector,
                "fields" : "embedding",
                "k" : k
            }
        ],
        select=["id","text","source"]
    )
    
    return list(results)