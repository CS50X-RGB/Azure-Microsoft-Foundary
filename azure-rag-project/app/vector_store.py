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

def store_chunks(chunks : list[dict]):
    result = search_client.upload_documents(
        documents=chunks
    )
    
    return result