import os
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from dotenv import load_dotenv

load_dotenv()

def generate_response(prompt):
    """
    PERSON 2: Context-aware analysis using LangChain.
    """
    # Initialize the NVIDIA Mistral model via LangChain
    llm = ChatNVIDIA(model="mistralai/mixtral-8x7b-instruct-v0.1")
    
    response = llm.invoke(prompt)
    return response.content