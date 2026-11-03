from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
load_dotenv()


api_key = os.environ["AZURE_API_TOKEN"]

llm = init_chat_model(
    model="azure_ai:gpt-4.1-mini",
    base_url="https://rohanchatterjee866-5140-resource.services.ai.azure.com/openai/v1",
    api_key=api_key
)

print(llm.invoke("Capital of India?"))