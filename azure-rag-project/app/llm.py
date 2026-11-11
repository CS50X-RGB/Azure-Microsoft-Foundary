import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def get_llm():
    return ChatOpenAI(
        model=os.getenv("AZURE_MODEL_NAME"),
        base_url=os.getenv("AZURE_API_ENDPOINT"),
        api_key=os.getenv("AZURE_API_KEY"),
        temperature=0.2
    )