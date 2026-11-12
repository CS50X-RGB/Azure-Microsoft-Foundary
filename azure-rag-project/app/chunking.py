from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_docs(documents : list[dict[str,str]]):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n","\n"," ",""]
    )
    
    chunks = []
    
    for doc in documents:
        text_chunks = splitter.split_text(doc['text'])
        
        for i,chunk in enumerate(text_chunks):
            chunks.append({
                "id" : f'{doc['source']}_{i}',
                "text" : chunk,
                "source" : doc['source']
            })
    return chunks