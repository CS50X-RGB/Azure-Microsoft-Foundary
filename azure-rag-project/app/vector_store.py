import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile
)
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

load_dotenv()

endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
key = ''.join(os.getenv("AZURE_SEARCH_API_KEY"))
index_name = os.getenv("AZURE_SEARCH_INDEX")


cred = AzureKeyCredential(key=key)

index_client = SearchIndexClient(
    endpoint=endpoint,
    credential=cred
)

fields = [
    SimpleField(
        name="id",
        type=SearchFieldDataType.String,
        key=True
    ),
    SimpleField(
        name="source",
        type=SearchFieldDataType.String,
        filterable=True
    ),
    SearchableField(
        name="text",
        type=SearchFieldDataType.String
    ),
    SearchField(
        name="embedding",
        type=SearchFieldDataType.Collection(
            SearchFieldDataType.Single
        ),
        searchable=True,
        vector_search_dimensions=1536,
        vector_search_profile_name="my-vector-profile"
    )
]

vector_search = VectorSearch(
    algorithms=[
        HnswAlgorithmConfiguration(
            name="my-hnsw"
        )
    ],
    profiles=[
        VectorSearchProfile(
            name="my-vector-profile",
            algorithm_configuration_name="my-hnsw"
        )
    ]
)

index = SearchIndex(
    name=index_name,
    fields=fields,
    vector_search=vector_search
)

index_client.create_or_update_index(index=index)

search_client = SearchClient(
    endpoint=endpoint,
    index_name=index_name,
    credential=cred
)
def store_chunks(chunks: list[dict]):
    allowed_fields = {"id", "source", "text", "embedding"}

    for chunk in chunks:
        extra_fields = set(chunk.keys()) - allowed_fields

        if extra_fields:
            raise ValueError(f"Unexpected fields: {extra_fields}")

    result = search_client.upload_documents(documents=chunks)

    for item in result:
        print(item.key, item.succeeded, item.error_message)

    return result

def retrieve_chunks(query_embedding : list[float],top_k :int = 5):
    vector_query = VectorizedQuery(
        vector=query_embedding,
        k_nearest_neighbors=top_k,
        fields="embedding"
    )
    
    results = search_client.search(
        search_text=None,
        vector_queries=[vector_query],
        select=["id","source","text"]
    )
    return list(results)