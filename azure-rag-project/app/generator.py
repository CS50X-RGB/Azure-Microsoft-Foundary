from app.llm import get_llm
from app.embedder import embed_query
from app.vector_store import retrieve_chunks
from langchain_core.prompts import ChatPromptTemplate

def generate_answer(query: str):
    query_embedding = embed_query(query)

    docs = retrieve_chunks(query_embedding)

    ctx = "\n\n".join(
        doc["text"] for doc in docs
    )

    prompt = ChatPromptTemplate.from_template("""
        You are a helpful AI assistant.

        Answer the user's question using ONLY the provided context.

        Instructions:
        - Do not make up information.
        - If the context doesn't contain the answer, say you don't know.
        - Give a clear and concise answer.

        Context:
        {ctx}

        User Question:
        {question}

        Answer:
    """)

    chain = prompt | get_llm()

    response = chain.invoke({
        "ctx": ctx,
        "question": query
    })

    return response.content

if __name__ == "__main__":
    print("Give me prompt")
    query = input()
    print(generate_answer(query=query))