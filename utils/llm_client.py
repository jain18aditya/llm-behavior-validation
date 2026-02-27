
from openai import OpenAI
from config import MODEL
import os
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def generate(prompt, temperature):
    response = client.responses.create(model=MODEL, input=prompt,
                                       temperature=temperature, max_output_tokens=80)
    return response.output_text.strip()

def generate_full_response(prompt, temperature):
    return client.responses.create(model=MODEL, input=prompt,
                                   temperature=temperature, max_output_tokens=80)

def get_client():
    return client

def get_model():
    return MODEL

def get_chroma_client():
    return chromadb.PersistentClient(path="./chroma_db")