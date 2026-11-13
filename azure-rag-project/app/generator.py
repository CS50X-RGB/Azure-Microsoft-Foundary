from app.llm import get_llm
from langchain_core.prompts import ChatPromptTemplate

def generate_answer(query : str,docs : list):
    
    ctx = "\n\n".join(
        doc['text'] for doc in docs
    )
    
    prompt = ChatPromptTemplate(
        """
        You are a helpful AI assistant.
        
        Answer the user's question using ONLY the provided context.
        
        Instructions:
        - Do not make up information
        - If the context doesn't contain the answer,say you don't know
        - Give a clear and concise answer.
        
        Context:
        {ctx}
        
        User Question:
        {question}
        
        Answer:
        """
    )
    
    chain = prompt | get_llm()
    
    
    response = chain.invoke({
        'ctx' : ctx,
        'question' : query
    })
    
    return response.content